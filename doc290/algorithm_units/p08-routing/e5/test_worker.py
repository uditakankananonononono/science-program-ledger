import unittest,json
from pathlib import Path
from core import launch,gate,Invalid
class WorkerControls(unittest.TestCase):
    def test_real_controls(self):
        rows={m:launch([m],timeout=.3 if m=='sleep' else 5) for m in ('sleep','memory','gatefail','badjson')}
        for r in rows.values():self.assertEqual(r['status'],'FAIL');self.assertTrue(r['reaped'])
        self.assertEqual(rows['sleep']['returncode'],-9);self.assertEqual(rows['sleep']['stdout'],'sleep-ready\n');self.assertIn('MemoryError',rows['memory']['stdout']);self.assertIn('JSONDecodeError',rows['badjson']['reason']);Path('/tmp/p4-dev-controls-current.json').write_text(json.dumps(rows,sort_keys=True,indent=2)+'\n')
    def test_success_real_final_gate(self):
        rows={m:launch(['devsubject',0,m]) for m in ('variant','p3')}
        for r in rows.values():self.assertEqual(r['status'],'PASS',r);self.assertEqual(r['check']['worst_time'],4);self.assertEqual(r['worker']['identity'],gate());self.assertEqual(r['returncode'],0)
        Path('/tmp/p4-dev-success-current.json').write_text(json.dumps(rows,sort_keys=True,indent=2)+'\n')
    def test_malformed_payload_failure(self):
        from unittest.mock import patch
        rows={m:launch(['devsubject',0,m]) for m in ('variant','p3')}
        import copy
        for key,value in (('rss_kib',True),('affinity',[]),('solve_seconds',True),('identity',{}),('as_limit_bytes',[0,0])):
            payload=copy.deepcopy(rows['variant']['worker']);payload[key]=value
            class P:
                returncode=0
                def communicate(self,timeout=None):return json.dumps(payload).encode(),b''
                def poll(self):return 0
            with patch('core.subprocess.Popen',return_value=P()):self.assertEqual(launch(['devsubject',0,'variant'])['status'],'FAIL')

    def test_false_certificate_genuine_success(self):
        from unittest.mock import patch
        import copy
        base=launch(['devsubject',0,'variant']);self.assertEqual(base['status'],'PASS',base)
        mutations=[]
        p=copy.deepcopy(base['worker']);p['certificate'].update(start_distances=[0,0],lower_bound=0,upper_bound=0);mutations.append(p)
        for field,value in (('upper_bound',0),('lower_bound',0),('start_distances',[3,0]),('early_exit',False),('reason','forward exhaustion'),('upper_bound',True)):
            p=copy.deepcopy(base['worker']);p['certificate'][field]=value;mutations.append(p)
        p=copy.deepcopy(base['worker']);p['counters']['lb_pruned']=1;mutations.append(p)
        p=copy.deepcopy(base['worker']);p['incumbent']=None;mutations.append(p)
        for payload in mutations:
            class P:
                returncode=0
                def communicate(self,timeout=None):return json.dumps(payload).encode(),b''
                def poll(self):return 0
            with patch('core.subprocess.Popen',return_value=P()):self.assertEqual(launch(['devsubject',0,'variant'])['status'],'FAIL')
