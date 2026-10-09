import unittest,copy
from method import solve,p3
from model import Invalid,witness

def e(t,ss):return {'target':t,'time':1,'exposure':0,'scenario_times':ss}
class Development(unittest.TestCase):
    def s(self):return {'graph':{'s':[e('g',[2,3]),e('g',[4,5]),e('s',[0,0])],'g':[]},'start':'s','goal':'g'}
    def test_equality_counters_parallel_zero_identity(self):
        r=solve(self.s());self.assertTrue(r['certificate']['early_exit']);self.assertEqual(r['certificate']['start_distances'],[2,3]);self.assertEqual(r['route']['worst_time'],3)
        for k in ('candidate_edges','labels_inserted','pops','max_live_queue'):self.assertEqual(r['counters'][k],0)
        self.assertGreater(r['counters']['reverse_relaxations'],0);self.assertGreater(r['counters']['incumbent_relaxations'],0)
        s=self.s();s['goal']='s';self.assertEqual(solve(s)['route']['worst_time'],0)
    def test_different_minima_suffix_equality(self):
        s={'graph':{'s':[e('g',[2,5]),e('g',[3,4])],'g':[]},'start':'s','goal':'g'};r=solve(s);self.assertFalse(r['certificate']['early_exit']);self.assertEqual(r['certificate']['start_distances'],[2,4]);self.assertEqual(r['route']['worst_time'],4)
        s={'graph':{'s':[e('g',[1,3]),e('g',[3,1])],'g':[]},'start':'s','goal':'g'};r=solve(s);self.assertFalse(r['certificate']['early_exit']);self.assertEqual(r['certificate']['lower_bound'],1);self.assertEqual(r['route']['worst_time'],3)
    def test_full_branch_matches_p3(self):
        s={'graph':{'s':[e('a',[0,8]),e('a',[4,4])],'a':[e('g',[0,0])],'g':[]},'start':'s','goal':'g'};r=solve(s);p=p3.solve(s);self.assertFalse(r['certificate']['early_exit']);self.assertEqual({k:r[k] for k in p},p)
    def test_unreachable_invalid_bound_incumbent_exceptions(self):
        from unittest.mock import patch
        s={'graph':{'s':[e('s',[0,0])],'g':[]},'start':'s','goal':'g'};self.assertIsNone(solve(s)['route'])
        for ds in ([{'s':None},{'s':2}],[{'s':9},{'s':9}],[{'s':-1},{'s':3}]):
            with patch('method.reverse',return_value=ds):
                with self.assertRaises(Invalid):solve(self.s())
        with patch('method.reverse',return_value=[{'s':0},{'s':None}]):
            with self.assertRaises(Invalid):solve(s)
        with patch('method.incumbent',return_value={'path':[],'edges':[],'scenario_totals':[0,0],'worst_time':0}):
            with self.assertRaises(Invalid):solve(self.s())
        with patch('method.reverse',side_effect=RuntimeError('fault')):
            with self.assertRaises(RuntimeError):solve(self.s())
