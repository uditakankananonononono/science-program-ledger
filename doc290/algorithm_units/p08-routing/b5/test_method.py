import unittest
from method import solve
from fixtures import oracle,edge
from model import Invalid,witness
from proof import distances,check
class Development(unittest.TestCase):
    def s(self):return {'graph':{'s':[edge('a',[1,5],1),edge('g',[8,8],0)],'a':[edge('g',[5,1],2),edge('a',[0,0],0)],'g':[]},'start':'s','goal':'g','budget':3}
    def test_equal_overshoot_correlation(self):
        s=self.s();r=solve(s);self.assertEqual(r['route']['worst_time'],6);self.assertEqual(r['route']['exposure'],3);self.assertEqual(oracle(s),6);check(s,r)
        s['budget']=2;r=solve(s);self.assertEqual(r['route']['worst_time'],8);self.assertEqual(oracle(s),8);self.assertGreater(r['counters']['feasibility_pruned'],0)
    def test_unreachable_budgetloss_identity(self):
        s={'graph':{'s':[edge('g',[1,1],2)],'g':[]},'start':'s','goal':'g','budget':1};r=solve(s);self.assertIsNone(r['route']);self.assertEqual(r['proof']['start_minimum'],2);self.assertIsNone(oracle(s))
        s['graph']['s']=[];s['graph']['g']=[edge('g',[0,0],0)];r=solve(s);self.assertIsNone(r['proof']['start_minimum'])
        s['goal']='s';self.assertEqual(solve(s)['route']['worst_time'],0)
    def test_parallel_asymmetric_types_index(self):
        s={'graph':{'s':[edge('g',[4,4],0),edge('g',[1,1],3)],'g':[edge('s',[1,1],7)]},'start':'s','goal':'g','budget':3};r=solve(s);self.assertEqual(r['route']['edges'][0]['edge_index'],1);self.assertEqual(r['proof']['reverse_exposure'],{'s':0,'g':0});self.assertEqual(solve(s),r)
        r['route']['exposure']=0
        with self.assertRaises(Invalid):witness(s,r['route'])
        for v in (True,1.0,-1,2**53):
            s=self.s();s['budget']=v
            with self.assertRaises(Invalid):solve(s)
    def test_false_ledger(self):
        import copy
        s=self.s();r=solve(s)
        for field,value in (('start_minimum',True),('start_minimum',1),('reverse_exposure',{'s':0,'a':0,'g':0}),('reverse_exposure',{'s':3,'g':0}),('reverse_exposure',{'s':3,'a':True,'g':0})):
            rr=copy.deepcopy(r);rr['proof'][field]=value
            with self.assertRaises(Invalid):check(s,rr)
