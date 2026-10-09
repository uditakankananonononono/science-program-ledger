import unittest,copy
from analysis import order,quartiles,paired_ratio,summarize
class AnalysisDevelopment(unittest.TestCase):
    def rows(self):
        out=[]
        for i in range(2):
            for rep in range(3):
                subjects={m:{'status':'PASS','worker':{'solve_seconds':(.5 if i==0 else 2) if m=='variant' else 1,'affinity':[0],'route':{},'counters':{},'identity':{},'as_limit_bytes':[134217728]*2}} for m in ('variant','p3')};out.append({'case_index':i,'name':str(i),'repeat':rep,'order':order(i,rep),'subjects':subjects})
        return out
    def test_order_and_nearest_rank(self):
        self.assertEqual(sum(order(i,r)[0]=='variant' for i in range(200) for r in range(3)),300);self.assertEqual(quartiles([9,1,4,2])['median'],2);self.assertEqual(quartiles([])['status'],'UNAVAILABLE')
    def test_faster_slower_tie_outlier(self):
        rs=self.rows();x=summarize(rs,2);self.assertEqual(x['descriptive_wins'],3);self.assertEqual(x['losses'],3);self.assertEqual(x['eligible_pair_count'],6);self.assertTrue(all(r['status']=='PASS' for r in x['deterministic_repeat_checks']))
        rs[0]['subjects']['variant']['worker']['solve_seconds']=1;rs[1]['subjects']['variant']['worker']['solve_seconds']=10000;x=summarize(rs,2);self.assertEqual(x['ties'],1);self.assertIn(10000,[r['ratio'] for r in x['pairs']])
    def test_failure_nonpositive_incomplete_empty(self):
        rs=self.rows();rs[0]['subjects']['variant']['status']='FAIL';rs[1]['subjects']['p3']['worker']['solve_seconds']=0;x=summarize(rs,2);self.assertEqual(x['pair_exclusions']['worker_failure'],1);self.assertEqual(x['pair_exclusions']['nonpositive_or_nonfinite_duration'],1);self.assertEqual(x['eligible_pair_count'],4);self.assertEqual(x['incomplete_case_exclusions'],1);self.assertEqual(len(x['case_medians']),1)
        for r in rs:r['subjects']['variant']['status']='FAIL'
        x=summarize(rs,2);self.assertEqual(x['pair_ratio_distribution']['status'],'UNAVAILABLE');self.assertEqual(x['case_ratio_distribution']['status'],'UNAVAILABLE')
    def test_numerical_exclusions_cpu_and_repeat(self):
        for a,b in ((1e308,1e-308),(1e-308,1e308)):
            self.assertEqual(paired_ratio(a,b)['reason'],'unrepresentable_ratio')
        for a in (True,0,-1,float('nan'),float('inf')):self.assertFalse(paired_ratio(a,1)['eligible'])
        rs=self.rows();rs[0]['subjects']['p3']['worker']['affinity']=[1];rs[3]['subjects']['variant']['worker']['counters']={'new':1};x=summarize(rs,2);self.assertEqual(x['actual_pair_cpu_mismatch_count'],1);self.assertEqual(x['deterministic_repeat_checks'][1]['status'],'FAIL')
