import random
import unittest
from routing import Edge,integrated_route,budgeted_scenario_route

def oracle(g,start,goal,budget,forbidden,penalties):
    n=len(next(e for es in g.values() for e in es).scenario_times)
    def walk(node,incoming,seen,risk,totals):
        if node==goal:
            yield max(totals)
            return
        for i,e in enumerate(g[node]):
            edge=(node,i);state=(e.target,edge);key=(incoming,edge)
            if state in seen or key in forbidden or risk+e.exposure>budget:continue
            p=penalties.get(key,0)
            new=tuple(a+b+p for a,b in zip(totals,e.scenario_times))
            yield from walk(e.target,edge,seen|{state},risk+e.exposure,new)
    return min(walk(start,None,{(start,None)},0,(0,)*n),default=None)

class IntegratedTests(unittest.TestCase):
    def test_required_revisit_and_budget(self):
        g={'a':[Edge('b',1,1,(1,2))],'b':[Edge('c',1,1,(2,1)),Edge('d',1,1,(1,1))],
           'c':[Edge('b',1,1,(1,1))],'d':[]}
        f={(('a',0),('b',1))};p={(('c',0),('b',1)):3}
        got=integrated_route(g,'a','d',4,f,p)
        self.assertEqual(got['path'],['a','b','c','b','d'])
        self.assertEqual(got['scenario_totals'],[8,8])
        self.assertIsNone(integrated_route(g,'a','d',3,f,p))

    def test_bad_inputs(self):
        g={'a':[Edge('b',1,1,(1,))],'b':[]}
        for b in (-1,True,float('nan')):
            with self.assertRaises(ValueError):integrated_route(g,'a','b',b)
        with self.assertRaises(ValueError):integrated_route(g,'a','b',2,{(('a',0),('a',0))})
        self.assertEqual(integrated_route(g,'a','a',0)['worst_time'],0)

    def test_random_oracle_and_witness(self):
        rng=random.Random(2300805)
        for case in range(150):
            g={v:[] for v in 'abcd'}
            for a in g:
                for b in g:
                    if a!=b and rng.random()<0.35:
                        g[a].append(Edge(b,0,rng.randrange(4),tuple(rng.randrange(5) for _ in range(2))))
            if not any(g.values()):g['a'].append(Edge('b',0,1,(1,1)))
            pairs=[((a,i),(e.target,j)) for a,es in g.items() for i,e in enumerate(es) for j in range(len(g[e.target]))]
            f={k for k in pairs if rng.random()<0.15};p={k:rng.randrange(4) for k in pairs if rng.random()<0.4}
            budget=rng.randrange(10)
            got=integrated_route(g,'a','d',budget,f,p)
            self.assertEqual(None if got is None else got['worst_time'],oracle(g,'a','d',budget,f,p),case)
            if got:
                ids=[(x['source'],x['edge_index']) for x in got['edges']]
                transitions=list(zip(ids,ids[1:]))
                self.assertTrue(all(k not in f for k in transitions))
                penalty=sum(p.get(k,0) for k in transitions)
                selected=[g[a][i] for a,i in ids]
                risk=sum(e.exposure for e in selected)
                totals=[sum(e.scenario_times[s] for e in selected)+penalty for s in range(2)]
                self.assertEqual(got['exposure'],risk);self.assertLessEqual(risk,budget)
                self.assertEqual(got['scenario_totals'],totals);self.assertEqual(got['turn_penalty'],penalty)
            # Without turn rules, incoming-edge expansion must preserve v3 objective.
            plain=integrated_route(g,'a','d',budget)
            prior=budgeted_scenario_route(g,'a','d',budget)
            self.assertEqual(None if plain is None else plain['worst_time'],None if prior is None else prior['worst_time'])
