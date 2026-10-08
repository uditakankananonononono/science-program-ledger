import unittest
from fractions import Fraction as F
from integral_lift import lift
class LiftTests(unittest.TestCase):
    def test_midpoint_exact(self):
        r=lift([1,1],[2],['1/2'],[0],['3/4'])
        self.assertEqual(r['controls'],[[F(1,4)],[F(1,2)]]);self.assertEqual(r['mixing_weights'],[F(3,4)])
    def test_degenerate_zero_slew(self):
        r=lift(['1/3','2/3'],[1],[0],['1/2'],['1/2'])
        self.assertEqual(r['controls'],[[F(1,2)],[F(1,2)]])
        with self.assertRaises(ValueError):lift([1],[1],[0],['1/2'],[0])
    def test_independent_mixes_and_terminal_identity(self):
        r=lift([1,1],[2,2],['1/2','1/2'],[0,0],['3/4','-3/4'])
        B=[[1,2],[3,-1]];end=[sum(b*z for b,z in zip(row,r['replayed_integrals'])) for row in B]
        expected=[sum(t*sum(b*u for b,u in zip(row,control)) for t,control in zip([1,1],r['controls'])) for row in B]
        self.assertEqual(end,expected)
    def test_outside_and_float_refused(self):
        for z in ('1.50000000000000000000001',.5):
            with self.assertRaises(ValueError):lift([1,1],[2],['1/2'],[0],[z])
if __name__=='__main__':unittest.main()
