import unittest,numpy as np
from corridor import solve_corridor
class CorridorTests(unittest.TestCase):
    def call(self,lower,upper,target=1):
        return solve_corridor([0],[target],[1,1],[[1]],[1],[10],[0],lower,upper)
    def test_forced_intermediate_node(self):
        r=self.call([[0],[.2],[1]],[[0],[.2],[1]])
        self.assertEqual(r['status'],'primal_checked');np.testing.assert_allclose(r['controls'],[[.2],[.8]])
        self.assertLessEqual(r['residuals']['node_corridor_violation'],1e-8)
    def test_intermediate_reach_infeasible(self):
        self.assertEqual(self.call([[0],[1.1],[1]],[[0],[1.2],[1]])['status'],'solver_infeasible')
    def test_initial_and_terminal_outside(self):
        self.assertEqual(self.call([[.1],[-1],[-1]],[[.2],[2],[2]])['status'],'initial_node_outside_corridor')
        self.assertEqual(self.call([[0],[-1],[0]],[[0],[2],[.5]])['status'],'solver_infeasible')
    def test_bad_boxes_rejected(self):
        for lo,hi in (([[0]],[[1]]),([[0],[1],[0]],[[0],[0],[1]]),([[0],[float('nan')],[0]],[[0],[1],[1]])):
            with self.assertRaises(ValueError):self.call(lo,hi)
    def test_dense_map_node_reconstruction(self):
        B=np.array([[1.,2.],[2.,-1.]])
        expected=np.array([[.2,.1],[-.1,.2]])
        times=np.array([.4,.6]);path=np.vstack([np.zeros(2),np.cumsum(times[:,None]*(expected@B.T),axis=0)])
        r=solve_corridor([0,0],path[-1],times,B,[1,1],[10,10],[0,0],path,path)
        np.testing.assert_allclose(r['trajectory'],path,atol=1e-8)
        np.testing.assert_allclose(r['controls'],expected,atol=1e-8)
if __name__=='__main__':unittest.main()
