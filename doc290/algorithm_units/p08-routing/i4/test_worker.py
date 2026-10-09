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
