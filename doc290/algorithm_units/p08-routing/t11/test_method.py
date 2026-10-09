import unittest,copy
from unittest.mock import patch
from bindings import load
from fixtures import development,edge,oracle
from proof import check,charged_check
from model import Invalid
class Development(unittest.TestCase):
    def test_all_synthetic_cases_both_methods(self):
        m,p=load('t11');b,bp=load('t9')
        for c in development():
            s=c['statement'];r=m.solve(s);check(s,r);br=b.solve(s);bp.check(s,br);self.assertEqual(None if r['route'] is None else r['route']['worst_time'],c['oracle']);self.assertEqual(None if br['route'] is None else br['route']['worst_time'],c['oracle'])
        r=m.solve(development()[0]['statement']);self.assertTrue(r['certificate']['source_bound_stronger']);self.assertTrue(r['certificate']['equality_exit']);self.assertEqual(r['counters']['labels_inserted'],0)
        r=m.solve(development()[5]['statement']);self.assertGreater(r['counters']['charged_strict_exclusions'],0);self.assertTrue(any(x['new_bound']==r['certificate']['upper'] and not x['pruned'] for x in r['bound_trace']))
    def test_typed_metadata_event_completeness(self):
        m,_=load('t11')
        for c in development():
            s=c['statement'];r=m.solve(s);changes=[]
            x=copy.deepcopy(r);x['extra']=0;changes.append(x)
            for key in ('reverse_relaxations','scenario_reverse_inspections','incumbent_inspections','charged_reverse_inspections'):
                for add in (1,999):
                    x=copy.deepcopy(r);x['counters'][key]+=add;changes.append(x)
            for key in r:
                x=copy.deepcopy(r);del x[key];changes.append(x)
            for key,value in [('charged_lambda',True),('charged_lambda',1.0),('lower',False),('old_lower',False),('source_bound_stronger',1),('reason',False)]:
                x=copy.deepcopy(r);x['certificate'][key]=value;changes.append(x)
            x=copy.deepcopy(r);x['counters']['charged_bound_stronger']=False;changes.append(x)
            if r['charged_proof'] is not None:
                x=copy.deepcopy(r);x['charged_proof']['distances'][0][0]=False;changes.append(x)
            if r['bound_trace']:
                x=copy.deepcopy(r);x['bound_trace'].pop();changes.append(x)
                x=copy.deepcopy(r);x['bound_trace'][0]['old_bound']=False;changes.append(x)
            for x in changes:
                with self.assertRaises((Invalid,KeyError,TypeError)):check(s,x)
    def test_audit_fail_before_decision_and_no_fallback(self):
        m,_=load('t11');s=development()[0]['statement']
        with patch.object(m,'charged_check',side_effect=Invalid('audit')):
            with self.assertRaises(Invalid):m.solve(s)
        with patch.object(m,'charged_reverse',return_value=[[None]*5]*2):
            with self.assertRaises(Invalid):m.solve(s)
        with patch.object(m,'charged_reverse',side_effect=RuntimeError('early must not call')):
            m.solve(development()[3]['statement']);m.solve(development()[6]['statement'])
    def test_revisit_turn_delay_correlated_goal_suffix(self):
        s={'graph':{'a':[edge('b',[1,5],1)],'b':[edge('c',[1,1],1),edge('g',[5,1],1)],'c':[edge('b',[1,1],1)],'g':[edge('u',[0,0],0)],'u':[edge('g',[0,0],0)]},'start':'a','goal':'g','budget':4,'forbidden':[[['a',0],['b',1]]],'penalties':[{'incoming':['c',0],'outgoing':['b',1],'delay':2}]}
        m,_=load('t11');r=m.solve(s);check(s,r);self.assertEqual(r['route']['path'],['a','b','c','b','g']);self.assertEqual(r['route']['worst_time'],10);self.assertEqual(oracle(s),10)
