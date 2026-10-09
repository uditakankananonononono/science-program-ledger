import unittest,copy
from unittest.mock import patch
from bindings import load
from fixtures import development,oracle,edge
from proof import check,prior
from model import Invalid
class Development(unittest.TestCase):
    def test_both_all_branches_oracle(self):
        m,_=load('t12');b,bp=load('t11')
        for c in development():
            r=m.solve(c['statement']);check(c['statement'],r);br=b.solve(c['statement']);bp.check(c['statement'],br)
            self.assertEqual(None if r['route'] is None else r['route']['worst_time'],c['oracle']);self.assertEqual(r['route'],br['route'])
    def test_lazy_old_equality_identity_never_charge(self):
        m,_=load('t12')
        for k in (4,7):
            s=development()[k]['statement']
            with patch.object(m,'charged_reverse',side_effect=RuntimeError('must not call')),patch.object(m,'charged_check',side_effect=RuntimeError('must not audit')):r=m.solve(s)
            with patch.object(prior,'charged_distances',side_effect=RuntimeError('parent must not invent charged ledger')):check(s,r)
            self.assertEqual(r['activation'],'old_bound_equality');self.assertIsNone(r['charged_proof']);self.assertEqual(r['counters']['charged_reverse_inspections'],0)
    def test_early_no_charge_and_audit_error_before_decision(self):
        m,_=load('t12')
        with patch.object(m,'charged_reverse',side_effect=RuntimeError('early no call')):
            for k in (3,6):r=m.solve(development()[k]['statement']);check(development()[k]['statement'],r)
        with patch.object(m,'charged_check',side_effect=Invalid('audit fail')):
            with self.assertRaises(Invalid):m.solve(development()[0]['statement'])
    def test_exact_top_branch_and_counter_mutations(self):
        m,_=load('t12')
        for c in development():
            s=c['statement'];r=m.solve(s);changes=[]
            for key in r:
                x=copy.deepcopy(r);del x[key];changes.append(x)
            x=copy.deepcopy(r);x['extra']=0;changes.append(x)
            for key in ('reverse_relaxations','scenario_reverse_inspections','incumbent_inspections','charged_reverse_inspections'):
                for add in (1,999):
                    x=copy.deepcopy(r);x['counters'][key]+=add;changes.append(x)
            for value in (False,None,'bogus'):
                x=copy.deepcopy(r);x['activation']=value;changes.append(x)
            x=copy.deepcopy(r);x['certificate']['old_lower']=False;changes.append(x)
            for x in changes:
                with self.assertRaises((Invalid,KeyError,TypeError)):check(s,x)
    def test_revisit_turn_goal_suffix(self):
        s={'graph':{'a':[edge('b',[1,5],1)],'b':[edge('c',[1,1],1),edge('g',[5,1],1)],'c':[edge('b',[1,1],1)],'g':[edge('u',[0,0],0)],'u':[edge('g',[0,0],0)]},'start':'a','goal':'g','budget':4,'forbidden':[[['a',0],['b',1]]],'penalties':[{'incoming':['c',0],'outgoing':['b',1],'delay':2}]}
        m,_=load('t12');r=m.solve(s);check(s,r);self.assertEqual(r['route']['worst_time'],oracle(s))
