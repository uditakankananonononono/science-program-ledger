import unittest,copy
from certificate import check,MAX
class Development(unittest.TestCase):
    def s(self):return {'graph':{'a':[{'target':'g','time':2,'exposure':1,'scenario_times':[]}],'g':[{'target':'a','time':1,'exposure':0,'scenario_times':[]}],'x':[{'target':'x','time':0,'exposure':0,'scenario_times':[]}]},'start':'a','goal':'g','budget':1,'route':{'path':['a','g'],'edges':[{'source':'a','edge_index':0,'target':'g'}],'time':2,'exposure':1},'multiplier':'1/2','potential':[0,'5/2','-3/2']}
    def test_all_edges_and_exact_algebra(self):
        r=check(self.s());self.assertEqual(r['status'],'CERTIFIED_OPTIMAL');self.assertEqual(r['lower_bound'],'2/1');self.assertEqual(len(r['edge_ledger']),3);self.assertEqual(r['budget_charge'],'1/2');self.assertEqual(r['edge_ledger'][1]['slack'],'7/2')
    def test_feasibility_before_slack(self):
        s=self.s();s['potential']=[0,3,0];self.assertEqual(check(s)['status'],'INVALID');s['potential']=[0,0,0];self.assertEqual(check(s)['status'],'UNAVAILABLE')
    def test_grammar_and_caps(self):
        for v in (True,1.0,'2/4','-0/1',-1,MAX+1):
            s=self.s();s['multiplier']=v;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['multiplier']=MAX;self.assertEqual(check(s)['status'],'INVALID')
    def test_model_first_optional_scenarios(self):
        s=self.s();s['multiplier']=None;s['graph']['g'][0]['scenario_times']=[0];self.assertEqual(check(s)['status'],'INVALID')
    def test_primal_index_budget_identity(self):
        s=self.s();s['route']['edges'][0]['edge_index']=-1;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['budget']=0;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s.update(goal='a',budget=0,route={'path':['a'],'edges':[],'time':0,'exposure':0},potential=[0,0,0]);self.assertEqual(check(s)['status'],'CERTIFIED_OPTIMAL')
    def test_disagreement(self):
        from compare import agreed
        self.assertFalse(agreed('CERTIFIED_OPTIMAL',{'status':'INVALID'}))
if __name__=='__main__':unittest.main()
