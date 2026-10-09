import unittest,copy
from certificate import check,b3,load_bytes,Invalid
class Development(unittest.TestCase):
    def s(self):return {'graph':{'a':[{'target':'g','time':1,'exposure':2,'scenario_times':[2,4]}],'g':[{'target':'a','time':1,'exposure':0,'scenario_times':[1,1]}],'x':[{'target':'x','time':0,'exposure':0,'scenario_times':[0,0]}]},'start':'a','goal':'g','budget':2,'route':{'path':['a','g'],'edges':[{'source':'a','edge_index':0,'target':'g'}],'exposure':2,'scenario_totals':[2,4],'worst_time':4},'weights':[0,1],'multiplier':'1/2','potential':[0,5,'-1/2']}
    def test_algebra_all_edges(self):
        r=check(self.s());self.assertEqual(r['status'],'CERTIFIED_JOINT');self.assertEqual(r['budget_charge'],'1/1');self.assertEqual(r['lower_bound'],'4/1');self.assertEqual(len(r['edge_ledger']),3);self.assertEqual(r['edge_ledger'][1]['slack'],'6/1')
    def test_grammar(self):
        for w in ([True,0],[1.0,0],['2/4','1/2'],[-1,2],[1,1],[1]):
            s=self.s();s['weights']=w;self.assertEqual(check(s)['status'],'INVALID')
        for x in (True,1.0,'2/4',-1,b3.MAX+1):
            s=self.s();s['multiplier']=x;self.assertEqual(check(s)['status'],'INVALID')
    def test_feasibility_before_gap(self):
        s=self.s();s['potential']=[0,0,0];s['graph']['x'][0]['target']='g';s['potential'][2]=-1;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['potential']=[0,0,0];self.assertEqual(check(s)['status'],'UNAVAILABLE')
    def test_model_first_identity(self):
        for field,value in (('budget',True),('budget',-1)):
            s=self.s();s['route']=None;s[field]=value;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['route']=None;s['graph']['g'][0]['scenario_times']=[];self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s.update(graph={'a':[]},goal='a',route=None);self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s.update(goal='x',start='x',budget=0,route={'path':['x'],'edges':[],'exposure':0,'scenario_totals':[0,0],'worst_time':0},potential=[0,0,0]);self.assertEqual(check(s)['status'],'CERTIFIED_JOINT')
    def test_primal_caps(self):
        for field,value in (('worst_time',True),('exposure',True),('exposure',3),('scenario_totals',[4,2])):
            s=self.s();s['route'][field]=value;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['route']['edges'][0]['edge_index']=True;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['budget']=1;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['multiplier']=b3.MAX;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['budget']=b3.MAX;self.assertEqual(check(s)['status'],'UNAVAILABLE')
    def test_disagreement_and_json(self):
        from compare import agreed
        self.assertFalse(agreed('CERTIFIED_JOINT',{'status':'INVALID'}))
        for data in (b'{"x":1,"x":2}',b'{"x":NaN}',b'['*11+b'0'+b']'*11,b' '*131073):
            with self.assertRaises(Invalid):load_bytes(data)
if __name__=='__main__':unittest.main()
