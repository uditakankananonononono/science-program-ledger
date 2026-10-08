import unittest
try:
    import numpy as np
    from benchmark_b1 import dijkstra,coordinate_bfs,check_path
    from mask_graph import mask_to_graph
    AVAILABLE=True
except ImportError:AVAILABLE=False

@unittest.skipUnless(AVAILABLE,'optional imaging dependencies unavailable')
class BenchmarkTests(unittest.TestCase):
    def test_comparator_and_coordinate_oracle(self):
        mask=np.array([[1,1,1],[0,0,1]],dtype=bool)
        g=mask_to_graph(mask.astype(int).tolist(),4,1,0,(1,2))
        value,path=dijkstra(g,'0,0','1,2')
        self.assertEqual(value,3);check_path(mask,path,'0,0','1,2',3)
        self.assertEqual(coordinate_bfs(mask,'0,0')['1,2'],2) # 8-neighbor oracle intentionally
    def test_bad_witness_rejected(self):
        mask=np.ones((3,3),dtype=bool)
        with self.assertRaises(AssertionError):check_path(mask,['0,0','2,2'],'0,0','2,2',1)
