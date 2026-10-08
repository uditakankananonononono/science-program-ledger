import random,unittest
from mask_graph import mask_to_graph,graph_payload
from runner import solve

class MaskGraphTests(unittest.TestCase):
    def test_chain_runner(self):
        g=mask_to_graph([[1,1,1]],4,2,1,(2,3))
        result=solve({'graph':graph_payload(g),'method':'integrated','start':'0,0','goal':'0,2','budget':2})
        self.assertEqual(result['result']['path'],['0,0','0,1','0,2'])
        self.assertEqual(result['result']['scenario_totals'],[4,6])
    def test_diagonal_choice(self):
        mask=[[1,0],[0,1]]
        self.assertEqual(mask_to_graph(mask,4,1,0)['0,0'],[])
        g=mask_to_graph(mask,8,1,0)
        self.assertEqual(g['0,0'][0].target,'1,1')
    def test_junction_and_disconnected(self):
        g=mask_to_graph([[0,1,0],[1,1,1],[0,1,0]],4,1,1)
        self.assertEqual(len(g['1,1']),4)
        self.assertEqual(sum(map(len,g.values())),8)
        self.assertEqual(mask_to_graph([[0]],4,1,1),{})
        self.assertEqual(mask_to_graph([[1]],4,1,1),{'0,0':[]})
    def test_invalid(self):
        for mask in ([],[[]],[[1],[1,0]],[[True]],[[2]],[[0.0]],'1'):
            with self.assertRaises(ValueError):mask_to_graph(mask,4,1,0)
        for connectivity in (True,4.0,6):
            with self.assertRaises(ValueError):mask_to_graph([[1]],connectivity,1,0)
        with self.assertRaises(ValueError):mask_to_graph([[0]],4,-1,0)
    def test_random_pairwise_adjacency_oracle(self):
        rng=random.Random(2300806)
        for case in range(200):
            mask=[[rng.randrange(2) for _ in range(5)] for _ in range(4)]
            points=[(r,c) for r,row in enumerate(mask) for c,x in enumerate(row) if x]
            for conn in (4,8):
                g=mask_to_graph(mask,conn,1,2,(3,4))
                actual={(node,e.target) for node,es in g.items() for e in es}
                expected={(f'{a},{b}',f'{c},{d}') for a,b in points for c,d in points
                          if (abs(a-c)+abs(b-d)==1 if conn==4 else max(abs(a-c),abs(b-d))==1)}
                self.assertEqual(actual,expected,case)
                self.assertEqual(len(g),len(points))
