import unittest,copy
from unittest.mock import patch
from method import solve
from proof import check,scenario_check,original
from fixtures import edge,oracle
from model import Invalid
class Development(unittest.TestCase):
    def s(self):return {'graph':{'a':[edge('g',[4,4],0),edge('b',[1,1],0),edge('c',[3,3],0),edge('g',[4,4],0)],'b':[edge('g',[5,5],0)],'c':[edge('g',[3,3],0)],'g':[]},'start':'a','goal':'g','budget':0,'forbidden':[],'penalties':[]}
    def test_strict_exclusions_equality(self):
        s=self.s();r=solve(s);check(s,r);self.assertEqual(oracle(s),4);self.assertEqual(r['counters']['objective_bound_pruned'],2);self.assertEqual(r['counters']['labels_inserted'],3)
        # Equal parallel goals retain distinct incoming-edge states, never bound-pruned.
        self.assertEqual(r['counters']['dominance_pruned'],0)
    def test_correlated_minima(self):
        s=self.s();s['graph']={'a':[edge('b',[1,5],0)],'b':[edge('g',[5,1],0),edge('g',[1,5],0)],'g':[]};r=solve(s);check(s,r);self.assertEqual(r['scenario_proof']['distances'][0][0],2);self.assertEqual(r['scenario_proof']['distances'][1][0],6);self.assertEqual(r['route']['worst_time'],6)
    def test_false_scenario_ledgers(self):
        s=self.s();r=solve(s)
        for change in ('none','low','bool','floatindex','missing','sink'):
            p=copy.deepcopy(r)
            if change=='none':p['scenario_proof']['distances'][0][0]=None
            if change=='low':p['scenario_proof']['distances'][0][0]=0
            if change=='bool':p['scenario_proof']['distances'][0][-1]=False
            if change=='floatindex':p['scenario_proof']['states'][1]['incoming'][1]=0.0
            if change=='missing':p['scenario_proof']['distances'].pop()
            if change=='sink':p['scenario_proof']['distances'][0][-1]=1
            with self.assertRaises(Invalid):check(s,p)
    def test_false_incumbent(self):
        s=self.s();r=solve(s)
        for value in (None,{},dict(r['incumbent'],worst_time=0)):
            p=copy.deepcopy(r);p['incumbent']=value
            with self.assertRaises((Invalid,KeyError)):check(s,p)
        with patch('method.incumbent',return_value=None):
            with self.assertRaises(Invalid):solve(s)
    def test_audit_before_pruning(self):
        s=self.s()
        with patch('method.scenario_check',side_effect=RuntimeError('audit')),patch('method.incumbent') as inc:
            with self.assertRaises(RuntimeError):solve(s)
            inc.assert_not_called()
        with patch('method.scenario_reverse',return_value=[[None]*7]*2):
            with self.assertRaises(Invalid):solve(s)
    def test_early_no_new_work(self):
        s=self.s();s['budget']=0;s['graph']['a']=[edge('g',[1,1],1)];r=solve(s);check(s,r);self.assertEqual(r['certificate']['reason'],'budget_infeasible')
        for k in ('scenario_reverse_inspections','incumbent_inspections','objective_bound_pruned'):self.assertEqual(r['counters'][k],0)
        s['graph']['a']=[edge('b',[1,1],0)];s['graph']['b']=[];r=solve(s);check(s,r);self.assertEqual(r['certificate']['reason'],'no_allowed_turn_path')
    def test_identity_zero_incumbent(self):
        s=self.s();s['goal']='a';r=solve(s);check(s,r);self.assertEqual(r['incumbent']['worst_time'],0);self.assertEqual(r['route']['edges'],[])
    def test_feasible_none_contradiction(self):
        import heapq
        s=self.s();actual=heapq.heappop
        def stale(q):
            value=actual(q)
            return (value[0],value[1],value[2],(99,99),*value[4:]) if len(value)==9 else value
        with patch('method.heapq.heappop',side_effect=stale):
            with self.assertRaises(Invalid):solve(s)
