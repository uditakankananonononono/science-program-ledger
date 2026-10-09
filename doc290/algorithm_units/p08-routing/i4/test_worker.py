import unittest,json,copy
from pathlib import Path
from core import launch,gate,validate_record
class Controls(unittest.TestCase):
    def test_success_real(self):
        r=launch(['devsubject',0]);self.assertEqual(r['status'],'PASS',r);self.assertEqual(r['worker']['identity'],gate());Path('/tmp/i4-dev-success.json').write_text(json.dumps(r,indent=2)+'\n')
    def test_real_failures(self):
        rs={m:launch([m],timeout=.3 if m=='sleep' else 5) for m in ('sleep','memory','gatefail','badjson')}
        self.assertTrue(all(r['status']=='FAIL' and r['reaped'] for r in rs.values()));self.assertEqual(rs['sleep']['stdout'],'sleep-ready\n');self.assertEqual(rs['sleep']['returncode'],-9);Path('/tmp/i4-dev-controls.json').write_text(json.dumps(rs,indent=2)+'\n')
    def test_false_payload(self):
        r=launch(['devsubject',0]);self.assertEqual(r['status'],'PASS',r)
        for field,value in (('rss_kib',True),('affinity',[]),('solve_seconds',True),('identity',{})):
            rr=copy.deepcopy(r);rr['worker'][field]=value;rr['stdout']=json.dumps(rr['worker']);self.assertEqual(validate_record(['devsubject',0],rr)['status'],'FAIL')
        rr=copy.deepcopy(r);rr['worker']['result']['candidates'][0]['clamp']='999/1';rr['stdout']=json.dumps(rr['worker']);self.assertEqual(validate_record(['devsubject',0],rr)['status'],'FAIL')
    def test_real_success_top_level_schema_and_index_mutations(self):
        r=launch(['devsubject',0]);self.assertEqual(r['status'],'PASS',r)
        changes=[]
        for key,value in (('gap','999/1'),('selected_index',False),('selected_index',0.0),('best_lower','999/1')):
            rr=copy.deepcopy(r);rr['worker']['result'][key]=value;changes.append(rr)
        rr=copy.deepcopy(r);rr['worker']['result']['primal']['worst_time']=999;changes.append(rr)
        rr=copy.deepcopy(r);rr['worker']['result']['candidates'][0]['index']=False;changes.append(rr)
        rr=copy.deepcopy(r);rr['worker']['result']['candidates'][0]['index']=0.0;changes.append(rr)
        rr=copy.deepcopy(r);rr['worker']['result']['extra']=0;changes.append(rr)
        rr=copy.deepcopy(r);del rr['worker']['result']['gap'];changes.append(rr)
        rr=copy.deepcopy(r);rr['worker']['result']['candidates'][0]['extra']=0;changes.append(rr)
        rr=copy.deepcopy(r);del rr['worker']['result']['candidates'][0]['potential'];changes.append(rr)
        rr=copy.deepcopy(r);rr['worker']['result']['candidates'].pop();changes.append(rr)
        rr=copy.deepcopy(r);rr['worker']['result']['candidates'].reverse();changes.append(rr)
        for rr in changes:
            rr['stdout']=json.dumps(rr['worker']);self.assertEqual(validate_record(['devsubject',0],rr)['status'],'FAIL')
