import unittest,copy,math
from analysis import order,quartiles,ratio,summarize
from classes import classify
from core import ROOT
import json
class Development(unittest.TestCase):
    def rows(self):
        classes=['equality_exit','strict_gap_search'];rows=[]
        for i in range(2):
            for r in range(3):
                ss={m:{'status':'PASS','worker':{'solve_seconds':(.5 if i==0 else 2) if m=='variant' else 1,'affinity':[0],'counters':{},'route':{}}} for m in ('variant','t8')};rows.append({'case_index':i,'repeat':r,'name':str(i),'order':order(i,r),'class':classes[i],'subjects':ss})
        return rows,classes
    def test_order_and_classes(self):
        self.assertEqual(sum(order(i,r)[0]=='variant' for i in range(200) for r in range(3)),300)
        cs=json.loads((ROOT/'cases.json').read_text());self.assertEqual([classify(c['statement']) for c in cs],json.loads((ROOT/'classes.json').read_text()));self.assertEqual((ROOT/'cases.json').read_bytes(),(ROOT.parent/'t9'/'cases.json').read_bytes())
    def test_rank_faster_slower_tie_outlier(self):
        self.assertEqual(quartiles([9,1,4,2])['median'],2);rs,cs=self.rows();s=summarize(rs,cs)['all_cases'];self.assertEqual((s['faster'],s['slower']),(3,3));self.assertTrue(all(r['status']=='PASS' for r in s['deterministic_checks']))
        rs[0]['subjects']['variant']['worker']['solve_seconds']=1;rs[1]['subjects']['variant']['worker']['solve_seconds']=10000;s=summarize(rs,cs)['all_cases'];self.assertEqual(s['ties'],1);self.assertIn(10000,[r.get('ratio') for r in s['pairs']])
    def test_fail_zero_numeric_empty_incomplete(self):
        rs,cs=self.rows();rs[0]['subjects']['variant']['status']='FAIL';rs[1]['subjects']['t8']['worker']['solve_seconds']=0;rs[2]['subjects']['variant']['worker']['solve_seconds']=1e308;rs[2]['subjects']['t8']['worker']['solve_seconds']=1e-308;s=summarize(rs,cs)['all_cases'];self.assertEqual(s['eligible_pairs'],3);self.assertEqual(sum(s['exclusions'].values()),3);self.assertEqual(s['incomplete_cases'],1)
        for a,b in ((1e308,1e-308),(1e-308,1e308)):self.assertEqual(ratio(a,b)['reason'],'numeric_ratio')
        for a in (True,-1,float('nan'),float('inf')):self.assertEqual(ratio(a,1)['reason'],'invalid_duration')
        for r in rs:r['subjects']['variant']['status']='FAIL'
        s=summarize(rs,cs);self.assertIsNone(s['all_cases']['ratio_distribution']['median']);self.assertIsNone(s['classes']['no_allowed_turn_path']['case_ratio_distribution']['median'])
    def test_structure_cpu_repeat(self):
        rs,cs=self.rows()
        for bad in (rs[:-1],rs+[rs[0]]):
            with self.assertRaises(ValueError):summarize(bad,cs)
        rs[0]['subjects']['t8']['worker']['affinity']=[1];rs[3]['subjects']['variant']['worker']['counters']={'bad':1};s=summarize(rs,cs)['all_cases'];self.assertEqual(s['exclusions']['cpu_mismatch'],1);self.assertEqual(s['deterministic_checks'][1]['status'],'FAIL')
    def test_original_binding_strictgap_equality(self):
        from bindings import load
        from model import witness
        s={'graph':{'a':[{'target':'g','time':1,'exposure':0,'scenario_times':[1,5]},{'target':'g','time':1,'exposure':0,'scenario_times':[5,1]}],'g':[]},'start':'a','goal':'g','budget':0,'forbidden':[],'penalties':[]}
        a,pa=load('t9');b,pb=load('t8');ra=a.solve(s);rb=b.solve(s)
        self.assertIs(a.original_t7_proof,pa.original_t7_proof);self.assertIs(b.original_t7_proof,pb.original);self.assertEqual(ra['certificate']['reason'],'strict_gap_search')
        for k in ('route','counters','proof','scenario_proof','incumbent'):self.assertEqual(ra[k],rb[k])
        s['graph']['a'][0]['scenario_times']=[1,1];ra=a.solve(s);rb=b.solve(s);self.assertEqual(ra['certificate']['reason'],'equality_exit');self.assertEqual(witness(s,ra['route'])['worst_time'],witness(s,rb['route'])['worst_time'])
    def test_log_refusal_and_class_order(self):
        from unittest.mock import patch
        with patch('analysis.math.log',return_value=float('inf')):self.assertEqual(ratio(1,1)['reason'],'numeric_log')
        rows,cs=self.rows();x=summarize(rows,cs);self.assertEqual(x['classes']['equality_exit']['actual_order_counts'],{'T9_first':2,'T8_first':1});self.assertEqual(x['classes']['strict_gap_search']['actual_order_counts'],{'T9_first':1,'T8_first':2})
