import unittest,numpy as np
from mobility_map import assemble
class MapTests(unittest.TestCase):
    def test_axis_convention_dense_hand_calculation(self):
        G=np.arange(18,dtype=float).reshape(3,3,2);m=np.array([1.,2.,3.]);L=np.diag([2.,3.,4.])
        expected=np.array([[16.,22.],[52.,58.],[88.,94.]])
        r=assemble(m,G,L);np.testing.assert_allclose(r['force_per_current'],expected)
        np.testing.assert_allclose(r['velocity_per_current'],L@expected)
    def test_fixed_gradient_force_current_identity(self):
        G=np.arange(18,dtype=float).reshape(3,3,2);m=np.array([1.,2.,3.]);I=np.array([.3,-.2])
        r=assemble(m,G,np.eye(3));np.testing.assert_allclose(np.array(r['force_per_current'])@I,(G@I)@m)
    def test_zero_moment_zero_map(self):
        r=assemble(np.zeros(3),np.ones((3,3,2)),np.eye(3));np.testing.assert_array_equal(r['velocity_per_current'],np.zeros((3,2)))
    def test_invalid_mobility_and_nonfinite_rejected(self):
        for L in (np.zeros((3,3)),np.diag([-1,1,1]),np.array([[1,1,0],[0,1,0],[0,0,1]])):
            with self.assertRaises(ValueError):assemble(np.ones(3),np.ones((3,3,1)),L)
        with self.assertRaises(ValueError):assemble([np.nan,0,0],np.ones((3,3,1)),np.eye(3))
if __name__=='__main__':unittest.main()
