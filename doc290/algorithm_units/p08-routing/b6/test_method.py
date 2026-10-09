import unittest,copy
from method import solve,b5
from model import Invalid
from proof import check
from fixtures import oracle,edge
class Development(unittest.TestCase):
    def s(self):return {'graph':{'s':[edge('a',[1,5],1)],'a':[edge('g',[5,1],2),edge('a',[0,0],0)],'g':[]},'start':'s','goal':'g','budget':3}
    def test_budgetloss_graphunreachable(self):
        s=self.s();s['budget']=2;r=solve(s);self.assertEqual(r['certificate']['reason'],'budget_infeasible');self.assertIsNone(oracle(s));check(s,r)
        for k in ('candidate_edges','labels_inserted','pops','feasibility_pruned','dominance_pruned','stale_pops','max_live_queue'):self.assertEqual(r['counters'][k],0)
        s['graph']['a']=[];r=solve(s);self.assertEqual(r['certificate']['reason'],'graph_unreachable');check(s,r)
    def test_equal_fullbranch_zero_identity(self):
        s=self.s();r=solve(s);p=b5.solve(s);self.assertEqual({k:r[k] for k in p},p);self.assertEqual(r['route']['worst_time'],6);self.assertEqual(oracle(s),6);self.assertEqual(solve(s),r)
        s['goal']='s';r=solve(s);self.assertFalse(r['certificate']['early_exit']);self.assertEqual(r['route']['worst_time'],0)
    def test_audit_exception_and_injected_proof(self):
        from unittest.mock import patch
        with patch('method.reverse',return_value={'s':None,'a':None,'g':0}):
            with self.assertRaises(Invalid):solve(self.s())
        with patch('method.ledger_check',side_effect=RuntimeError('audit')):
            with self.assertRaises(RuntimeError):solve(self.s())
        import heapq
        original=heapq.heappop
        def stale(q):
            result=original(q);return (result[0],result[1],(99,99),result[3],result[4])
        with patch('method.heapq.heappop',side_effect=stale),patch('method.reverse',return_value={'s':3,'a':2,'g':0}):
            with self.assertRaises(Invalid):solve(self.s())
        s=self.s();r=solve(s)
        for field,value in (('reason','graph_unreachable'),('budget',True),('early_exit',True)):
            rr=copy.deepcopy(r);rr['certificate'][field]=value
            with self.assertRaises(Invalid):check(s,rr)
    def test_early_counter_metadata_mutations(self):
        s=self.s();s['budget']=2;r=solve(s)
        for k in ('candidate_edges','labels_inserted','pops','feasibility_pruned','dominance_pruned','stale_pops','max_live_queue'):
            rr=copy.deepcopy(r);rr['counters'][k]=1
            with self.assertRaises(Invalid):check(s,rr)
