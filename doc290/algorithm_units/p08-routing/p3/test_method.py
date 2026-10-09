import unittest,copy
from model import model,witness,Invalid,EDGE_MAX
from method import solve,reverse,incumbent,prunable
from fixtures import exhaustive,edge
class Development(unittest.TestCase):
    def s(self):return {'graph':{'s':[edge('a',[1,8]),edge('a',[7,1]),edge('g',[20,20])],'a':[edge('g',[3,0]),edge('a',[0,0])],'g':[edge('s',[1,1])]},'start':'s','goal':'g'}
    def test_directed_indices_and_bound(self):
        s=self.s();r=solve(s);self.assertEqual(r['route']['worst_time'],8);self.assertEqual(r['route']['edges'][0]['edge_index'],0);self.assertEqual(exhaustive(s),8);self.assertGreater(r['counters']['lb_pruned'],0);self.assertEqual(solve(s),r)
        ds=reverse(s['graph'],'g',2,{'reverse_relaxations':0});self.assertEqual(ds[0]['s'],4);self.assertEqual(ds[1]['s'],1);self.assertEqual(r['incumbent']['worst_time'],8)
    def test_strict_equal_and_large_intermediate(self):
        ds=[{'v':4},{'v':1}];self.assertFalse(prunable((0,7),'v',ds,8));self.assertTrue(prunable((1,8),'v',ds,8));self.assertTrue(prunable((0,0),'v',[{'v':None}],8));self.assertTrue(prunable((EDGE_MAX*32,EDGE_MAX*32),'v',ds,8))
    def test_no_shared_minima_and_zero_cycles(self):
        s={'graph':{'s':[edge('g',[1,9]),edge('g',[9,1]),edge('s',[0,0])],'g':[]},'start':'s','goal':'g'};r=solve(s);self.assertEqual(r['route']['worst_time'],9);self.assertEqual(exhaustive(s),9);self.assertEqual(len(r['route']['path']),2)
        s.update(start='g');self.assertEqual(solve(s)['route']['worst_time'],0)
    def test_false_incumbent_and_no_exception_rescue(self):
        from unittest.mock import patch
        fake={'path':['s','g'],'edges':[{'source':'s','edge_index':2,'target':'g'}],'scenario_totals':[0,0],'worst_time':0}
        with patch('method.incumbent',return_value=fake):
            with self.assertRaises(Invalid):solve(self.s())
        with patch('method.reverse',side_effect=RuntimeError('invariant')):
            with self.assertRaises(RuntimeError):solve(self.s())
    def test_model_types_caps_unreachable(self):
        for value in (True,1.0,-1,EDGE_MAX+1):
            s=self.s();s['graph']['s'][0]['scenario_times'][0]=value
            with self.assertRaises(Invalid):solve(s)
        s={'graph':{'s':[]},'start':'s','goal':'s'}
        with self.assertRaises(Invalid):solve(s)
        s={'graph':{'s':[edge('s',[0,0])],'g':[]},'start':'s','goal':'g'};self.assertIsNone(solve(s)['route'])
    def test_oracle_disagreement_control(self):
        s=self.s();r=solve(s)['route'];w=witness(s,r);self.assertNotEqual(w['worst_time'],7)
        r=copy.deepcopy(r);r['worst_time']=True
        with self.assertRaises(Invalid):witness(s,r)
if __name__=='__main__':unittest.main()
