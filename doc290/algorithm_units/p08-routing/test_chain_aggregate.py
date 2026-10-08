import unittest
from chain_aggregate import aggregate_chains,expand_route
from routing import Edge,exposure_budget_route,scenario_robust_route,budgeted_scenario_route

class AggregateTests(unittest.TestCase):
    def graph(self):
        return {'a':[Edge('b',2,1,(3,4))],
                'b':[Edge('a',7,4,(5,6)),Edge('c',1,0,(2,1))],
                'c':[Edge('b',9,2,(7,8))]}
    def test_asymmetric_totals_and_expansion(self):
        g=self.graph();compressed,w=aggregate_chains(g)
        self.assertEqual(compressed['a'][0],Edge('c',3,1,(5,5)))
        self.assertEqual(compressed['c'][0],Edge('a',16,6,(12,14)))
        for start,goal,budget in (('a','c',1),('c','a',6)):
            for solver in (exposure_budget_route,budgeted_scenario_route):
                original=solver(g,start,goal,budget);derived=solver(compressed,start,goal,budget)
                self.assertEqual(expand_route(derived,w),original['path'])
                for key in ('time','exposure','scenario_totals','worst_time'):
                    if key in original:self.assertEqual(original[key],derived[key])
            original=scenario_robust_route(g,start,goal);derived=scenario_robust_route(compressed,start,goal)
            self.assertEqual(original['worst_time'],derived['worst_time'])
    def test_invalid_vectors_and_overflow(self):
        g=self.graph();g['a'][0]=Edge('b',2,1,(3,))
        with self.assertRaises(ValueError):aggregate_chains(g)
        g=self.graph();g['a'][0]=Edge('b',1e308,1,(3,4));g['b'][1]=Edge('c',1e308,0,(2,1))
        with self.assertRaises(OverflowError):aggregate_chains(g)
    def test_isolate_and_empty(self):
        self.assertEqual(aggregate_chains({}),({},{}))
        g,w=aggregate_chains({'a':[]});self.assertEqual(g,{'a':[]})
        result=exposure_budget_route(g,'a','a',0)
        self.assertEqual(expand_route(result,w),['a'])
        self.assertIsNone(expand_route(None,w))

    def test_float_regrouping_changes_feasibility_documented(self):
        # b is a junction/anchor; b-c-d is compressed independently of a-b.
        g={'a':[Edge('b',1,1e16,(1,))],
           'b':[Edge('a',1,1e16,(1,)),Edge('c',1,1.0,(1,)),Edge('x',1,1e16,(1,))],
           'c':[Edge('b',1,1.0,(1,)),Edge('d',1,1.0,(1,))],
           'd':[Edge('c',1,1.0,(1,))],'x':[Edge('b',1,1e16,(1,))]}
        compressed,w=aggregate_chains(g)
        original=exposure_budget_route(g,'a','d',1e16)
        derived=exposure_budget_route(compressed,'a','d',1e16)
        self.assertIsNotNone(original)
        self.assertEqual(original['exposure'],1e16)
        self.assertIsNone(derived)
        original=budgeted_scenario_route(g,'a','d',1e16)
        derived=budgeted_scenario_route(compressed,'a','d',1e16)
        self.assertIsNotNone(original)
        self.assertIsNone(derived)
