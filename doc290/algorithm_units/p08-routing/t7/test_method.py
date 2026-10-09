import unittest,copy
from method import solve,t6
from model import Invalid
from proof import check
from fixtures import edge,oracle
class Development(unittest.TestCase):
    def s(self):return {'graph':{'a':[edge('b',[1,5],1)],'b':[edge('c',[1,1],1),edge('g',[5,1],1)],'c':[edge('b',[1,1],1)],'g':[]},'start':'a','goal':'g','budget':4,'forbidden':[[['a',0],['b',1]]],'penalties':[{'incoming':['c',0],'outgoing':['b',1],'delay':2}]}
    def test_feasible_fullbranch_repeatvertex(self):
        s=self.s();r=solve(s);p=t6.solve(s);self.assertEqual({k:r[k] for k in p},p);self.assertEqual(oracle(s),10);self.assertEqual(r['route']['path'],['a','b','c','b','g']);check(s,r)
        s['goal']='a';self.assertEqual(solve(s)['route']['worst_time'],0)
    def test_early_classes_counters(self):
        s=self.s();s['budget']=3;r=solve(s);self.assertEqual(r['certificate']['reason'],'budget_infeasible');self.assertIsNone(oracle(s));check(s,r)
        for k in ('candidate_edges','forbidden_skipped','feasibility_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue'):self.assertEqual(r['counters'][k],0)
        s['graph']['c']=[];s['penalties']=[];r=solve(s);self.assertEqual(r['certificate']['reason'],'no_allowed_turn_path');check(s,r)
    def test_exception_falseproof_and_impossible_none(self):
        from unittest.mock import patch
        with patch('method.proof_check',side_effect=RuntimeError('audit')):
            with self.assertRaises(RuntimeError):solve(self.s())
        s=self.s();s['budget']=3
        with patch('method.reverse',return_value=[None]*6):
            with self.assertRaises(Invalid):solve(s)
        import heapq
        original=heapq.heappop
        def stale(q):
            r=original(q);return (r[0],r[1],r[2],(99,99),*r[4:])
        with patch('method.reverse',return_value=[4,3,2,0,1,0]),patch('method.heapq.heappop',side_effect=stale):
            with self.assertRaises(Invalid):solve(self.s())
    def test_counter_budget_reason_mutations(self):
        s=self.s();s['budget']=3;r=solve(s)
        for k in ('candidate_edges','forbidden_skipped','feasibility_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue'):
            rr=copy.deepcopy(r);rr['counters'][k]=1
            with self.assertRaises(Invalid):check(s,rr)
        for k,v in (('early_exit',False),('budget',True),('reason','feasible_search')):
            rr=copy.deepcopy(r);rr['certificate'][k]=v
            with self.assertRaises(Invalid):check(s,rr)
