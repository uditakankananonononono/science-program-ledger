import unittest
from fractions import Fraction as F
from solver_certificates import solver_certificates
class CandidateTests(unittest.TestCase):
    def test_and_exact_bound_sign(self):
        r=solver_certificates(['1/2']*2,[0,0],['1/2']*2,1,0)
        self.assertEqual(r['certificate']['certified_lower_on_minimum'],0)
        self.assertEqual(r['certificate']['certified_upper_on_maximum'],F(1,2))
    def test_or_upper_one_and_lower_half(self):
        r=solver_certificates(['1/2']*2,[0,0],['1/2']*2,'1/2',0)
        self.assertEqual(r['certificate']['certified_lower_on_minimum'],F(1,2));self.assertEqual(r['certificate']['certified_upper_on_maximum'],1)
    def test_nonbinary_marginal_exact_certificate(self):
        r=solver_certificates(['1/3'],['1/3'],[1],1,0)
        self.assertEqual(r['certificate']['certified_lower_on_minimum'],F(1,3));self.assertEqual(r['certificate']['certified_upper_on_maximum'],F(1,3))
    def test_nan_dual_refused(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        import numpy as np
        fake=SimpleNamespace(success=True,fun=0.,eqlin=SimpleNamespace(marginals=[0.,np.nan,0.]))
        with patch('solver_certificates.linprog',return_value=fake):
            with self.assertRaises(RuntimeError):solver_certificates(['1/2'],[0],[1],1,0)
if __name__=='__main__':unittest.main()
