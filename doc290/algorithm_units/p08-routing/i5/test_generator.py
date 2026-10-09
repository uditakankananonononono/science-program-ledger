import unittest,copy
from unittest.mock import patch
from fractions import Fraction as F
from generator import generate,envelope,paths,weights
from proof import verify,parametric
from core import devstatement
from model import Failure
class Development(unittest.TestCase):
    def test_dev_success_verify(self):
        s=devstatement();r=generate(s);verify(s,r);self.assertEqual(r['status'],'CERTIFIED_INTEGRATED');self.assertEqual(len(r['weights']),3)
    def test_charged_envelope_ray_plateau(self):
        # Synthetic raw paths, outside fixed20: same/duplicate/zero slopes and plateau.
        raw=[{'scenario_totals':[0],'exposure':3},{'scenario_totals':[9],'exposure':1}]
        lines,points,lam,LB=envelope(raw,(F(1),),1);self.assertEqual(lam,F(9,2));self.assertEqual(LB,9);self.assertEqual(parametric(raw,(F(1),),1)[2:],(lam,LB))
        raw.append(copy.deepcopy(raw[1]));self.assertEqual(envelope(raw,(F(1),),1)[2:],(lam,LB))
        raw=[{'scenario_totals':[1],'exposure':0},{'scenario_totals':[2],'exposure':0}];self.assertEqual(envelope(raw,(F(1),),0)[2:],(F(0),F(1)))
    def test_schema_point_path_selection(self):
        s=devstatement();r=generate(s);changes=[]
        for key,v in (('gap','999/1'),('selected_weight',False),('selected_weight',0.0),('best_lower','999/1')):
            x=copy.deepcopy(r);x[key]=v;changes.append(x)
        x=copy.deepcopy(r);x['paths'][0]['exposure']=False;changes.append(x)
        x=copy.deepcopy(r);x['weights'][0]['index']=False;changes.append(x)
        x=copy.deepcopy(r);x['weights'][0]['points'][0]['lambda']='1/1';changes.append(x)
        x=copy.deepcopy(r);x['weights'][0]['lines'][0]['slope']=False;changes.append(x)
        x=copy.deepcopy(r);x['weights'][0]['selected_lambda']='1/1';changes.append(x)
        for x in changes:
            with self.assertRaises(Failure):verify(s,x)
    def test_schedule_no_generator_import(self):
        s=devstatement();r=generate(s)
        with patch('generator.weights',side_effect=RuntimeError('shared schedule')):verify(s,r)
    def test_model_domain_missing_invalid(self):
        s=devstatement();s['route']=None;r=generate(s);verify(s,r);self.assertEqual(r['status'],'UNAVAILABLE')
        s=devstatement();s['graph']['z']*=6;r=generate(s);verify(s,r);self.assertEqual(r['status'],'UNAVAILABLE_DOMAIN')
        s['budget']=True;self.assertEqual(generate(s)['status'],'INVALID')
    def test_no_subset_envelope_and_unique_arc_guard(self):
        # Actual model <=6-edge guard checked on admitted graphs. Synthetic 8state
        # complete DAG exceeds64 and demonstrates no prefixenvelope authority.
        G={str(k):[] for k in range(8)};states=[{}]*8;arcs=[]
        for a in range(8):
            for b in range(8):
                if a!=b:arcs.append({'source':a,'target':b,'edge':None,'delay':0})
        raw,overflow=paths(G,1,states,arcs);self.assertTrue(overflow);self.assertEqual(len(raw),65)
        with self.assertRaises(Failure):paths(G,1,states,arcs+[arcs[0]])
        s=devstatement()
        with patch('generator.paths',return_value=(raw,True)),patch('generator.envelope') as e:r=generate(s);self.assertEqual(r['status'],'UNAVAILABLE_ENUMERATION');e.assert_not_called()
    def test_parent_independent_and_domain(self):
        from model import i3
        s=devstatement();s['graph']['u']=[{'target':'q','time':1,'exposure':i3.b3.MAX,'scenario_times':[i3.b3.MAX]*2}];s['graph']['x']=[{'target':'u','time':1,'exposure':0,'scenario_times':[0,0]}]
        r=generate(s);verify(s,r)
    def test_forbidden_turn_revisit_and_allstate_clamp(self):
        from model import i3
        e=lambda t,ss:{'target':t,'time':1,'exposure':0,'scenario_times':ss}
        s={'graph':{'a':[e('b',[1,1])],'b':[e('c',[1,1]),e('g',[1,1])],'c':[e('b',[1,1])],'g':[]},'start':'a','goal':'g','budget':0,'forbidden':[[['a',0],['b',1]]],'penalties':[],'route':{'path':['a','b','c','b','g'],'edges':[{'source':a,'edge_index':j,'target':b} for a,j,b in [('a',0,'b'),('b',0,'c'),('c',0,'b'),('b',1,'g')]],'scenario_totals':[4,4],'worst_time':4,'exposure':0,'turn_penalty':0}}
        r=generate(s);verify(s,r);self.assertEqual(r['status'],'CERTIFIED_INTEGRATED')
        s['penalties']=[{'incoming':['c',0],'outgoing':['b',1],'delay':2}];s['route']['scenario_totals']=[6,6];s['route']['worst_time']=6;s['route']['turn_penalty']=2;r=generate(s);verify(s,r);self.assertEqual(r['best_lower'],'6/1')
    def test_selected_domain_no_smaller_rescue(self):
        from generator import old
        from model import Domain
        s=devstatement()
        with patch('generator.text',side_effect=Domain('selected cap')),patch.object(old,'reverse') as reverse:
            r=generate(s);self.assertEqual(r['status'],'UNAVAILABLE_DOMAIN');self.assertEqual(len(r['weights']),3);reverse.assert_not_called()
