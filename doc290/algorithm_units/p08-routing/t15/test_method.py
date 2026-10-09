import unittest,copy
from unittest.mock import patch
from bindings import load
from fixtures import development,edge,oracle
from proof import check
from model import Invalid
class Development(unittest.TestCase):
    def test_all_both_oracle_single_preprocess(self):
        m,_=load('t15');b,bp=load('t14')
        for c in development():
            r=m.solve(c['statement']);check(c['statement'],r);br=b.solve(c['statement']);bp.check(c['statement'],br)
            self.assertEqual(None if r['route'] is None else r['route']['worst_time'],c['oracle'])
            self.assertEqual(r['route'],br['route'])
            for k in ('reverse_relaxations','scenario_reverse_inspections','incumbent_inspections','labels_inserted','candidate_edges','charged_reverse_inspections'):self.assertEqual(r['counters'][k],br['counters'][k])
    def test_positive_prefix_omitted_raise_same_route(self):
        m,p=load('t15');s=development()[0]['statement'];orig=m.scalar_candidate;raw=p.scenario_candidate_expected;audit=m.route_audit;produced=[]
        def construct(*args):
            if args[-2]>0:raise RuntimeError('omitted constructor')
            route,stop=orig(*args);produced.append(route);return route,stop
        def routeaudit(s,route):
            if route not in produced and route['worst_time']!=8:raise RuntimeError('omitted route audit')
            return audit(s,route)
        def replay(s,column):
            if column>0:raise RuntimeError('omitted replay')
            return raw(s,column)
        with patch.object(m,'route_audit',side_effect=routeaudit),patch.object(m,'scalar_candidate',side_effect=construct),patch.object(p,'scenario_candidate_expected',side_effect=replay),patch.object(m,'charged_reverse',side_effect=RuntimeError('charged')),patch.object(m,'charged_check',side_effect=RuntimeError('charged')):
            r=m.solve(s);p.check(s,r)
        self.assertEqual(r['candidate_prefix']['remaining_scenario_indices'],[1]);self.assertEqual(r['candidate_prefix']['terminal_reason'],'bound_equality');self.assertIs(r['route'],r['incumbent']);self.assertIs(r['route'],r['candidate_ledger'][r['selected_candidate']]['route'])
        # Later candidate audits are impossible because its constructor/replay refuses.
        bad=copy.deepcopy(r);bad['candidate_ledger'].append(copy.deepcopy(bad['candidate_ledger'][-1]));bad['candidate_prefix']['scenario_count']=2;bad['candidate_prefix']['remaining_scenario_indices']=[]
        with self.assertRaises(Invalid):p.check(s,bad)
    def test_original_absent_skip_raise(self):
        m,p=load('t15')
        for k in (3,4):
            s=development()[k]['statement']
            with patch.object(m,'scalar_candidate',side_effect=RuntimeError('skip')),patch.object(m,'build_candidates',side_effect=RuntimeError('skip')),patch.object(m,'route_audit',side_effect=RuntimeError('skip')),patch.object(m,'candidates_check',side_effect=RuntimeError('skip')),patch.object(m,'charged_reverse',side_effect=RuntimeError('skip')),patch.object(p,'candidate_prefix_expected',side_effect=RuntimeError('skip')):r=m.solve(s);p.check(s,r)
            self.assertIsNone(r['candidate_prefix']);self.assertIsNone(r['candidate_ledger']);self.assertIs(r['route'],r['incumbent'])
    def test_last_equality_full_ineligible_and_fail(self):
        m,p=load('t15');s={'graph':{'a':[edge('g',[8,8],0),edge('g',[1,10],1),edge('g',[2,2],1)],'g':[]},'start':'a','goal':'g','budget':1,'forbidden':[],'penalties':[]}
        r=m.solve(s);p.check(s,r);self.assertEqual(r['candidate_prefix']['scenario_count'],2);self.assertEqual(r['candidate_prefix']['remaining_scenario_indices'],[]);self.assertEqual(r['candidate_prefix']['terminal_reason'],'bound_equality');self.assertEqual(r['route']['worst_time'],oracle(s))
        for k in (1,2,7):
            s=development()[k]['statement'];r=m.solve(s);p.check(s,r);self.assertEqual(r['candidate_prefix']['terminal_reason'],'all_candidates');self.assertEqual(r['candidate_prefix']['remaining_scenario_indices'],[])
        with patch.object(m,'candidates_check',side_effect=Invalid('candidate audit')):
            with self.assertRaises(Invalid):m.solve(development()[0]['statement'])
    def test_metadata_counts_mutations(self):
        m,p=load('t15')
        for c in development():
            s=c['statement'];r=m.solve(s);changes=[]
            for k in r:
                x=copy.deepcopy(r);del x[k];changes.append(x)
            for k in r['counters']:
                for add in (1,999):
                    x=copy.deepcopy(r);x['counters'][k]+=add;changes.append(x)
            if r['candidate_prefix'] is not None:
                for k in r['candidate_prefix']:
                    x=copy.deepcopy(r);del x['candidate_prefix'][k];changes.append(x)
                for k,v in [('scenario_count',True),('selected_index',0.0),('selected_W',False),('original_L',False),('remaining_scenario_indices',[False]),('terminal_reason','continuing')]:
                    x=copy.deepcopy(r);x['candidate_prefix'][k]=v;changes.append(x)
            else:
                x=copy.deepcopy(r);x['candidate_prefix']={};changes.append(x)
            for x in changes:
                with self.assertRaises((Invalid,KeyError,TypeError)):p.check(s,x)
