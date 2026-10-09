import unittest,copy
from unittest.mock import patch
from bindings import load
from fixtures import development,edge,oracle
from model import Invalid
class Development(unittest.TestCase):
    def test_all_both_oracle_counts(self):
        m,p=load('t16');b,bp=load('t15')
        for c in development():
            r=m.solve(c['statement']);p.check(c['statement'],r);br=b.solve(c['statement']);bp.check(c['statement'],br)
            self.assertEqual(None if r['route'] is None else r['route']['worst_time'],c['oracle'])
            for k in ('reverse_relaxations','scenario_reverse_inspections','incumbent_inspections'):self.assertEqual(r['counters'][k],br['counters'][k])
    def test_original_skips_raise(self):
        m,p=load('t16')
        for k in (3,4,5,6):
            s=development()[k]['statement']
            with patch.object(m,'charged_reverse',side_effect=RuntimeError('skip')),patch.object(m,'charged_check',side_effect=RuntimeError('skip')),patch.object(m,'build_candidates',side_effect=RuntimeError('skip')),patch.object(m,'route_audit',side_effect=RuntimeError('skip')),patch.object(p,'candidate_prefix_expected',side_effect=RuntimeError('skip')):r=m.solve(s);p.check(s,r)
            self.assertEqual(r['candidate_schedule'],'uncharged_skip');self.assertIsNone(r['candidate_prefix'])
    def test_charged_originalW_skip_absent(self):
        m,p=load('t16');s=copy.deepcopy(development()[1]['statement']);s['graph']['a'][1]['exposure']=6
        with patch.object(m,'scalar_candidate',side_effect=RuntimeError('skip')),patch.object(m,'build_candidates',side_effect=RuntimeError('skip')),patch.object(m,'route_audit',side_effect=RuntimeError('skip')),patch.object(p,'candidate_prefix_expected',side_effect=RuntimeError('skip')):r=m.solve(s);p.check(s,r)
        self.assertEqual(r['candidate_activation'],'charged_original_bound_equality');self.assertIs(r['route'],r['incumbent']);self.assertIsNone(r['candidate_ledger']);self.assertIsNone(r['selected_candidate']);self.assertIsNone(r['candidate_prefix']);self.assertEqual(r['counters']['scalar_candidate_inspections'],0);self.assertGreater(r['counters']['charged_reverse_inspections'],0)
    def test_once_charged_reuse_and_added_tradeoff(self):
        m,p=load('t16');b,_=load('t15');orig=m.charged_reverse;audit=m.charged_check
        for k in (0,1,2,7):
            s=development()[k]['statement'];calls=[];checks=[]
            def once(*args):
                if calls:raise RuntimeError('rerun charged')
                v=orig(*args);calls.append(v);return v
            def onceaudit(*args):
                if checks:raise RuntimeError('repeat charged audit')
                checks.append(args[1]);return audit(*args)
            with patch.object(m,'charged_reverse',side_effect=once),patch.object(m,'charged_check',side_effect=onceaudit):r=m.solve(s);p.check(s,r)
            self.assertEqual(len(calls),1);self.assertEqual(len(checks),1);self.assertIs(r['charged_proof'],checks[0]);self.assertIs(r['charged_proof']['distances'],calls[0]);self.assertEqual(r['route']['worst_time'],oracle(s))
        s=development()[0]['statement'];r=m.solve(s);br=b.solve(s);self.assertGreater(r['counters']['charged_reverse_inspections'],br['counters']['charged_reverse_inspections']);self.assertEqual(br['counters']['charged_reverse_inspections'],0)
    def test_combined_prefix_omitted_raise(self):
        m,p=load('t16');s=development()[0]['statement'];orig=m.scalar_candidate;raw=p.scenario_candidate_expected
        def construct(*args):
            if args[-2]>0:raise RuntimeError('omitted constructor')
            return orig(*args)
        def replay(s,column):
            if column>0:raise RuntimeError('omitted replay')
            return raw(s,column)
        with patch.object(m,'scalar_candidate',side_effect=construct),patch.object(p,'scenario_candidate_expected',side_effect=replay):r=m.solve(s);p.check(s,r)
        self.assertIs(r['route'],r['incumbent']);self.assertIs(r['route'],r['candidate_ledger'][r['selected_candidate']]['route']);self.assertEqual(r['candidate_prefix']['bound_kind'],'combined_fixed_lambda1');self.assertEqual(r['candidate_prefix']['remaining_scenario_indices'],[1])
    def test_last_equality_and_audit_errors(self):
        m,p=load('t16');s={'graph':{'a':[edge('g',[8,8],0),edge('g',[1,10],1),edge('g',[2,2],1)],'g':[]},'start':'a','goal':'g','budget':1,'forbidden':[],'penalties':[]}
        r=m.solve(s);p.check(s,r);self.assertEqual(r['candidate_prefix']['terminal_reason'],'bound_equality');self.assertEqual(r['candidate_prefix']['remaining_scenario_indices'],[]);self.assertEqual(r['candidate_prefix']['scenario_count'],2)
        with patch.object(m,'charged_check',side_effect=Invalid('audit')):
            with self.assertRaises(Invalid):m.solve(development()[0]['statement'])
        with patch.object(m,'candidates_check',side_effect=Invalid('audit')):
            with self.assertRaises(Invalid):m.solve(development()[0]['statement'])
    def test_all_schema_and_counter_mutations(self):
        m,p=load('t16')
        for c in development():
            s=c['statement'];r=m.solve(s);changes=[]
            for key in r:
                x=copy.deepcopy(r);del x[key];changes.append(x)
            for key in r['counters']:
                for add in (1,999):
                    x=copy.deepcopy(r);x['counters'][key]+=add;changes.append(x)
            for key in ('candidate_activation','candidate_schedule'):
                for value in (False,None,'bogus'):
                    x=copy.deepcopy(r);x[key]=value;changes.append(x)
            if r['candidate_prefix'] is not None:
                for key,value in [('original_L',False),('combined_L',False),('bound_kind','original'),('scenario_count',False),('selected_index',0.0),('remaining_scenario_indices',[False]),('terminal_reason','continuing')]:
                    x=copy.deepcopy(r);x['candidate_prefix'][key]=value;changes.append(x)
                x=copy.deepcopy(r);x['candidate_ledger'].append(copy.deepcopy(x['candidate_ledger'][-1]));changes.append(x)
            if r['candidate_activation']=='charged_original_bound_equality':
                for key,value in [('candidate_ledger',[]),('selected_candidate',0),('candidate_prefix',{}),('incumbent_selected_upper',False),('charged_proof',None)]:
                    x=copy.deepcopy(r);x[key]=value;changes.append(x)
            for x in changes:
                with self.assertRaises((Invalid,KeyError,TypeError)):p.check(s,x)
