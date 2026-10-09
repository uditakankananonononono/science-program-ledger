import unittest,copy,json
from pathlib import Path
from core import launch,validate_record
class Controls(unittest.TestCase):
    def test_real_parent_stages_and_typed_mutations(self):
        saved={}
        for k in range(4):
            args=['devsubject',k];r=launch(args);self.assertEqual(r['status'],'PASS',r);saved[str(k)]=r;changes=[]
            for key,value in [('reason',False),('reason',{}),('original',{}),('extra',0)]:
                rr=copy.deepcopy(r);rr['worker']['result'][key]=value;changes.append(rr)
            z=r['worker']['result']
            for key in z:
                rr=copy.deepcopy(r);del rr['worker']['result'][key];changes.append(rr)
            if 'distances' in z:
                for v in (None,True,2.0,99):
                    rr=copy.deepcopy(r);rr['worker']['result']['distances'][0]=v;changes.append(rr)
                rr=copy.deepcopy(r);rr['worker']['result']['exposure_arcs'][0]['source']=False;changes.append(rr)
            if 'completed_statement' in z:
                rr=copy.deepcopy(r);rr['worker']['result']['completed_statement']['distances'][0]=True;changes.append(rr)
            if 'downstream' in z:
                rr=copy.deepcopy(r);rr['worker']['result']['downstream']['reason']=False;changes.append(rr)
            for rr in changes:rr['stdout']=json.dumps(rr['worker']);self.assertEqual(validate_record(args,rr)['status'],'FAIL')
        Path('/tmp/t10-dev-receipts.json').write_text(json.dumps(saved,indent=2)+'\n')
    def test_real_operational_controls(self):
        rs={m:launch([m],timeout=.3 if m=='sleep' else 5) for m in ('sleep','memory','gatefail','badjson')};self.assertTrue(all(r['status']=='FAIL' and r['reaped'] for r in rs.values()));Path('/tmp/t10-dev-controls.json').write_text(json.dumps(rs,indent=2)+'\n')
