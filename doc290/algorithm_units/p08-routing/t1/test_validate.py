import unittest,copy
from validate import validate,helper
class Development(unittest.TestCase):
    def s(self):return {'graph':{'a':[{'target':'b','time':1,'exposure':1,'scenario_times':[2,3]}],'b':[{'target':'c','time':1,'exposure':1,'scenario_times':[4,1]}],'c':[]},'start':'a','goal':'c','budget':2,'forbidden':[],'penalties':[{'incoming':['a',0],'outgoing':['b',0],'delay':5}],'route':{'path':['a','b','c'],'edges':[{'source':'a','edge_index':0,'target':'b'},{'source':'b','edge_index':0,'target':'c'}],'exposure':2,'scenario_totals':[11,9],'worst_time':11,'turn_penalty':5}}
    def test_literal_ledger_and_negative_index(self):
        s=self.s();r=validate(s);self.assertEqual(r['ledger'][0]['delay'],0);self.assertEqual(r['ledger'][1]['delay'],5)
        s['route']['edges'][0]['edge_index']=-1;self.assertEqual(validate(s)['status'],'INVALID')
    def test_rule_even_null_unused(self):
        s=self.s();s['route']=None;s['penalties'][0]['outgoing']=['c',0];self.assertEqual(validate(s)['status'],'INVALID')
        s=self.s();s['route']=None;self.assertEqual(validate(s)['status'],'UNAVAILABLE')
    def test_dimension_integer_and_cap(self):
        for change in ('erase','bool','float','sum'):
            s=self.s()
            if change=='erase':s['route']['scenario_totals']=[]
            if change=='bool':s['graph']['a'][0]['scenario_times'][0]=True
            if change=='float':s['penalties'][0]['delay']=5.0
            if change=='sum':s['penalties'][0]['delay']=2**53-1
            self.assertEqual(validate(s)['status'],'INVALID')
    def test_noedge_policy(self):
        s=self.s();s['graph']={'a':[]};s.update(start='a',goal='a',route=None,penalties=[]);self.assertEqual(validate(s)['status'],'INVALID')
        s=self.s();s['graph']['i']=[];s.update(start='i',goal='i',budget=0,route={'path':['i'],'edges':[],'exposure':0,'scenario_totals':[0,0],'worst_time':0,'turn_penalty':0});self.assertEqual(validate(s)['status'],'FEASIBLE_WITNESS')
    def test_forbidden_wins_and_duplicates(self):
        s=self.s();s['forbidden']=[[['a',0],['b',0]]];self.assertEqual(validate(s)['status'],'INVALID')
        s=self.s();s['penalties'].append(copy.deepcopy(s['penalties'][0]));self.assertEqual(validate(s)['status'],'INVALID')
    def test_disagreement(self):
        from compare import agreed
        self.assertFalse(agreed('FEASIBLE_WITNESS',{'status':'INVALID'}))
if __name__=='__main__':unittest.main()
