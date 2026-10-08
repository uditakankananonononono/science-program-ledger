import unittest
from chain_costs import serialize_chain_costs
from routing import Edge
from mask_graph import mask_to_graph

class ChainCostTests(unittest.TestCase):
    def check(self,g):
        result=serialize_chain_costs(g)
        recovered={}
        for ch in result['chains']:
            for direction in ch['directions']:
                steps=direction['steps']
                self.assertEqual(direction['source'],steps[0]['source'])
                self.assertEqual(direction['target'],steps[-1]['target'])
                for s in steps:
                    key=(s['source'],s['target'])
                    self.assertNotIn(key,recovered)
                    recovered[key]=(s['time'],s['exposure'],tuple(s['scenario_times']))
        expected={(v,e.target):(e.time,e.exposure,e.scenario_times) for v,es in g.items() for e in es}
        self.assertEqual(recovered,expected)
        return result
    def test_asymmetric_directed_costs(self):
        g={'a':[Edge('b',2,1,(3,4))],'b':[Edge('a',7,4,(5,6)),Edge('c',1,0,(2,1))],
           'c':[Edge('b',9,2,(7,8))]}
        r=self.check(g)
        self.assertEqual(len(r['chains']),1)
        self.assertEqual(r['chains'][0]['directions'][0]['steps'][0]['time'],2)
        self.assertEqual(r['chains'][0]['directions'][1]['steps'][0]['time'],9)
    def test_cycle_and_isolate(self):
        g=mask_to_graph([[1,1],[1,1]],4,1,2,(3,4))
        r=self.check(g)
        self.assertEqual(len(r['chains']),1)
        self.assertEqual(r['chains'][0]['source'],r['chains'][0]['target'])
        self.assertEqual(self.check({'a':[]})['chains'],[])
    def test_all_small_masks(self):
        for bits in range(512):
            mask=[[(bits>>(3*r+c))&1 for c in range(3)] for r in range(3)]
            for conn in (4,8):self.check(mask_to_graph(mask,conn,1,2,(3,4)))
