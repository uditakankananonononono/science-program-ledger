import random
import unittest
from routing import Edge, exposure_budget_route, scenario_robust_route


def enumerate_paths(g, node, goal, visited=(), edges=()):
    if node == goal:
        yield edges
        return
    for e in g[node]:
        if e.target not in visited + (node,):
            yield from enumerate_paths(g, e.target, goal, visited + (node,), edges + (e,))

class Tests(unittest.TestCase):
    def test_budget_tradeoff(self):
        g={'a':[Edge('b',1,5),Edge('c',3,1)],'b':[Edge('d',1,5)],'c':[Edge('d',3,1)],'d':[]}
        self.assertEqual(exposure_budget_route(g,'a','d',2)['time'],6)
        self.assertEqual(exposure_budget_route(g,'a','d',10)['time'],2)
        self.assertIsNone(exposure_budget_route(g,'a','d',1))

    def test_correlated_scenarios_not_edgewise_worst(self):
        g={'a':[Edge('b',0,0,(10,0)),Edge('c',0,0,(6,6))],
           'b':[Edge('d',0,0,(0,10))],'c':[Edge('d',0,0,(6,6))],'d':[]}
        self.assertEqual(scenario_robust_route(g,'a','d')['path'],['a','b','d'])
        self.assertEqual(scenario_robust_route(g,'a','d')['worst_time'],10)

    def test_zero_cycles(self):
        g={'a':[Edge('b',0,0,(0,0))],'b':[Edge('a',0,0,(0,0)),Edge('c',1,1,(1,1))],'c':[]}
        self.assertEqual(exposure_budget_route(g,'a','c',1)['time'],1)
        self.assertEqual(scenario_robust_route(g,'a','c')['worst_time'],1)

    def test_invalid(self):
        for value in (-1,float('nan'),float('inf'),True):
            g={'a':[Edge('b',value,0,(1,))],'b':[]}
            with self.assertRaises(ValueError): exposure_budget_route(g,'a','b',1)
            with self.assertRaises(ValueError): scenario_robust_route(g,'a','b')
        with self.assertRaises(ValueError): scenario_robust_route({'a':[Edge('b',1,1)],'b':[]},'a','b')
        with self.assertRaises(ValueError): exposure_budget_route({'a':[]},'a','x',1)

    def test_identity_and_disconnected(self):
        g={'a':[Edge('b',1,1,(1,2))],'b':[],'c':[]}
        self.assertEqual(exposure_budget_route(g,'a','a',0)['path'],['a'])
        self.assertEqual(scenario_robust_route(g,'a','a')['worst_time'],0)
        self.assertIsNone(exposure_budget_route(g,'a','c',100))
        self.assertIsNone(scenario_robust_route(g,'a','c'))

    def test_random_exhaustive_oracle(self):
        rng=random.Random(2300801)
        for case in range(150):
            nodes=[str(i) for i in range(6)]
            g={v:[] for v in nodes}
            for a in nodes:
                for b in nodes:
                    if a!=b and rng.random()<0.30:
                        g[a].append(Edge(b,rng.randrange(6),rng.randrange(6),tuple(rng.randrange(6) for _ in range(3))))
            if not any(g.values()):
                g['0'].append(Edge('1',1,1,(1,1,1)))
            paths=list(enumerate_paths(g,'0','5'))
            budget=rng.randrange(12)
            feasible=[sum(e.time for e in p) for p in paths if sum(e.exposure for e in p)<=budget]
            got=exposure_budget_route(g,'0','5',budget)
            self.assertEqual(None if got is None else got['time'], min(feasible) if feasible else None,case)
            vals=[max(sum(e.scenario_times[s] for e in p) for s in range(3)) for p in paths]
            got=scenario_robust_route(g,'0','5')
            self.assertEqual(None if got is None else got['worst_time'],min(vals) if vals else None,case)

if __name__=='__main__': unittest.main(verbosity=2)
