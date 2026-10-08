import unittest
from fractions import Fraction as F
from primal_certificate import verify
class PrimalTests(unittest.TestCase):
    def test_exact_minimum_witness(self):
        r=verify(['1/2']*2,[0,0],['1/2']*2,1,0,[[1,0],[0,1]],['1/2']*2,[0]*5,[0,1,0,0,0])
        self.assertTrue(r['minimum_exactly_certified']);self.assertFalse(r['maximum_exactly_certified'])
    def test_exact_maximum_witness(self):
        r=verify(['1/2']*2,[0,0],['1/2']*2,1,0,[[0,0],[1,1]],['1/2']*2,[0]*5,[0,1,0,0,0])
        self.assertTrue(r['maximum_exactly_certified']);self.assertEqual(r['verified_witness_probability'],F(1,2))
    def test_nonzero_gap_not_optimality(self):
        r=verify(['1/2'],[0],[1],1,0,[[0],[1]],['1/2']*2,[-1,0,0],[2,0,0])
        self.assertFalse(r['minimum_exactly_certified']);self.assertFalse(r['maximum_exactly_certified'])
    def test_exact_marginal_and_mass_refusal(self):
        for ps in (['1/3','2/3'],[-1,2],['1/2','1/3']):
            with self.assertRaises(ValueError):verify(['1/2'],[0],[1],1,0,[[0],[1]],ps,[0]*3,[1,0,0])
if __name__=='__main__':unittest.main()
