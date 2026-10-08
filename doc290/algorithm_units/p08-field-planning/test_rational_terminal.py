import unittest
from fractions import Fraction as F
from rational_terminal import solve_terminal
class TerminalTests(unittest.TestCase):
    def test_dense_pivot_swap_reachable(self):
        r=solve_terminal([0,0],[1,2],[1,1],[[0,2],[1,1]],[2,2],[1,1],[0,0])
        self.assertEqual(r['status'],'exact_model_reachable');self.assertEqual(r['unique_integrals'],[F(3,2),F(1,2)])
        self.assertEqual(r['terminal'],[1,2])
    def test_exact_outside_unreachable(self):
        r=solve_terminal([0],['1.5000000000000000000001'],[1,1],[[1]],[2],['1/2'],[0])
        self.assertEqual(r['status'],'exact_model_unreachable');self.assertEqual(len(r['violations']),1)
    def test_singular_and_rectangular_unsupported(self):
        for B in ([[1,1],[1,1]],[[1],[1]]):
            with self.assertRaises(ValueError):solve_terminal([0,0],[1,1],[1],B,[1,1],[1,1],[0,0])
    def test_invalid_bounds_not_unreachable(self):
        with self.assertRaises(ValueError):solve_terminal([0],[10],[0],[[1]],[1],[1],[0])
if __name__=='__main__':unittest.main()
