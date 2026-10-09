import unittest,copy
from model import witness,Invalid
from method import solve,beam,p3

def e(t,ss):return {'target':t,'time':1,'exposure':0,'scenario_times':ss}
class Development(unittest.TestCase):
    def s(self):return {'graph':{'s':[e('a',[0,9]),e('a',[4,4])],'a':[e('g',[0,0])],'g':[]},'start':'s','goal':'g'}
    def exhaustive(self,s):
        costs=[]
        def walk(v,seen,ss):
            if v==s['goal']:costs.append(max(ss));return
            for edge in s['graph'][v]:
                if edge['target'] not in seen:walk(edge['target'],seen|{edge['target']},[x+y for x,y in zip(ss,edge['scenario_times'])])
        walk(s['start'],{s['start']},[0,0]);return min(costs) if costs else None
    def test_strict_improve_counts(self):
        r=solve(self.s());self.assertEqual(r['route']['worst_time'],4);self.assertEqual(r['beam_info']['old_worst'],9);self.assertEqual(r['beam_info']['beam_worst'],4);self.assertEqual(r['beam_info']['selected_source'],'beam');self.assertEqual(self.exhaustive(self.s()),4);self.assertEqual(solve(self.s()),r)
    def test_incomplete_beam_loses_optimum_exact_recovers(self):
        s={'graph':{'s':[e('a',[0,6]),e('a',[1,5]),e('a',[10,0])],'a':[e('g',[0,20])],'g':[]},'start':'s','goal':'g'};r=solve(s);self.assertEqual(r['beam_info']['beam_worst'],25);self.assertEqual(r['route']['worst_time'],20);self.assertEqual(self.exhaustive(s),20);self.assertEqual(r['beam_info']['old_worst'],26)
    def test_tie_parallel_zero_identity(self):
        s={'graph':{'s':[e('g',[1,5]),e('g',[5,1]),e('s',[0,0])],'g':[]},'start':'s','goal':'g'};r=solve(s);self.assertEqual(r['beam_info']['selected_source'],'old');self.assertEqual(r['incumbent'],p3.solve(s)['incumbent']);self.assertEqual(r['route']['edges'][0]['edge_index'],0)
        s['goal']='s';r=solve(s);self.assertEqual(r['route']['worst_time'],0);self.assertEqual(r['beam_info']['beam_worst'],0)
    def test_absence_not_unreachable_exceptions(self):
        from unittest.mock import patch
        with patch('method.beam',return_value=(None,{'beam_expansions':0,'beam_goal_candidates':0,'beam_kept':0,'beam_depths':0})):self.assertEqual(solve(self.s())['route']['worst_time'],4)
        with patch('method.beam',side_effect=RuntimeError('beamfault')):
            with self.assertRaises(RuntimeError):solve(self.s())
        fake={'path':['s','g'],'edges':[],'scenario_totals':[0,0],'worst_time':0}
        with patch('method.beam',return_value=(fake,{})):
            with self.assertRaises(Invalid):solve(self.s())
        s={'graph':{'s':[e('s',[0,0])],'g':[]},'start':'s','goal':'g'};self.assertIsNone(solve(s)['route'])
    def test_proposal_recompute_and_depthbound(self):
        s=self.s();b,c=beam(s,s['graph'],2);self.assertEqual(witness(s,b)['worst_time'],4);self.assertEqual(c['beam_depths'],len(s['graph'])-1);self.assertLessEqual(c['beam_expansions'],2*sum(len(v) for v in s['graph'].values())*(len(s['graph'])-1))
        b['worst_time']=0
        with self.assertRaises(Invalid):witness(s,b)
