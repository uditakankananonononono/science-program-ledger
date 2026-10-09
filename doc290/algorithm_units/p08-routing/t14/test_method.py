import unittest,copy
from unittest.mock import patch
from bindings import load
from fixtures import development
from proof import check,baseline
from model import Invalid
class Development(unittest.TestCase):
    def test_all_both_oracle_single_preprocess(self):
        m,_=load('t14');b,bp=load('t13')
        for c in development():
            r=m.solve(c['statement']);check(c['statement'],r);br=b.solve(c['statement']);bp.check(c['statement'],br)
            self.assertEqual(None if r['route'] is None else r['route']['worst_time'],c['oracle'])
            for k in ('reverse_relaxations','scenario_reverse_inspections','incumbent_inspections'):self.assertEqual(r['counters'][k],br['counters'][k])
    def test_actual_skip_and_parent_no_scalar_expected_no_audit(self):
        m,_=load('t14')
        for k in (3,4):
            s=development()[k]['statement']
            with patch.object(m,'scalar_candidate',side_effect=RuntimeError('skip')),patch.object(m,'build_candidates',side_effect=RuntimeError('skip')),patch.object(m,'candidates_check',side_effect=RuntimeError('skip')),patch.object(m,'charged_reverse',side_effect=RuntimeError('skip')),patch.object(m,'charged_check',side_effect=RuntimeError('skip')):r=m.solve(s)
            with patch.object(baseline,'candidate_expected',side_effect=RuntimeError('no expected')),patch.object(baseline,'candidates_check',side_effect=RuntimeError('no audit')),patch.object(baseline,'scenario_candidate_expected',side_effect=RuntimeError('no scalar')),patch.object(baseline.prior,'charged_distances',side_effect=RuntimeError('no charged')):check(s,r)
            self.assertEqual(r['candidate_activation'],'original_bound_equality');self.assertIs(r['route'],r['incumbent']);self.assertIsNone(r['candidate_ledger']);self.assertIsNone(r['selected_candidate'])
    def test_audit_error_activated_and_early(self):
        m,_=load('t14')
        with patch.object(m,'candidates_check',side_effect=Invalid('audit')):
            with self.assertRaises(Invalid):m.solve(development()[0]['statement'])
        with patch.object(m,'build_candidates',side_effect=RuntimeError('early')):
            for k in (5,6):m.solve(development()[k]['statement'])
    def test_exact_stage_and_skip_mutations(self):
        m,_=load('t14')
        for c in development():
            s=c['statement'];r=m.solve(s);changes=[]
            for key in r:
                x=copy.deepcopy(r);del x[key];changes.append(x)
            x=copy.deepcopy(r);x['extra']=0;changes.append(x)
            for key in ('reverse_relaxations','scenario_reverse_inspections','incumbent_inspections','charged_reverse_inspections','scalar_candidate_inspections'):
                for add in (1,999):
                    x=copy.deepcopy(r);x['counters'][key]+=add;changes.append(x)
            for v in (None,False,'bogus'):
                x=copy.deepcopy(r);x['candidate_activation']=v;changes.append(x)
            if r['candidate_activation']=='original_bound_equality':
                x=copy.deepcopy(r);x['selected_candidate']=0;changes.append(x)
                x=copy.deepcopy(r);x['candidate_ledger']=[];changes.append(x)
                x=copy.deepcopy(r);x['incumbent_selected_upper']=False;changes.append(x)
            for x in changes:
                with self.assertRaises((Invalid,KeyError,TypeError)):check(s,x)
