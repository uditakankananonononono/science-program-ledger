import unittest,copy
from unittest.mock import patch
from bindings import load
from fixtures import development
from proof import check
from model import Invalid
class Development(unittest.TestCase):
    def test_all_both_original_oracles(self):
        m,_=load('t13');b,bp=load('t12')
        for c in development():
            original=copy.deepcopy(c['statement']);r=m.solve(c['statement']);check(c['statement'],r);br=b.solve(c['statement']);bp.check(c['statement'],br)
            self.assertEqual(original,c['statement']);self.assertEqual(None if r['route'] is None else r['route']['worst_time'],c['oracle']);self.assertEqual(None if br['route'] is None else br['route']['worst_time'],c['oracle'])
    def test_improved_overbudget_duplicate_correlation_identity(self):
        m,_=load('t13');r=m.solve(development()[0]['statement']);self.assertEqual(r['incumbent_original_upper'],8);self.assertEqual(r['incumbent_selected_upper'],2);self.assertEqual(r['selected_candidate'],1)
        r=m.solve(development()[1]['statement']);self.assertEqual(r['selected_candidate'],0);self.assertEqual(r['candidate_ledger'][1]['audit']['state'],'valid_but_ineligible_over_budget')
        r=m.solve(development()[2]['statement']);self.assertEqual(r['selected_candidate'],0);self.assertEqual(r['candidate_ledger'][1]['route']['scenario_totals'],[1,10])
        for k in (3,4):
            r=m.solve(development()[k]['statement']);self.assertEqual(r['selected_candidate'],0);self.assertEqual(len(r['candidate_ledger']),3)
    def test_raises_equality_skip_and_candidate_audit(self):
        m,_=load('t13')
        for k in (0,3,4):
            with patch.object(m,'charged_reverse',side_effect=RuntimeError('skip')),patch.object(m,'charged_check',side_effect=RuntimeError('skip')):r=m.solve(development()[k]['statement']);check(development()[k]['statement'],r)
        with patch.object(m,'candidates_check',side_effect=Invalid('audit')):
            with self.assertRaises(Invalid):m.solve(development()[0]['statement'])
        with patch.object(m,'build_candidates',side_effect=RuntimeError('early no candidates')):
            for k in (5,6):m.solve(development()[k]['statement'])
    def test_every_top_and_candidate_schema_refusal(self):
        m,_=load('t13')
        for c in development():
            s=c['statement'];r=m.solve(s);changes=[]
            for key in r:
                x=copy.deepcopy(r);del x[key];changes.append(x)
            x=copy.deepcopy(r);x['extra']=0;changes.append(x)
            if r['candidate_ledger'] is not None:
                x=copy.deepcopy(r);x['incumbent_selected_upper']=r['incumbent_original_upper']+1;changes.append(x)
                for v in (False,0.0,99):
                    x=copy.deepcopy(r);x['selected_candidate']=v;changes.append(x)
                for key in r['candidate_ledger'][1]:
                    x=copy.deepcopy(r);del x['candidate_ledger'][1][key];changes.append(x)
            for x in changes:
                with self.assertRaises((Invalid,KeyError,TypeError)):check(s,x)
    def test_partial_stop_is_not_fullproof(self):
        m,_=load('t13');s=development()[8]['statement'];r=m.solve(s);check(s,r)
        stop=r['candidate_ledger'][1]['stop_ledger'];self.assertIn('NOT complete',stop['semantics']);self.assertTrue(any(v!='settled' for v in stop['state_status']))
