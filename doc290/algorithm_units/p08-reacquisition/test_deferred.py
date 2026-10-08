import unittest,numpy as np
from deferred import resolve
class DeferredTests(unittest.TestCase):
    def test_obvious_corrupt_reacquisition_rejected(self):
        r=resolve(np.zeros(4),np.eye(4),.01,.1,[100,100],.01*np.eye(2),.1,[0,0],.01*np.eye(2))
        self.assertFalse(r['accepted_first']);np.testing.assert_allclose(r['provisional']['state'],0)
    def test_consistent_return_accepted(self):
        r=resolve(np.zeros(4),np.eye(4),.01,.1,[1,1],.01*np.eye(2),.1,[1,1],.01*np.eye(2))
        self.assertTrue(r['accepted_first']);self.assertEqual(r['latency_observations'],1)
    def test_transactional_bad_confirmation(self):
        state=np.zeros(4);P=np.eye(4);before=P.copy()
        with self.assertRaises(ValueError):resolve(state,P,.01,.1,[1,1],np.eye(2),.1,[float('nan'),0],np.eye(2))
        np.testing.assert_array_equal(P,before);np.testing.assert_array_equal(state,0)
    def test_score_matches_direct_density(self):
        from kalman import ConstantVelocity
        state=np.zeros(4);P=np.eye(4);R=np.eye(2);z=np.array([2.,3.])
        r=resolve(state,P,.25,.1,[1,1],R,.2,z,R)
        branch=ConstantVelocity(state,P,.25);branch.step(.1);p=branch.step(.2)
        S=p['covariance'][:2,:2]+R;e=z-p['state'][:2]
        expected=.5*(np.log(np.linalg.det(S))+e@np.linalg.inv(S)@e+2*np.log(2*np.pi))
        self.assertAlmostEqual(r['confirmation_nll_reject_accept'][0],expected)
if __name__=='__main__':unittest.main()
