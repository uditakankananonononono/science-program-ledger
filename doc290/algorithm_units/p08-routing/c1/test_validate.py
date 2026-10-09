import unittest,copy
from validate import validate
class Development(unittest.TestCase):
    def chain(self):
        def e(t):return {'target':t,'time':1,'exposure':1,'scenario_times':[1]}
        return {'original':{'a':[e('b')],'b':[e('a'),e('c')],'c':[e('b')]},'compressed':{'a':[e('c')],'c':[e('a')]},'witnesses':{'a':[['a','b','c']],'c':[['c','b','a']]},'start':'a','goal':'c','budget':2,'forbidden':[],'penalties':[],'route':None}
    def proper(self):
        s=self.chain()
        for es in s['compressed'].values():es[0].update(time=2,exposure=2,scenario_times=[2])
        return s
    def test_walk_partition_counterexample(self):
        s=self.proper();s['compressed']['a'][0]['target']='a';s['compressed']['c'][0]['target']='c';s['witnesses']={'a':[['a','b','a']],'c':[['c','b','c']]};self.assertEqual(validate(s)['status'],'INVALID')
    def test_null_after_all_validation(self):
        self.assertEqual(validate(self.proper())['status'],'UNAVAILABLE')
        for change in ('interior','turn','cost','coverage'):
            s=self.proper()
            if change=='interior':s['start']='b'
            if change=='turn':s['penalties']=[1]
            if change=='cost':s['compressed']['a'][0]['time']=1
            if change=='coverage':s['witnesses']['c']=[]
            self.assertEqual(validate(s)['status'],'INVALID')
    def test_valid_literal_route(self):
        s=self.proper();s['route']={'path':['a','c'],'edges':[{'source':'a','edge_index':0,'target':'c'}],'time':2,'exposure':2,'scenario_totals':[2],'worst_time':2}
        r=validate(s);self.assertEqual(r['expanded_path'],['a','b','c']);self.assertEqual(r['original_edges'],[{'source':'a','edge_index':0,'target':'b'},{'source':'b','edge_index':1,'target':'c'}])
        s['route']['edges'][0]['edge_index']=-1;self.assertEqual(validate(s)['status'],'INVALID')
    def test_integer_bool_and_float(self):
        for v in (True,1.0,-1,2**53):
            s=self.proper();s['original']['a'][0]['time']=v;self.assertEqual(validate(s)['status'],'INVALID')
    def test_identity_isolate(self):
        s={'original':{'a':[]},'compressed':{'a':[]},'witnesses':{'a':[]},'start':'a','goal':'a','budget':0,'forbidden':[],'penalties':[],'route':{'path':['a'],'edges':[],'time':0,'exposure':0,'scenario_totals':[],'worst_time':0}}
        self.assertEqual(validate(s)['status'],'FEASIBLE_WITNESS')
    def test_comparator_disagreement(self):
        from compare import agreed
        self.assertFalse(agreed('FEASIBLE_WITNESS',{'status':'INVALID'}))
if __name__=='__main__':unittest.main()
