import unittest,copy
from certificate import check,MAX,Invalid,load_bytes
from oracle import minimum

def e(t,x):return {'target':t,'time':1,'exposure':x,'scenario_times':[1,1]}
class Development(unittest.TestCase):
    def s(self):return {'graph':{'s':[e('g',2)],'g':[e('s',1)],'x':[e('x',0)]},'start':'s','goal':'g','budget':1,'forbidden':[],'penalties':[],'distances':[2,2,0,None,0]}
    def test_all_goaloutgoing_unused_and_oracle(self):
        r=check(self.s());self.assertEqual(r['status'],'CERTIFIED_BUDGET_INFEASIBLE');self.assertEqual(minimum(self.s()),2);self.assertEqual(len(r['states']),5);self.assertEqual(len(r['exposure_arcs']),5)
    def test_model_before_missing_and_json(self):
        s=self.s();s['distances']=None;s['budget']=True;self.assertEqual(check(s)['status'],'INVALID')
        for vectors in ([],[1]):
            s=self.s();s['distances']=None;s['graph']['s'][0]['scenario_times']=vectors;self.assertEqual(check(s)['status'],'INVALID')
        s={'graph':{'s':[]},'start':'s','goal':'s','budget':0,'forbidden':[],'penalties':[],'distances':None};self.assertEqual(check(s)['status'],'INVALID')
        for data in (b'{"x":1,"x":2}',b'{"x":NaN}',b'['*11+b'0'+b']'*11,b' '*131073):
            with self.assertRaises(Invalid):load_bytes(data)
    def test_false_none_types_and_expanded_cap(self):
        for v in (None,True,-1,MAX*129+1):
            s=self.s();s['distances'][0]=v;self.assertEqual(check(s)['status'],'INVALID')
        # 2 original edges produce bound 2*MAX, valid exposure cap despite >MAX distance
        s={'graph':{'s':[e('a',MAX)],'a':[e('g',MAX)],'g':[]},'start':'s','goal':'g','budget':MAX,'forbidden':[],'penalties':[],'distances':[2*MAX,0,MAX,0]};self.assertEqual(check(s)['status'],'CERTIFIED_BUDGET_INFEASIBLE')
    def test_revisit_distinct_incoming_parallel_zero(self):
        s={'graph':{'a':[e('b',1)],'b':[e('c',1),e('g',1)],'c':[e('b',1)],'g':[]},'start':'a','goal':'g','budget':3,'forbidden':[[['a',0],['b',1]]],'penalties':[],'distances':[4,3,2,0,1,0]};self.assertEqual(minimum(s),4);self.assertEqual(check(s)['status'],'CERTIFIED_BUDGET_INFEASIBLE')
        s={'graph':{'a':[e('g',0),e('g',2)],'g':[]},'start':'a','goal':'g','budget':0,'forbidden':[],'penalties':[],'distances':[0,0,0,0]};self.assertEqual(check(s)['status'],'UNAVAILABLE');self.assertEqual(minimum(s),0)
    def test_scalar_delay_not_exposure_and_identity(self):
        s={'graph':{'s':[e('a',1)],'a':[e('g',1)],'g':[]},'start':'s','goal':'g','budget':2,'forbidden':[],'penalties':[{'incoming':['s',0],'outgoing':['a',0],'delay':17}],'distances':[2,0,1,0]};self.assertEqual(check(s)['status'],'UNAVAILABLE');self.assertEqual(minimum(s),2)
        s=self.s();s['goal']='s';s['budget']=0;s['distances']=[0,0,1,None,0];self.assertEqual(check(s)['status'],'UNAVAILABLE')
    def test_disagreement(self):
        from compare import agreed
        self.assertFalse(agreed('CERTIFIED_NO_TURN_PATH',{'status':'INVALID'}))
    def test_transitive_verify_identity(self):
        from compare import gate,ROOT
        import sys,types
        from unittest.mock import patch
        helper=(ROOT/'../../p08-field-planning/f3/verify.py').resolve()
        fake=types.SimpleNamespace(__file__='/tmp/unpinned-verify.py')
        with patch.dict(sys.modules,{'verify':fake}):
            with self.assertRaises(Invalid):gate()
        original=type(helper).read_bytes
        def changed(path):return b'modified helper' if path.resolve()==helper else original(path)
        with patch.object(type(helper),'read_bytes',changed):
            with self.assertRaises(Invalid):gate()
if __name__=='__main__':unittest.main()
