import unittest,copy
from unittest.mock import patch
from generator import generate
from proof import verify
from model import t5,Failure
from fixtures import development,statement,edge,MAX
class Development(unittest.TestCase):
    def test_real_development_stages(self):
        for c in development():r=generate(c['statement']);self.assertEqual(r['status'],c['expected']);verify(c['statement'],r)
    def test_supplied_no_search_corruption_no_repair(self):
        for c in development()[1:3]:
            with patch('generator.minima',side_effect=RuntimeError('no search')):r=generate(c['statement']);verify(c['statement'],r)
            self.assertEqual(r['original'],c['statement'])
    def test_independent_allstage_strict_mutations(self):
        for c in development():
            s=c['statement'];r=generate(s)
            with patch('generator.generate',side_effect=RuntimeError('forbidden')),patch('generator.minima',side_effect=RuntimeError('forbidden')):verify(s,r)
            for key,value in [('reason',False),('reason',{}),('original',{}),('extra',0)]:
                x=copy.deepcopy(r);x[key]=value
                with self.assertRaises(Failure):verify(s,x)
            if r['status']=='COMPLETED':
                for value in (None,True,2.0,99):
                    x=copy.deepcopy(r);x['distances'][0]=value
                    with self.assertRaises(Failure):verify(s,x)
                x=copy.deepcopy(r);x['exposure_arcs'][0]['source']=False
                with self.assertRaises(Failure):verify(s,x)
            if 'downstream' in r:
                x=copy.deepcopy(r);x['downstream']['reason']=False
                with self.assertRaises(Failure):verify(s,x)
    def test_unreachable_goaloutgoing_zero_parallel_identity_large(self):
        s=statement({'q':[edge('g',0),edge('g',1)],'g':[edge('v',2)],'v':[edge('g',3)],'unused':[edge('g',7)]},start='q');r=generate(s);verify(s,r);self.assertEqual(r['source_minimum'],0);self.assertTrue(all(v is not None for v in r['distances']))
        s=statement({'a':[edge('b',0)],'b':[edge('a',0)]},goal='a');r=generate(s);verify(s,r);self.assertEqual(r['source_minimum'],0)
        s=statement({'a':[edge('g',0) for _ in range(9)],'g':[]});r=generate(s);verify(s,r);self.assertEqual(r['status'],'COMPLETED')
        s=statement({'a':[edge('b',1)],'b':[edge('g',1)],'g':[]},forbidden=[[['a',0],['b',0]]]);r=generate(s);verify(s,r);self.assertIsNone(r['distances'][0]);self.assertEqual(r['distances'][2],0)
    def test_large_total_and_penalty_not_exposure(self):
        s=statement({'a':[edge('b',MAX)],'b':[edge('g',MAX)],'g':[]},penalties=[{'incoming':['a',0],'outgoing':['b',0],'delay':2}]);r=generate(s);verify(s,r);self.assertEqual(r['source_minimum'],2*MAX);self.assertEqual(r['downstream']['status'],'CERTIFIED_BUDGET_INFEASIBLE')
        s['penalties'][0]['delay']=MAX;r=generate(s);verify(s,r);self.assertEqual(r['status'],'INVALID')
    def test_synthesized_checker_invalid_is_fail(self):
        s=development()[0]['statement']
        with patch.object(t5,'check',return_value={'status':'INVALID'}):
            with self.assertRaises(Failure):generate(s)
        with patch('generator.minima',return_value=[None]*4):
            with self.assertRaises(Failure):generate(s)
