import unittest,copy
from certificate import model,check,MAX
class Development(unittest.TestCase):
    def s(self):return {'graph':{'a':[{'target':'g','time':2,'exposure':0,'scenario_times':[]}],'g':[{'target':'a','time':7,'exposure':0,'scenario_times':[]}]},'start':'a','goal':'g','forbidden':[],'penalties':[],'route':{'path':['a','g'],'edges':[{'source':'a','edge_index':0,'target':'g'}],'time':2,'turn_penalty':0},'potential':[0,2,0,2]}
    def test_full_literal_transitions_goal_outgoing(self):
        s=self.s();G,f,p,states,arcs=model(s);self.assertEqual([(a['source'],a['target'],a['cost']) for a in arcs],[(0,1,2),(1,2,7),(1,3,0),(2,1,2)]);self.assertEqual(check(s)['status'],'CERTIFIED_OPTIMAL')
    def test_unused_unreachable_state(self):
        s=self.s();s['graph']['x']=[{'target':'x','time':1,'exposure':0,'scenario_times':[]}];s['potential']=[0,2,0,-3,2];self.assertEqual(check(s)['status'],'CERTIFIED_OPTIMAL')
        s['potential'][3]=True;self.assertEqual(check(s)['status'],'INVALID')
    def test_feasibility_before_slack(self):
        s=self.s();s['potential']=[0,3,0,0];self.assertEqual(check(s)['status'],'INVALID')
        s['potential']=[0,0,0,0];self.assertEqual(check(s)['status'],'UNAVAILABLE')
    def test_types_caps_and_scenarios(self):
        for kind in ('routefloat','boolh','caph','scenario','costdelay'):
            s=self.s()
            if kind=='routefloat':s['route']['time']=2.0
            if kind=='boolh':s['potential'][1]=True
            if kind=='caph':s['potential'][1]=MAX+1
            if kind=='scenario':s['graph']['g'][0]['scenario_times']=[0]
            if kind=='costdelay':s['penalties']=[{'incoming':['a',0],'outgoing':['g',0],'delay':MAX}]
            self.assertEqual(check(s)['status'],'INVALID')
    def test_identity_and_no_first_turn(self):
        s=self.s();s.update(goal='a',route={'path':['a'],'edges':[],'time':0,'turn_penalty':0},potential=[0,0,0,0]);self.assertEqual(check(s)['status'],'CERTIFIED_OPTIMAL')
    def test_disagreement(self):
        from compare import agreed
        self.assertFalse(agreed('CERTIFIED_OPTIMAL',{'status':'INVALID'}))
if __name__=='__main__':unittest.main()
