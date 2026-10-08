import unittest,numpy as np
from gradient_structure import construct,check
from mobility_map import assemble
class StructureTests(unittest.TestCase):
    def test_construct_and_map(self):
        G=construct([[1,2,3,4,5],[0,1,0,0,0]])
        self.assertTrue(check(G)['passes_local_structure'])
        r=assemble([1,0,0],G,np.eye(3));np.testing.assert_allclose(r['force_per_current'],[[1,0],[3,0],[4,0]])
    def test_asymmetry_and_trace_negative_controls(self):
        for row,col in ((0,1),(0,0)):
            G=construct([[1,2,3,4,5]]);G[row,col,0]+=.1
            self.assertFalse(check(G)['passes_local_structure'])
    def test_frame_rotation_preserves_structure(self):
        G=construct([[1,2,3,4,5]]);theta=.3;Q=np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1]])
        rotated=np.stack([Q@g@Q.T for g in G.transpose(2,0,1)],axis=2)
        self.assertTrue(check(rotated)['passes_local_structure'])
    def test_bad_inputs(self):
        with self.assertRaises(ValueError):construct([[np.nan,0,0,0,0]])
        with self.assertRaises(ValueError):check(construct([[1,2,3,4,5]]),np.bool_(True))
if __name__=='__main__':unittest.main()
