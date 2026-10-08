import unittest
from chain_compress import compress_chains
from mask_graph import mask_to_graph
from routing import Edge

class CompressionTests(unittest.TestCase):
    def graph(self,nodes,pairs):
        g={v:[] for v in nodes}
        for a,b in pairs:g[a].append(Edge(b,1,0));g[b].append(Edge(a,1,0))
        return g
    def check(self,g):
        result=compress_chains(g)
        edges=[]
        for chain in result['chains']:
            p=chain['pixel_path']
            self.assertEqual(chain['source'],p[0]);self.assertEqual(chain['target'],p[-1])
            self.assertEqual(chain['edge_steps'],len(p)-1)
            self.assertTrue(all(len(g[v])==2 and v not in result['anchors'] for v in p[1:-1]))
            edges.extend(frozenset((a,b)) for a,b in zip(p,p[1:]))
        expected={frozenset((v,e.target)) for v,es in g.items() for e in es}
        self.assertEqual(set(edges),expected);self.assertEqual(len(edges),len(expected))
        return result
    def test_chain_cycle_and_isolate(self):
        r=self.check(self.graph('abcde',[('a','b'),('b','c'),('c','a')]))
        self.assertEqual(r['anchors'],['a','d','e'])
        self.assertEqual(len(r['chains']),1);self.assertEqual(r['chains'][0]['edge_steps'],3)
        self.assertEqual(r['chains'][0]['source'],r['chains'][0]['target'])
        r=self.check(self.graph('abcd',[('a','b'),('b','c'),('c','d')]))
        self.assertEqual(r['anchors'],['a','d']);self.assertEqual(len(r['chains']),1)
    def test_exhaustive_masks(self):
        for bits in range(512):
            mask=[[(bits>>(3*y+x))&1 for x in range(3)] for y in range(3)]
            for conn in (4,8):self.check(mask_to_graph(mask,conn,1,0))
    def test_empty_and_invalid(self):
        self.assertEqual(self.check({})['chains'],[])
        with self.assertRaises(ValueError):compress_chains({'a':[Edge('b',1,0)],'b':[]})
