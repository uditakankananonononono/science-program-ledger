import unittest,copy,importlib.util
from pathlib import Path
from unittest.mock import patch
from method import solve
from proof import check,original
from fixtures import edge,oracle
from model import Invalid
spec=importlib.util.spec_from_file_location('dev_original_t8',Path(__file__).resolve().parent.parent/'t8'/'method.py');t8=importlib.util.module_from_spec(spec);spec.loader.exec_module(t8)
t8.original_t7_proof=original.original;t8.scenario_check=original.scenario_check;t8.incumbent_check=original.incumbent_check
class Development(unittest.TestCase):
    def s(self):return {'graph':{'a':[edge('g',[4,4],0),edge('g',[4,4],0),edge('a',[0,0],0)],'g':[edge('a',[0,0],0)]},'start':'a','goal':'g','budget':0,'forbidden':[[['a',0],['g',0]]],'penalties':[]}
    def test_equality_all_phase_zero(self):
        s=self.s();r=solve(s);check(s,r);self.assertEqual(r['certificate']['reason'],'equality_exit');self.assertEqual(r['route'],r['incumbent']);self.assertEqual(oracle(s),4)
        for k in ('candidate_edges','forbidden_skipped','feasibility_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue','objective_bound_pruned'):self.assertEqual(r['counters'][k],0)
        s['goal']='a';r=solve(s);check(s,r);self.assertEqual(r['certificate']['lower'],0);self.assertEqual(r['route']['edges'],[])
    def test_strict_gap_loop_correlated(self):
        s=self.s();s['graph']['a']=[edge('g',[1,5],0),edge('g',[5,1],0)];s['forbidden']=[];r=solve(s);check(s,r);old=t8.solve(s);self.assertEqual(r['certificate']['lower'],1);self.assertEqual(r['certificate']['upper'],5);self.assertEqual(r['certificate']['reason'],'strict_gap_search')
        for k in ('route','counters','proof','scenario_proof','incumbent'):self.assertEqual(r[k],old[k])
    def test_metadata_rejection(self):
        s=self.s();r=solve(s)
        for key,v in (('lower',True),('upper',4.0),('lower',0),('upper',None),('reason','strict_gap_search'),('equality_exit',1),('early_exit',True),('budget',False)):
            rr=copy.deepcopy(r);rr['certificate'][key]=v
            with self.assertRaises(Invalid):check(s,rr)
        for k in ('candidate_edges','forbidden_skipped','feasibility_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue','objective_bound_pruned'):
            rr=copy.deepcopy(r);rr['counters'][k]=1
            with self.assertRaises(Invalid):check(s,rr)
        rr=copy.deepcopy(r);rr['route']=copy.deepcopy(rr['route']);rr['route']['edges'][0]['edge_index']=True
        with self.assertRaises(Invalid):check(s,rr)
        rr=copy.deepcopy(r);rr['route']=copy.deepcopy(rr['route']);rr['route']['edges'][0]['edge_index']=1
        with self.assertRaises(Invalid):check(s,rr)
    def test_contradiction_no_search_rescue(self):
        s=self.s()
        with patch('method.scenario_check',side_effect=RuntimeError('audit')),patch('method.incumbent') as inc:
            with self.assertRaises(RuntimeError):solve(s)
            inc.assert_not_called()
        with patch('method.scenario_check'),patch('method.scenario_reverse',return_value=[[None]*6]*2):
            with self.assertRaises(Invalid):solve(s)
        with patch('method.scenario_check'),patch('method.scenario_reverse',return_value=[[9]*6]*2):
            with self.assertRaises(Invalid):solve(s)
        with patch('method.incumbent',return_value=None):
            with self.assertRaises(Invalid):solve(s)
    def test_infeasible_unchanged(self):
        s=self.s();s['graph']['a']=[edge('g',[4,4],1)];s['forbidden']=[];r=solve(s);check(s,r);self.assertEqual(r['certificate']['reason'],'budget_infeasible');self.assertIsNone(r['scenario_proof']);self.assertIsNone(r['certificate']['lower'])
