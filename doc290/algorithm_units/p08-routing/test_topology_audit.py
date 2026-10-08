import unittest
from routing import Edge
from topology_audit import audit_topology
from mask_graph import mask_to_graph

class TopologyTests(unittest.TestCase):
    def graph(self,nodes,pairs):
        g={n:[] for n in nodes}
        for a,b in pairs:g[a].append(Edge(b,1,0));g[b].append(Edge(a,1,0))
        return g
    def test_chain_and_isolate(self):
        g=self.graph('abcd',[('a','b'),('b','c')]);r=audit_topology(g)
        self.assertEqual(r,dict(vertices=4,undirected_edges=2,components=2,isolated_vertices=1,endpoints=2,branch_vertices=0,cycle_rank=0))
    def test_loop_and_branch(self):
        g=self.graph('abcd',[('a','b'),('b','c'),('c','a'),('a','d')]);r=audit_topology(g)
        self.assertEqual(r['cycle_rank'],1);self.assertEqual(r['branch_vertices'],1)
        self.assertEqual(r['endpoints'],1)
    def test_invalid_representation(self):
        for g in ({'a':[Edge('b',1,0)],'b':[]},{'a':[Edge('a',1,0)]},
                  {'a':[Edge('b',1,0),Edge('b',1,0)],'b':[Edge('a',1,0)]}):
            with self.assertRaises(ValueError):audit_topology(g)
    def test_all_3x3_masks_edge_formula(self):
        for bits in range(512):
            mask=[[(bits>>(3*r+c))&1 for c in range(3)] for r in range(3)]
            for conn in (4,8):
                r=audit_topology(mask_to_graph(mask,conn,1,0))
                self.assertEqual(r['vertices'],bits.bit_count())
                # Independent pairwise edge oracle, not adjacency counts from extractor.
                points=[(y,x) for y in range(3) for x in range(3) if mask[y][x]]
                pairs=sum(1 for i,(y,x) in enumerate(points) for a,b in points[i+1:]
                          if (abs(y-a)+abs(x-b)==1 if conn==4 else max(abs(y-a),abs(x-b))==1))
                self.assertEqual(r['undirected_edges'],pairs)
                self.assertGreaterEqual(r['cycle_rank'],0)
    def test_empty(self):
        self.assertEqual(audit_topology({})['components'],0)
