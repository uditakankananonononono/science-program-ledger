import unittest,numpy as np
from feasibility import solve
class FeasibilityTests(unittest.TestCase):
    def test_unique_scalar_solution(self):
        r=solve([0],[1],[1,1],[[1]],[.5],[10],[0])
        self.assertEqual(r['status'],'primal_checked');np.testing.assert_allclose(r['controls'],[[.5],[.5]])
    def test_slew_first_step_limits_reach(self):
        self.assertEqual(solve([0],[1],[1],[[1]],[2],[.5],[0])['status'],'solver_infeasible')
        r=solve([0],[.5],[1],[[1]],[2],[.5],[0]);np.testing.assert_allclose(r['controls'],[[.5]])
    def test_rank_deficient_unreachable(self):
        self.assertEqual(solve([0,0],[0,1],[1],[[1],[0]],[2],[2],[0])['status'],'solver_infeasible')
    def test_dense_map_terminal_readback(self):
        B=np.array([[1,2],[3,1.]])
        r=solve([0,0],[.3,.4],[.2,.3,.5],B,[2,2],[10,10],[0,0])
        u=np.array(r['controls']);np.testing.assert_allclose(np.array([.2,.3,.5])@u@B.T,[.3,.4],atol=1e-8)
    def test_bad_input_preserves_buffers(self):
        initial=np.zeros(1);target=np.ones(1)
        with self.assertRaises(ValueError):solve(initial,target,[0],[[1]],[1],[1],[0])
        np.testing.assert_array_equal(initial,[0]);np.testing.assert_array_equal(target,[1])
if __name__=='__main__':unittest.main()
