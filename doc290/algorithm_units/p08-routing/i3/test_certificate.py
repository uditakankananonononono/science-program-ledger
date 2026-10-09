import unittest,copy
from certificate import check,b3,load_bytes,Invalid
class Development(unittest.TestCase):
    def e(self,t,ss,x=0):return {'target':t,'time':1,'exposure':x,'scenario_times':ss}
    def s(self):return {'graph':{'a':[self.e('b',[2,4],1)],'b':[self.e('g',[4,2],1)],'g':[self.e('a',[1,1])],'x':[self.e('x',[0,0])]},'start':'a','goal':'g','budget':2,'route':{'path':['a','b','g'],'edges':[{'source':'a','edge_index':0,'target':'b'},{'source':'b','edge_index':0,'target':'g'}],'exposure':2,'scenario_totals':[7,7],'worst_time':7,'turn_penalty':1},'forbidden':[],'penalties':[{'incoming':['a',0],'outgoing':['b',0],'delay':1}],'weights':['1/2','1/2'],'multiplier':1,'potential':[0,4,9,0,-1,9]}
    def test_all_states_turn_algebra(self):
        r=check(self.s());self.assertEqual(r['status'],'CERTIFIED_INTEGRATED');self.assertEqual(r['budget_charge'],'2/1');self.assertEqual(r['lower_bound'],'7/1');self.assertEqual(len(r['states']),6);self.assertEqual(len(r['transition_ledger']),6)
    def test_forbidden_and_unreachable_sink(self):
        s=self.s();s['forbidden']=[[['a',0],['b',0]]];self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['graph']['x']=[self.e('g',[0,0])];self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['graph']['x']=[self.e('g',[0,0])];s['potential'][4]=9;self.assertEqual(check(s)['status'],'CERTIFIED_INTEGRATED')
    def test_grammar_and_primal(self):
        for w in ([True,0],[1.0,0],['2/4','1/2'],[-1,2],[1,1],[1]):
            s=self.s();s['weights']=w;self.assertEqual(check(s)['status'],'INVALID')
        for x in (True,1.0,'2/4',-1,b3.MAX+1):
            s=self.s();s['multiplier']=x;self.assertEqual(check(s)['status'],'INVALID')
        for field,value in (('worst_time',True),('exposure',True),('exposure',3),('scenario_totals',[6,6]),('turn_penalty',0)):
            s=self.s();s['route'][field]=value;self.assertEqual(check(s)['status'],'INVALID')
    def test_model_caps_first_identity(self):
        for value in (True,-1):
            s=self.s();s['route']=None;s['budget']=value;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['route']=None;s['graph']['g'][0]['scenario_times']=[];self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['graph']['b'][0]['time']=b3.MAX;s['route']=None;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['graph']['b'][0]['scenario_times']=[b3.MAX,0];self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['multiplier']=b3.MAX;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s.update(graph={'a':[]},goal='a',route=None,penalties=[]);self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s.update(start='x',goal='x',budget=0,penalties=[],route={'path':['x'],'edges':[],'exposure':0,'scenario_totals':[0,0],'worst_time':0,'turn_penalty':0},potential=[0,0,0,0,0,0]);self.assertEqual(check(s)['status'],'CERTIFIED_INTEGRATED')
    def test_feasibility_before_gap_and_revisit(self):
        s=self.s();s['potential']=[0,0,0,0,-1,0];self.assertEqual(check(s)['status'],'UNAVAILABLE')
        s=self.s();s['potential']=[0,0,0,0,-1,0];s['graph']['x']=[self.e('g',[0,0])];self.assertEqual(check(s)['status'],'INVALID')
        # Same vertex b visited with different incoming edges; explicit original witnesses.
        s={'graph':{'a':[self.e('b',[1,1])],'b':[self.e('c',[1,1]),self.e('g',[1,1])],'c':[self.e('b',[1,1])],'g':[]},'start':'a','goal':'g','budget':0,'forbidden':[[['a',0],['b',1]]],'penalties':[],'route':{'path':['a','b','c','b','g'],'edges':[{'source':a,'edge_index':i,'target':b} for a,i,b in [('a',0,'b'),('b',0,'c'),('c',0,'b'),('b',1,'g')]],'exposure':0,'scenario_totals':[4,4],'worst_time':4,'turn_penalty':0},'weights':[1,0],'multiplier':0,'potential':[0,1,2,4,3,4]}
        self.assertEqual(check(s)['status'],'CERTIFIED_INTEGRATED')
    def test_disagreement_and_json(self):
        from compare import agreed
        self.assertFalse(agreed('CERTIFIED_INTEGRATED',{'status':'INVALID'}))
        for data in (b'{"x":1,"x":2}',b'{"x":NaN}',b'['*11+b'0'+b']'*11,b' '*131073):
            with self.assertRaises(Invalid):load_bytes(data)
if __name__=='__main__':unittest.main()
