import unittest,copy,json
from pathlib import Path
from core import launch,validate_record
class Controls(unittest.TestCase):
    def test_real_synthetic_variant_and_parent_mutations(self):
        saved={}
        for k in range(11):
            for m in ('variant',):
                args=['devsubject',k,m];r=launch(args);self.assertEqual(r['status'],'PASS',r);saved[f'{k}:{m}']=r;changes=[]
                for key in ('route','counters','proof','certificate','scenario_proof','incumbent','charged_proof','bound_trace','activation','candidate_ledger','incumbent_original_upper','incumbent_selected_upper','selected_candidate','candidate_activation','candidate_prefix','candidate_schedule','weighted_proof'):
                    rr=copy.deepcopy(r);del rr['worker'][key];changes.append(rr)
                rr=copy.deepcopy(r);rr['worker']['extra']=0;changes.append(rr)
                rr=copy.deepcopy(r);rr['worker']['counters']['labels_inserted']=False;changes.append(rr)
                rr=copy.deepcopy(r);rr['worker']['certificate']['reason']=False;changes.append(rr)
                if m=='variant':
                    rr=copy.deepcopy(r);rr['worker']['certificate']['charged_lambda']=True;changes.append(rr)
                    if r['worker']['charged_proof'] is not None:
                        rr=copy.deepcopy(r);rr['worker']['charged_proof']['distances'][0][0]=False;changes.append(rr)
                    if r['worker']['bound_trace']:
                        rr=copy.deepcopy(r);rr['worker']['bound_trace'].pop();changes.append(rr)
                countnames=('reverse_relaxations','scenario_reverse_inspections','incumbent_inspections')+('charged_reverse_inspections',)
                countnames+=('scalar_candidate_inspections','weighted_candidate_inspections')
                for key in countnames:
                    for add in (1,999):
                        rr=copy.deepcopy(r);rr['worker']['counters'][key]+=add;changes.append(rr)
                if m=='variant':
                    for value in (None,False,'charged_bound','old_bound_equality','exposure_exit'):
                        if value!=r['worker']['activation']:
                            rr=copy.deepcopy(r);rr['worker']['activation']=value;changes.append(rr)
                    if r['worker']['activation']=='old_bound_equality':
                        rr=copy.deepcopy(r);rr['worker']['charged_proof']={'states':[],'distances':[],'lambda':1};changes.append(rr)
                if m=='variant' and r['worker']['candidate_ledger'] is not None:
                    for key,value in (('selected_candidate',False),('selected_candidate',0.0),('incumbent_selected_upper',999),('incumbent_original_upper',999)):
                        rr=copy.deepcopy(r);rr['worker'][key]=value;changes.append(rr)
                    rr=copy.deepcopy(r);rr['worker']['candidate_ledger'][1]['audit']['eligible']=not rr['worker']['candidate_ledger'][1]['audit']['eligible'];changes.append(rr)
                    rr=copy.deepcopy(r);rr['worker']['candidate_ledger'][1]['stop_ledger']['inspections']+=1;changes.append(rr)
                    rr=copy.deepcopy(r);rr['worker']['candidate_ledger'][0]['route']['exposure']=False;changes.append(rr)
                if m=='variant':
                    for value in (False,None,'bogus'):
                        rr=copy.deepcopy(r);rr['worker']['candidate_activation']=value;changes.append(rr)
                    if r['worker']['candidate_activation']=='original_bound_equality':
                        rr=copy.deepcopy(r);rr['worker']['candidate_ledger']=[];changes.append(rr)
                        rr=copy.deepcopy(r);rr['worker']['selected_candidate']=0;changes.append(rr)
                if m=='variant' and r['worker']['candidate_prefix'] is not None:
                    meta=r['worker']['candidate_prefix']
                    for key in meta:
                        rr=copy.deepcopy(r);del rr['worker']['candidate_prefix'][key];changes.append(rr)
                    for key,value in [('scenario_count',False),('scenario_count',999),('remaining_scenario_indices',[False]),('selected_index',0.0),('selected_W',False),('original_L',False),('terminal_reason','all_candidates' if meta['terminal_reason']=='bound_equality' else 'bound_equality')]:
                        rr=copy.deepcopy(r);rr['worker']['candidate_prefix'][key]=value;changes.append(rr)
                    rr=copy.deepcopy(r);rr['worker']['candidate_ledger'].append(copy.deepcopy(rr['worker']['candidate_ledger'][-1]));changes.append(rr)
                if m=='t16':
                    rr=copy.deepcopy(r);rr['worker']['candidate_schedule']={};changes.append(rr)
                if m=='variant':
                    for v in (None,False,'bogus'):
                        rr=copy.deepcopy(r);rr['worker']['candidate_schedule']=v;changes.append(rr)
                    if r['worker']['candidate_activation']=='charged_original_bound_equality':
                        for key,v in [('candidate_ledger',[]),('candidate_prefix',{}),('selected_candidate',0),('charged_proof',None)]:
                            rr=copy.deepcopy(r);rr['worker'][key]=v;changes.append(rr)
                if r['worker']['weighted_proof'] is not None:
                    for key in r['worker']['weighted_proof']:
                        rr=copy.deepcopy(r);del rr['worker']['weighted_proof'][key];changes.append(rr)
                    for key,value in [('weights',[1,2]),('weighted_index',True),('selected_index',0.0),('selected_W',False),('preweighted_W',999),('trigger','wrong'),('turn_delay_factor',1),('exposure_weight',1)]:
                        rr=copy.deepcopy(r);rr['worker']['weighted_proof'][key]=value;changes.append(rr)
                    for field in ('state_status','pops','tentative_distances','predecessor_arc','remaining_heap','settled_order','inspections','semantics'):
                        rr=copy.deepcopy(r);del rr['worker']['candidate_ledger'][-1]['stop_ledger'][field];changes.append(rr)
                for rr in changes:
                    rr['stdout']=json.dumps(rr['worker']);self.assertEqual(validate_record(args,rr)['status'],'FAIL')
        Path('/tmp/t17-dev-receipts.json').write_text(json.dumps(saved,indent=2)+'\n')
    def test_real_controls(self):
        rs={m:launch([m],timeout=.3 if m=='sleep' else 5) for m in ('sleep','memory','gatefail','badjson')};self.assertTrue(all(r['status']=='FAIL' and r['reaped'] for r in rs.values()));Path('/tmp/t17-dev-controls.json').write_text(json.dumps(rs,indent=2)+'\n')
