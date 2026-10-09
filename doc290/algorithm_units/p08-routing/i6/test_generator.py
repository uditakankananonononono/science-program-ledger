import unittest,copy
from unittest.mock import patch
from generator import generate,previous
from proof import verify,down
from fixtures import development,statement,edge
from model import Failure,i3
class Development(unittest.TestCase):
    def test_all_synthetic_stages(self):
        for c in development():
            r=generate(c['statement']);self.assertEqual(r['status'],c['expected']);verify(c['statement'],r)
    def test_preserved_no_search_no_replacement(self):
        c=development()[1];s=c['statement']
        with patch.object(previous,'paths',side_effect=RuntimeError('no search')):
            # Downstream I5 itself enumerates for proof; only witness-completion
            # dispatch has no separate search. Patch downstream to a sentinel.
            with patch.object(previous,'generate',return_value={'downstream':'sentinel'}):r=generate(s)
        self.assertEqual(r['completed_statement'],s);self.assertEqual(r['status'],'PRESERVED')
    def test_independent_and_every_stage_mutations(self):
        for c in development():
            s=c['statement'];r=generate(s)
            with patch('generator.generate',side_effect=RuntimeError('forbidden')):verify(s,r)
            for key,value in [('reason',False),('reason',{}),('reason',None),('original',{}),('extra',0)]:
                x=copy.deepcopy(r);x[key]=value
                with self.assertRaises(Failure):verify(s,x)
            if 'selected_index' in r:
                for v in (False,0.0,99):
                    x=copy.deepcopy(r);x['selected_index']=v
                    with self.assertRaises(Failure):verify(s,x)
            if 'completed_statement' in r:
                x=copy.deepcopy(r);x['completed_statement']['route']['exposure']=False
                with self.assertRaises(Failure):verify(s,x)
                x=copy.deepcopy(r);x['downstream']['gap']='999/1'
                with self.assertRaises(Failure):verify(s,x)
    def test_revisit_turn_tie_identity(self):
        s=statement({'x':[edge('y',(2,3))],'y':[edge('w',(1,2)),edge('g',(2,1))],'w':[edge('y',(1,1))],'g':[]},start='x',forbidden=[[['x',0],['y',1]]],penalties=[{'incoming':['w',0],'outgoing':['y',1],'delay':2}]);r=generate(s);verify(s,r);self.assertEqual(r['selected_route']['path'],['x','y','w','y','g']);self.assertEqual(r['selected_route']['scenario_totals'],[8,9]);self.assertEqual(r['selected_route']['turn_penalty'],2)
        s=statement({'a':[edge('g',(4,4)),edge('g',(4,4))],'g':[]});r=generate(s);verify(s,r);self.assertEqual(r['selected_route']['edges'][0]['edge_index'],0)
        s=statement({'a':[edge('b',(2,3))],'b':[]},goal='a');r=generate(s);verify(s,r);self.assertEqual(r['selected_route']['edges'],[])
    def test_selected_domain_before_checker_and_no_rescue(self):
        s=development()[5]['statement']
        original=i3.b3.t2.helper.checked
        def input_only(x):
            if x['route'] is not None:raise RuntimeError('must cap before checker')
            return original(x)
        with patch.object(i3.b3.t2.helper,'checked',side_effect=input_only):
            r=generate(s);verify(s,r);self.assertEqual(r['status'],'UNAVAILABLE_WITNESS_DOMAIN')
    def test_reconstruction_audit_failure_is_failure(self):
        s=development()[0]['statement']
        with patch('generator.reconstruct',return_value={'path':['q','z'],'edges':[],'scenario_totals':[0,0],'worst_time':0,'exposure':0,'turn_penalty':0}):
            with self.assertRaises(Failure):generate(s)
    def test_65th_helper_no_prefix_no_downstream(self):
        s=development()[0]['statement'];raw=[{'arcs':[0],'exposure':0,'scenario_totals':[2,3]}]*65
        with patch.object(previous,'paths',return_value=(raw,True)),patch.object(previous,'generate') as emission:
            r=generate(s);emission.assert_not_called()
        with patch.object(down,'raw_paths',return_value=(raw,True)):
            verify(s,r)
            for v in (False,{},[],0,None):
                x=copy.deepcopy(r);x['reason']=v
                with self.assertRaises(Failure):verify(s,x)
    def test_supplied_suboptimal_preserved_and_nonminimum_no_rescue(self):
        s=statement({'a':[edge('g',(8,8)),edge('g',(1,1))],'g':[]});s['route']={'path':['a','g'],'edges':[{'source':'a','edge_index':0,'target':'g'}],'scenario_totals':[8,8],'worst_time':8,'exposure':0,'turn_penalty':0}
        r=generate(s);verify(s,r);self.assertEqual(r['completed_statement'],s);self.assertEqual(r['downstream']['status'],'UNAVAILABLE')
        # Repeated incoming-state supplied walk is valid and still preserved.
        s=statement({'a':[edge('b',(1,1))],'b':[edge('a',(1,1)),edge('g',(1,1))],'g':[]});s['route']={'path':['a','b','a','b','g'],'edges':[{'source':a,'edge_index':j,'target':b} for a,j,b in [('a',0,'b'),('b',0,'a'),('a',0,'b'),('b',1,'g')]],'scenario_totals':[4,4],'worst_time':4,'exposure':0,'turn_penalty':0};r=generate(s);verify(s,r);self.assertEqual(r['completed_statement'],s)
        s['route']=None;r=generate(s);verify(s,r);self.assertEqual(r['selected_route']['worst_time'],2)
    def test_parent_all_ledger_fields_refuse_typed_mutations(self):
        for c in development():
            s=c['statement'];r=generate(s);changes=[]
            if 'paths' in r and r['paths']:
                x=copy.deepcopy(r);x['paths'][0]['arcs'][0]=False;changes.append(x)
                x=copy.deepcopy(r);x['paths'][0]['scenario_totals'][0]=float(x['paths'][0]['scenario_totals'][0]);changes.append(x)
            for key in ('feasible_indices','objectives'):
                if key in r and r[key]:
                    x=copy.deepcopy(r);x[key][0]=False;changes.append(x)
            if 'selected_route' in r:
                x=copy.deepcopy(r);x['selected_route']['turn_penalty']=False;changes.append(x)
            for x in changes:
                with self.assertRaises(Failure):verify(s,x)
