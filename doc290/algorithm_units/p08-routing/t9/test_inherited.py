import unittest,copy,sys,types
from method import solve
from model import Invalid,witness,COST_MAX,load_bytes
from proof import check
from fixtures import edge,oracle
class Development(unittest.TestCase):
    def s(self):return {'graph':{'a':[edge('b',[1,5],1)],'b':[edge('c',[1,1],1),edge('g',[5,1],1)],'c':[edge('b',[1,1],1)],'g':[]},'start':'a','goal':'g','budget':4,'forbidden':[[['a',0],['b',1]]],'penalties':[{'incoming':['c',0],'outgoing':['b',1],'delay':2}]}
    def test_repeated_vertex_turn_delay_budget(self):
        s=self.s();r=solve(s);self.assertEqual(r['route']['path'],['a','b','c','b','g']);self.assertEqual(r['route']['scenario_totals'],[10,10]);self.assertEqual(r['route']['exposure'],4);self.assertEqual(r['route']['turn_penalty'],2);self.assertEqual(oracle(s),10);check(s,r)
        s['budget']=3;self.assertIsNone(solve(s)['route']);self.assertIsNone(oracle(s))
    def test_parallel_zero_asymmetry_identity(self):
        s={'graph':{'a':[edge('g',[5,5],0),edge('g',[1,1],1),edge('a',[0,0],0)],'g':[edge('a',[3,3],2)]},'start':'a','goal':'g','budget':1,'forbidden':[],'penalties':[]};r=solve(s);self.assertEqual(r['route']['edges'][0]['edge_index'],1);self.assertEqual(oracle(s),1);self.assertEqual(solve(s),r)
        s['goal']='a';self.assertEqual(solve(s)['route']['worst_time'],0)
    def test_false_full_state_and_witness(self):
        s=self.s();r=solve(s)
        for field,value in (('start_minimum',0),('start_minimum',True),('distances',[0]*len(r['proof']['distances'])),('states',[])):
            p=copy.deepcopy(r);p['proof'][field]=value
            with self.assertRaises(Invalid):check(s,p)
        p=copy.deepcopy(r);p['route']['edges'][0]['edge_index']=True
        with self.assertRaises(Invalid):witness(s,p['route'])
    def test_caps_json_audit_exception(self):
        for c in (True,1.0,COST_MAX+1):
            s=self.s();s['graph']['a'][0]['exposure']=c
            with self.assertRaises(Invalid):solve(s)
        for b in (b'{"x":1,"x":2}',b'{"x":NaN}',b'['*11+b'0'+b']'*11):
            with self.assertRaises(Invalid):load_bytes(b)
        from unittest.mock import patch
        with patch('method.original_t7_proof.check',side_effect=RuntimeError('audit')):
            with self.assertRaises(RuntimeError):solve(self.s())
    def test_loaded_transitive_helper(self):
        from core import gate,ROOT
        from unittest.mock import patch
        from pathlib import Path
        with patch.dict(sys.modules,{'verify':types.SimpleNamespace(__file__='/tmp/fake.py')}):
            with self.assertRaises(Invalid):gate()
        helper=(ROOT/'../../p08-field-planning/f3/verify.py').resolve();original=Path.read_bytes
        def changed(p):return b'changed' if p.resolve()==helper else original(p)
        with patch.object(Path,'read_bytes',changed):
            with self.assertRaises(Invalid):gate()
