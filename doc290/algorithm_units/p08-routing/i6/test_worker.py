import unittest,json,copy
from pathlib import Path
from core import launch,validate_record,gate,devcase
class Controls(unittest.TestCase):
    def test_real_synthetic_allstage_receipts_and_mutations(self):
        saved={}
        for index in range(6):
            args=['devsubject',index];r=launch(args);self.assertEqual(r['status'],'PASS',r);saved[str(index)]=r;changes=[]
            for k,v in [('reason',False),('reason',{}),('original',{}),('extra',0)]:
                rr=copy.deepcopy(r);rr['worker']['result'][k]=v;changes.append(rr)
            z=r['worker']['result']
            if 'paths' in z and z['paths']:
                rr=copy.deepcopy(r);rr['worker']['result']['paths'][0]['arcs'][0]=False;changes.append(rr)
            for key in ('feasible_indices','objectives'):
                if key in z and z[key]:
                    rr=copy.deepcopy(r);rr['worker']['result'][key][0]=False;changes.append(rr)
            if 'selected_index' in z:
                for v in (False,0.0,999):
                    rr=copy.deepcopy(r);rr['worker']['result']['selected_index']=v;changes.append(rr)
                rr=copy.deepcopy(r);rr['worker']['result']['selected_route']['scenario_totals'][0]=False;changes.append(rr)
            if 'completed_statement' in z:
                rr=copy.deepcopy(r);rr['worker']['result']['completed_statement']['route']['edges'][0]['edge_index']=False;changes.append(rr)
                rr=copy.deepcopy(r);rr['worker']['result']['route_check']['exposure']=False;changes.append(rr)
                rr=copy.deepcopy(r);rr['worker']['result']['downstream']['selected_weight']=False;changes.append(rr)
            for rr in changes:
                rr['stdout']=json.dumps(rr['worker']);self.assertEqual(validate_record(args,rr)['status'],'FAIL')
        Path('/tmp/i6-dev-receipts.json').write_text(json.dumps(saved,indent=2)+'\n')
    def test_real_operational_controls(self):
        rs={m:launch([m],timeout=.3 if m=='sleep' else 5) for m in ('sleep','memory','gatefail','badjson')};self.assertTrue(all(r['status']=='FAIL' and r['reaped'] for r in rs.values()));Path('/tmp/i6-dev-controls.json').write_text(json.dumps(rs,indent=2)+'\n')
