import unittest
from routing import Edge
from anchor_route import route_integer_anchors

class AnchorTests(unittest.TestCase):
    def graph(self):
        return {'a':[Edge('b',2,1,(3,4))],
                'b':[Edge('a',7,4,(5,6)),Edge('c',1,0,(2,1))],
                'c':[Edge('b',9,2,(7,8))]}
    def test_objectives_and_expansion(self):
        for method,budget in [('budget',1),('scenario',None),('budget-scenario',1)]:
            result=route_integer_anchors(self.graph(),'a','c',method,budget)
            self.assertEqual(result['expanded_pixel_path'],['a','b','c'])
            self.assertEqual(result['compressed_result']['path'],['a','c'])
    def test_nonanchor_and_float_rejected(self):
        with self.assertRaises(ValueError):route_integer_anchors(self.graph(),'b','c','budget',1)
        for value in (1.0,True):
            g=self.graph();g['a'][0]=Edge('b',value,1,(3,4))
            with self.assertRaises(ValueError):route_integer_anchors(g,'a','c','budget',1)
    def test_budget_and_method_rejected(self):
        for value in (-1,True,1.0,None):
            with self.assertRaises(ValueError):route_integer_anchors(self.graph(),'a','c','budget',value)
        with self.assertRaises(ValueError):route_integer_anchors(self.graph(),'a','c','scenario',1)
        with self.assertRaises(ValueError):route_integer_anchors(self.graph(),'a','c','integrated',1)
    def test_infeasible_and_identity(self):
        r=route_integer_anchors(self.graph(),'a','c','budget',0)
        self.assertIsNone(r['compressed_result']);self.assertIsNone(r['expanded_pixel_path'])
        self.assertEqual(route_integer_anchors({'a':[]},'a','a','budget',0)['expanded_pixel_path'],['a'])
