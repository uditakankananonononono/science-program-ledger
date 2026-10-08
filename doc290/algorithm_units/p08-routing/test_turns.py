import random
import unittest
from routing import Edge, turn_constrained_route


def oracle(g,start,goal,forbidden,penalties):
    # Enumerate simple expanded-state paths, not simple vertex paths.
    def visit(node,incoming,seen,cost):
        if node==goal:
            yield cost
            return
        for i,e in enumerate(g[node]):
            outgoing=(node,i)
            key=(incoming,outgoing)
            state=(e.target,outgoing)
            if state in seen or key in forbidden:
                continue
            yield from visit(e.target,outgoing,seen|{state},cost+e.time+penalties.get(key,0))
    return min(visit(start,None,{(start,None)},0),default=None)

class TurnTests(unittest.TestCase):
    def test_forbidden_and_penalty(self):
        g={'a':[Edge('b',1,0),Edge('c',3,0)],'b':[Edge('d',1,0)],'c':[Edge('d',1,0)],'d':[]}
        key=(('a',0),('b',0))
        self.assertEqual(turn_constrained_route(g,'a','d',forbidden={key})['path'],['a','c','d'])
        self.assertEqual(turn_constrained_route(g,'a','d',penalties={key:5})['time'],4)
        self.assertEqual(turn_constrained_route(g,'a','d',penalties={key:1})['turn_penalty'],1)

    def test_vertex_revisit_can_be_required(self):
        g={'a':[Edge('b',1,0)],'b':[Edge('c',1,0),Edge('d',1,0)],'c':[Edge('b',1,0)],'d':[]}
        key=(('a',0),('b',1))
        got=turn_constrained_route(g,'a','d',forbidden={key})
        self.assertEqual(got['path'],['a','b','c','b','d'])
        self.assertEqual(got['time'],4)

    def test_parallel_identity(self):
        g={'a':[Edge('b',1,0),Edge('b',2,0)],'b':[Edge('c',1,0)],'c':[]}
        got=turn_constrained_route(g,'a','c',forbidden={(('a',0),('b',0))})
        self.assertEqual(got['edges'][0]['edge_index'],1)
        self.assertEqual(got['time'],3)

    def test_invalid_and_empty(self):
        g={'a':[Edge('b',1,0)],'b':[]}
        for key in ((('x',0),('b',0)),(('a',0),('a',0))):
            with self.assertRaises(ValueError):turn_constrained_route(g,'a','b',forbidden={key})
        for value in (-1,float('inf'),True):
            h={'a':[Edge('b',1,0)],'b':[Edge('c',1,0)],'c':[]}
            with self.assertRaises(ValueError):turn_constrained_route(h,'a','c',penalties={(('a',0),('b',0)):value})
        self.assertEqual(turn_constrained_route({'a':[]},'a','a')['time'],0)
        self.assertIsNone(turn_constrained_route({'a':[],'b':[]},'a','b'))

    def test_random_expanded_state_oracle(self):
        rng=random.Random(2300802)
        for case in range(100):
            nodes=list('abcd')
            g={v:[] for v in nodes}
            for a in nodes:
                for b in nodes:
                    if a!=b and rng.random()<0.35:
                        g[a].append(Edge(b,rng.randrange(5),0))
            pairs=[((a,i),(e.target,j)) for a in nodes for i,e in enumerate(g[a]) for j in range(len(g[e.target]))]
            forbidden={key for key in pairs if rng.random()<0.2}
            penalties={key:rng.randrange(4) for key in pairs if rng.random()<0.4}
            expected=oracle(g,'a','d',forbidden,penalties)
            got=turn_constrained_route(g,'a','d',forbidden,penalties)
            self.assertEqual(None if got is None else got['time'],expected,case)
            if got:
                ids=[(e['source'],e['edge_index']) for e in got['edges']]
                turns=list(zip(ids,ids[1:]))
                self.assertTrue(all(key not in forbidden for key in turns))
                edge_time=sum(g[a][i].time for a,i in ids)
                penalty=sum(penalties.get(key,0) for key in turns)
                self.assertEqual(got['time'],edge_time+penalty)
                self.assertEqual(got['turn_penalty'],penalty)

if __name__=='__main__':unittest.main(verbosity=2)
