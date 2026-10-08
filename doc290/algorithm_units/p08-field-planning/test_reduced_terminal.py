import unittest,numpy as np
from reduced_terminal import solve_reduced
class ReducedTests(unittest.TestCase):
    def test_rectangular_redundancy(self):
        r=solve_reduced([0],[1],[1,1],[[1,1]],[1,1],[1,1],[0,0])
        self.assertEqual(r['status'],'primal_checked');self.assertEqual(r['lp_variables'],2)
        self.assertAlmostEqual(np.array(r['trajectory'])[-1,0],1)
    def test_rank_deficient_unreachable(self):
        r=solve_reduced([0,0],[1,-1],[1],[[1],[1]],[1],[1],[0])
        self.assertEqual(r['status'],'solver_infeasible')
    def test_zero_slew_interval(self):
        r=solve_reduced([0],[1],[1,1],[[1]],[1],[0],[.5])
        np.testing.assert_allclose(r['controls'],[[.5],[.5]])
    def test_corrupted_solver_nan_rejected(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        with patch('reduced_terminal.linprog',return_value=SimpleNamespace(status=0,success=True,x=[np.nan])):
            with self.assertRaises(RuntimeError):solve_reduced([0],[1],[1],[[1]],[1],[1],[0])
if __name__=='__main__':unittest.main()
