import unittest
from routing import Edge, exposure_budget_route as budget, scenario_robust_route as robust, budgeted_scenario_route as joint

class HardenedTests(unittest.TestCase):
    def assert_witness(self,g,result):
        self.assertIsNotNone(result)
        selected=[]
        for i, item in enumerate(result['edges']):
            self.assertEqual(item['source'],result['path'][i])
            edge=g[item['source']][item['edge_index']]
            self.assertEqual(edge.target,result['path'][i+1])
            self.assertEqual(edge.target,item['target'])
            selected.append(edge)
        if 'time' in result: self.assertEqual(sum(e.time for e in selected),result['time'])
        if 'exposure' in result: self.assertEqual(sum(e.exposure for e in selected),result['exposure'])
        if 'scenario_totals' in result:
            totals=[sum(e.scenario_times[s] for e in selected) for s in range(len(result['scenario_totals']))]
            self.assertEqual(totals,result['scenario_totals'])
            self.assertEqual(max(totals),result['worst_time'])

    def test_parallel_edge_witness(self):
        g={'a':[Edge('b',1,5,(9,9)),Edge('b',3,1,(2,3))],'b':[Edge('c',1,0,(1,1))],'c':[]}
        for result in (budget(g,'a','c',1),robust(g,'a','c'),joint(g,'a','c',1)):
            self.assert_witness(g,result)
            self.assertEqual(result['edges'][0]['edge_index'],1)

    def test_decimal_boundary_is_binary_float(self):
        g={'a':[Edge('b',0.1,0.1,(0.1,0.2))],'b':[Edge('c',0.2,0.2,(0.2,0.1))],'c':[]}
        self.assertIsNone(budget(g,'a','c',0.3))
        self.assertIsNone(joint(g,'a','c',0.3))
        for result in (budget(g,'a','c',0.30000000000000004),robust(g,'a','c'),joint(g,'a','c',0.30000000000000004)):
            self.assert_witness(g,result)

    def test_invalid_all_units(self):
        for value in (-1,float('inf'),float('nan'),True,'1'):
            g={'a':[Edge('b',1,1,(1,1))],'b':[]}
            for func in (budget,joint):
                with self.assertRaises(ValueError): func(g,'a','b',value)
            bad={'a':[Edge('b',1,value,(1,1))],'b':[]}
            with self.assertRaises(ValueError): robust(bad,'a','b')
            bad={'a':[Edge('b',1,1,(1,value))],'b':[]}
            with self.assertRaises(ValueError): joint(bad,'a','b',2)
        for g in ({'a':[Edge('b',1,1,())],'b':[]},
                  {'a':[Edge('b',1,1,(1,))],'b':[Edge('a',1,1,(1,2))]}):
            with self.assertRaises(ValueError): robust(g,'a','b')
            with self.assertRaises(ValueError): joint(g,'a','b',2)

    def test_malformed_edges_and_nodes(self):
        for g in ({'a':[object()],'b':[]},{'a':[Edge('b',1,1,[1])],'b':[]},{'a':[Edge('x',1,1,(1,))],'b':[]},{'a':[],1:[]}):
            with self.assertRaises(ValueError): budget(g,'a','a',1)

    def test_overflow_rejected(self):
        g={'a':[Edge('b',1e308,0,(1e308,))],'b':[Edge('c',1e308,0,(1e308,))],'c':[]}
        with self.assertRaises(OverflowError): budget(g,'a','c',1)
        with self.assertRaises(OverflowError): robust(g,'a','c')
        with self.assertRaises(OverflowError): joint(g,'a','c',1)

if __name__=='__main__': unittest.main(verbosity=2)
