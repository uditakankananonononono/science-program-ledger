import unittest
from certificate import check,b3
class Development(unittest.TestCase):
    def s(self):return {'graph':{'a':[{'target':'g','time':1,'exposure':0,'scenario_times':[2,4]}],'g':[{'target':'a','time':1,'exposure':0,'scenario_times':[1,1]}],'x':[{'target':'x','time':0,'exposure':0,'scenario_times':[0,0]}]},'start':'a','goal':'g','route':{'path':['a','g'],'edges':[{'source':'a','edge_index':0,'target':'g'}],'scenario_totals':[2,4],'worst_time':4},'weights':[0,1],'potential':[0,4,'-1/2']}
    def test_all_edges_weighted_algebra(self):
        r=check(self.s());self.assertEqual(r['status'],'CERTIFIED_MINIMAX');self.assertEqual(len(r['edge_ledger']),3);self.assertEqual(r['edge_ledger'][1]['slack'],'5/1')
    def test_simplex_grammar(self):
        for w in ([True,0],[1.0,0],['2/4','1/2'],[-1,2],[1,1],[1]):
            s=self.s();s['weights']=w;self.assertEqual(check(s)['status'],'INVALID')
    def test_feasibility_before_slack(self):
        s=self.s();s['potential']=[0,5,0];self.assertEqual(check(s)['status'],'INVALID');s['potential']=[0,0,0];self.assertEqual(check(s)['status'],'UNAVAILABLE')
    def test_model_first_identity_dimension(self):
        s=self.s();s['route']=None;s['graph']['g'][0]['scenario_times']=[];self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['graph']={'a':[]};s['route']=None;s['goal']='a';self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s.update(goal='x',start='x',route={'path':['x'],'edges':[],'scenario_totals':[0,0],'worst_time':0},potential=[0,0,0]);self.assertEqual(check(s)['status'],'CERTIFIED_MINIMAX')
    def test_primal_proxy_and_caps(self):
        s=self.s();s['route']['worst_time']=True;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['potential'][1]=b3.MAX+1;self.assertEqual(check(s)['status'],'INVALID')
        s=self.s();s['route']['edges'][0]['edge_index']=-1;self.assertEqual(check(s)['status'],'INVALID')
    def test_disagreement(self):
        from compare import agreed
        self.assertFalse(agreed('CERTIFIED_MINIMAX',{'status':'INVALID'}))
if __name__=='__main__':unittest.main()
