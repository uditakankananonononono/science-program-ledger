import unittest,numpy as np
from minimax import minimax_terminal
class MinimaxTests(unittest.TestCase):
    def test_two_gains_analytic_optimum(self):
        r=minimax_terminal([0],[1],[[[1]],[[2]]],[2],[2],[0],[[1],[1]])
        np.testing.assert_allclose(r['controls'],[[2/3]],atol=1e-8)
        self.assertAlmostEqual(r['worst_terminal_coordinate_error'],1/3)
    def test_slew_limited_optimum(self):
        r=minimax_terminal([0],[1],[[[1]]],[2],[.5],[0],[[1]])
        self.assertAlmostEqual(r['worst_terminal_coordinate_error'],.5)
    def test_zero_error_feasible(self):
        r=minimax_terminal([0],[1],[[[1]],[[2]]],[2],[2],[0],[[1],[2]])
        self.assertAlmostEqual(r['worst_terminal_coordinate_error'],0)
    def test_corrupt_successful_solver_epigraph_rejected(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        for bound in (float('nan'),float('inf'),-1.,-.000000000001):
            with self.subTest(bound=bound):
                fake=SimpleNamespace(status=0,success=True,x=np.array([1.,bound]))
                with patch('minimax.linprog',return_value=fake):
                    with self.assertRaises(RuntimeError):minimax_terminal([0],[1],[[[1]]],[2],[2],[0],[[1]])
if __name__=='__main__':unittest.main()
