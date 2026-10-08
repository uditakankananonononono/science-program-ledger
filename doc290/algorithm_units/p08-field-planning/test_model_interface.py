import unittest,numpy as np
from model_interface import unpack_upstream,require_workspace
class InterfaceTests(unittest.TestCase):
    def test_distinct_axis_order(self):
        G=unpack_upstream([[1,2,3,4,5]])
        np.testing.assert_array_equal(G[:,:,0],[[1,2,3],[2,4,5],[3,5,-5]])
    def test_each_packed_axis_separately(self):
        matrices=[[[1,0,0],[0,0,0],[0,0,-1]],[[0,1,0],[1,0,0],[0,0,0]],[[0,0,1],[0,0,0],[1,0,0]],[[0,0,0],[0,1,0],[0,0,-1]],[[0,0,0],[0,0,1],[0,1,0]]]
        G=unpack_upstream(np.eye(5))
        for i,expected in enumerate(matrices):np.testing.assert_array_equal(G[:,:,i],expected)
    def test_inclusive_workspace_and_immediate_outside(self):
        bounds=np.array([[-.01,.01]]*3)
        for p in ([-.01,.01,0],[0,0,0]):np.testing.assert_array_equal(require_workspace(p,bounds),p)
        with self.assertRaises(ValueError):require_workspace([np.nextafter(.01,np.inf),0,0],bounds)
    def test_invalid_and_buffer_copy(self):
        p=np.zeros(3);b=np.array([[-1,1]]*3);out=require_workspace(p,b);out[0]=.5;np.testing.assert_array_equal(p,0)
        with self.assertRaises(ValueError):require_workspace([np.nan,0,0],b)
        with self.assertRaises(ValueError):require_workspace(p,[[1,-1]]*3)
        with self.assertRaises(ValueError):unpack_upstream([[1,2,3,4,np.inf]])
if __name__=='__main__':unittest.main()
