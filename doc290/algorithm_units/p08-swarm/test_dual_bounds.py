import unittest
from fractions import Fraction as F
from dual_bounds import certify
class DualTests(unittest.TestCase):
    def test_exact_frechet_full_payload_duals(self):
        r=certify(['1/2']*2,[0,0],['1/2']*2,1,0,[0,0,0,0,0],[0,1,0,0,0])
        self.assertEqual(r['certified_lower_on_minimum'],0);self.assertEqual(r['certified_upper_on_maximum'],F(1,2));self.assertEqual(r['independent_feasible_probability'],F(1,4))
    def test_candidate_violation_repaired_exactly(self):
        r=certify(['1/2'],[0],[1],1,0,['1/10',1,0],['-1/10',1,0])
        self.assertEqual(r['lower_normalization_shift'],F(1,10));self.assertEqual(r['upper_normalization_shift'],F(1,10))
        self.assertEqual(r['certified_lower_on_minimum'],F(1,2));self.assertEqual(r['certified_upper_on_maximum'],F(1,2))
    def test_loose_candidates_do_not_claim_optimality(self):
        r=certify(['1/2'],[0],[1],1,0,[-5,0,0],[5,0,0])
        self.assertEqual(r['certified_lower_on_minimum'],-5);self.assertEqual(r['certified_upper_on_maximum'],5)
    def test_float_candidates_and_dimension_refused(self):
        for lower in ([0.,0,0],[0,0]):
            with self.assertRaises(ValueError):certify(['1/2'],[0],[1],1,0,lower,[1,0,0])
if __name__=='__main__':unittest.main()
