import unittest,json
from pathlib import Path
from core import launch,gate,Invalid
class WorkerControls(unittest.TestCase):
    def test_real_controls(self):
        rows={m:launch([m],timeout=.3 if m=='sleep' else 5) for m in ('sleep','memory','gatefail','badjson')}
        for r in rows.values():self.assertEqual(r['status'],'FAIL');self.assertTrue(r['reaped'])
        self.assertEqual(rows['sleep']['returncode'],-9);self.assertEqual(rows['sleep']['stdout'],'sleep-ready\n');self.assertIn('MemoryError',rows['memory']['stdout']);self.assertIn('JSONDecodeError',rows['badjson']['reason']);Path('/tmp/p4-dev-controls-current.json').write_text(json.dumps(rows,sort_keys=True,indent=2)+'\n')
    def test_success_real_final_gate(self):
        rows={m:launch(['devsubject',0,m]) for m in ('variant','baseline')}
        for r in rows.values():self.assertEqual(r['status'],'PASS',r);self.assertEqual(r['check']['worst_time'],4);self.assertEqual(r['worker']['identity'],gate());self.assertEqual(r['returncode'],0)
        Path('/tmp/p4-dev-success-current.json').write_text(json.dumps(rows,sort_keys=True,indent=2)+'\n')
    def test_malformed_payload_failure(self):
        from unittest.mock import patch
        rows={m:launch(['devsubject',0,m]) for m in ('variant','baseline')}
        import copy
        for key,value in (('rss_kib',True),('affinity',[]),('solve_seconds',True),('identity',{}),('as_limit_bytes',[0,0])):
            payload=copy.deepcopy(rows['variant']['worker']);payload[key]=value
            class P:
                returncode=0
                def communicate(self,timeout=None):return json.dumps(payload).encode(),b''
                def poll(self):return 0
            with patch('core.subprocess.Popen',return_value=P()):self.assertEqual(launch(['devsubject',0,'variant'])['status'],'FAIL')
    def test_false_full_ledger_genuine_success(self):
        from unittest.mock import patch
        import copy
        base=launch(['devsubject',0,'variant']);self.assertEqual(base['status'],'PASS',base)
        for field,value in (('start_minimum',True),('start_minimum',1),('reverse_exposure',{'q':1,'z':0}),('reverse_exposure',{'q':0}),('reverse_exposure',{'q':False,'z':0}),('reverse_exposure',{'q':0,'z':1})):
            payload=copy.deepcopy(base['worker']);payload['proof'][field]=value
            class P:
                returncode=0
                def communicate(self,timeout=None):return json.dumps(payload).encode(),b''
                def poll(self):return 0
            with patch('core.subprocess.Popen',return_value=P()):self.assertEqual(launch(['devsubject',0,'variant'])['status'],'FAIL')
    def test_false_state_ledger_genuine_success(self):
        from unittest.mock import patch
        import copy
        base=launch(['devsubject',0,'variant']);self.assertEqual(base['status'],'PASS',base)
        for field,value in (('start_minimum',True),('start_minimum',1),('distances',[0,0,0,1]),('distances',[False,0,0,0]),('states',[])):
            payload=copy.deepcopy(base['worker']);payload['proof'][field]=value
            class P:
                returncode=0
                def communicate(self,timeout=None):return json.dumps(payload).encode(),b''
                def poll(self):return 0
            with patch('core.subprocess.Popen',return_value=P()):self.assertEqual(launch(['devsubject',0,'variant'])['status'],'FAIL')

    def test_state_schema_genuine_success(self):
        from unittest.mock import patch
        import copy
        base=launch(['devsubject',0,'variant']);self.assertEqual(base['status'],'PASS',base)
        changes=[]
        for value in (False,0.0,True):
            p=copy.deepcopy(base['worker']);p['proof']['states'][1]['incoming'][1]=value;changes.append(p)
        p=copy.deepcopy(base['worker']);p['proof']['states'][1]['extra']=0;changes.append(p)
        p=copy.deepcopy(base['worker']);del p['proof']['states'][1]['vertex'];changes.append(p)
        p=copy.deepcopy(base['worker']);p['proof']['states'][1]['incoming']=('q',0);changes.append(p)
        p=copy.deepcopy(base['worker']);p['proof']['states'][0]['kind']=False;changes.append(p)
        for payload in changes:
            class P:
                returncode=0
                def communicate(self,timeout=None):return json.dumps(payload).encode(),b''
                def poll(self):return 0
            # Tuple JSON is a list on the wire, so this mutation preserves valid schema.
            if isinstance(payload['proof']['states'][1]['incoming'],tuple):continue
            with patch('core.subprocess.Popen',return_value=P()):self.assertEqual(launch(['devsubject',0,'variant'])['status'],'FAIL')
