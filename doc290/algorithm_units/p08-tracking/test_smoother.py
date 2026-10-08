import unittest
import numpy as np
from smoother import smooth

class SmootherTests(unittest.TestCase):
    def test_joint_gaussian_two_time_fixture(self):
        # x0~N(0,I), x1=x0+w, w~N(0,I), y=x1+v, v~N(0,I).
        # Direct joint conditional: Cov(x0,y)=I, Var(y)=3I.
        # x0|y mean=y/3, covariance=I-I/3=2I/3.
        y=np.array([3.,6.,9.,12.])
        means=np.stack([np.zeros(4),2*y/3])
        covs=np.stack([np.eye(4),2*np.eye(4)/3])
        sm,sc=smooth(means,covs,np.zeros((1,4)),np.array([2*np.eye(4)]),np.array([np.eye(4)]))
        np.testing.assert_allclose(sm[0],y/3)
        np.testing.assert_allclose(sc[0],2*np.eye(4)/3)
        np.testing.assert_array_equal(sm[-1],means[-1])
        np.testing.assert_array_equal(sc[-1],covs[-1])
    def test_single_record_copy(self):
        mean=np.array([[1.,2.,3.,4.]]);cov=np.array([np.eye(4)])
        sm,sc=smooth(mean,cov,np.empty((0,4)),np.empty((0,4,4)),np.empty((0,4,4)))
        np.testing.assert_array_equal(sm,mean);np.testing.assert_array_equal(sc,cov)
        sm[0,0]=999;sc[0,0,0]=999
        self.assertEqual(mean[0,0],1);self.assertEqual(cov[0,0,0],1)
    def test_prediction_only_identity(self):
        means=np.zeros((3,4));covs=np.array([np.eye(4),2*np.eye(4),3*np.eye(4)])
        sm,sc=smooth(means,covs,np.zeros((2,4)),covs[1:],np.array([np.eye(4)]*2))
        np.testing.assert_allclose(sm,means);np.testing.assert_allclose(sc,covs)
    def test_rejections_leave_inputs_unchanged(self):
        means=np.zeros((2,4));covs=np.array([np.eye(4)]*2);before=covs.copy()
        for predicted in (np.array([np.zeros((4,4))]),np.array([np.diag([-1,1,1,1])])):
            with self.assertRaises(ValueError):smooth(means,covs,np.zeros((1,4)),predicted,np.array([np.eye(4)]))
        with self.assertRaises(ValueError):smooth(means,covs,np.zeros((2,4)),np.array([np.eye(4)]),np.array([np.eye(4)]))
        # Internally inconsistent records would yield negative smoothed covariance.
        with self.assertRaises(ValueError):smooth(means,np.array([5*np.eye(4),np.eye(4)]),np.zeros((1,4)),np.array([2*np.eye(4)]),np.array([np.eye(4)]))
        np.testing.assert_array_equal(covs,before)

if __name__=='__main__':unittest.main(verbosity=2)
