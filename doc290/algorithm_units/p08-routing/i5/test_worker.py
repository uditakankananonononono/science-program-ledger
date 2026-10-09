import unittest,json,copy
from pathlib import Path
from core import launch,validate_record,gate
class Controls(unittest.TestCase):
    def test_real_success(self):
        r=launch(['devsubject',0]);self.assertEqual(r['status'],'PASS',r);self.assertEqual(r['worker']['identity'],gate());Path('/tmp/i5-dev-success.json').write_text(json.dumps(r,indent=2)+'\n')
    def test_real_controls(self):
        rs={m:launch([m],timeout=.3 if m=='sleep' else 5) for m in ('sleep','memory','gatefail','badjson')};self.assertTrue(all(r['status']=='FAIL' and r['reaped'] for r in rs.values()));self.assertEqual(rs['sleep']['returncode'],-9);Path('/tmp/i5-dev-controls.json').write_text(json.dumps(rs,indent=2)+'\n')
    def test_real_parent_mutations(self):
        r=launch(['devsubject',0]);self.assertEqual(r['status'],'PASS',r);changes=[]
        for k,v in (('gap','999/1'),('selected_weight',False),('selected_weight',0.0),('primal',{}),('extra',0)):
            rr=copy.deepcopy(r);rr['worker']['result'][k]=v;changes.append(rr)
        rr=copy.deepcopy(r);rr['worker']['result']['weights'][0]['index']=False;changes.append(rr)
        rr=copy.deepcopy(r);rr['worker']['result']['weights'][0]['points'][0]['lambda']='99/1';changes.append(rr)
        rr=copy.deepcopy(r);rr['worker']['result']['paths'][0]['exposure']=False;changes.append(rr)
        rr=copy.deepcopy(r);del rr['worker']['result']['gap'];changes.append(rr)
        for rr in changes:
            rr['stdout']=json.dumps(rr['worker']);self.assertEqual(validate_record(['devsubject',0],rr)['status'],'FAIL')

    def test_real_short_receipt_reason_mutations(self):
        saved={}
        for mode in ('devmissing','devdomain'):
            args=[mode,0];r=launch(args);self.assertEqual(r['status'],'PASS',r);saved[mode]=r
            for v in (False,{},[],0,None):
                rr=copy.deepcopy(r);rr['worker']['result']['reason']=v
                rr['stdout']=json.dumps(rr['worker']);self.assertEqual(validate_record(args,rr)['status'],'FAIL')
        Path('/tmp/i5-dev-short.json').write_text(json.dumps(saved,indent=2)+'\n')
