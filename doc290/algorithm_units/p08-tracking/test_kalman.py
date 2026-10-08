import unittest
import numpy as np
from kalman import ConstantVelocity

class KalmanTests(unittest.TestCase):
    def test_prediction_closed_form(self):
        f=ConstantVelocity([1,2,3,4],np.zeros((4,4)),2)
        r=f.step(2)
        np.testing.assert_allclose(r['state'],[7,10,3,4])
        expected=np.array([[16/3,0,4,0],[0,16/3,0,4],[4,0,4,0],[0,4,0,4]])
        np.testing.assert_allclose(r['covariance'],expected)
        self.assertFalse(r['observed']);self.assertIsNone(r['nis'])
    def test_update_scalar_fixture(self):
        f=ConstantVelocity([0,0,0,0],np.diag([1,1,0,0]),0)
        r=f.step(1,[2,4],np.eye(2))
        np.testing.assert_allclose(r['state'],[1,2,0,0])
        np.testing.assert_allclose(r['covariance'],np.diag([0.5,0.5,0,0]))
        self.assertAlmostEqual(r['nis'],10)
    def test_process_partition_identity(self):
        a=ConstantVelocity([1,2,3,4],np.eye(4),0.3)
        b=ConstantVelocity([1,2,3,4],np.eye(4),0.3)
        a.step(2);b.step(.7);b.step(1.3)
        np.testing.assert_allclose(a.state,b.state)
        np.testing.assert_allclose(a.covariance,b.covariance,atol=1e-12)
    def test_variable_dt_dropout_psd(self):
        rng=np.random.default_rng(80803)
        f=ConstantVelocity([0,0,1,1],np.eye(4),.1)
        for i in range(100):
            r=f.step(float(rng.uniform(.01,2)),None if i%3==0 else rng.normal(size=2),None if i%3==0 else np.diag([.1,.2]))
            np.testing.assert_allclose(r['covariance'],r['covariance'].T,atol=1e-12)
            self.assertGreaterEqual(np.linalg.eigvalsh(r['covariance']).min(),-1e-12)
    def test_invalid_inputs_no_mutation(self):
        f=ConstantVelocity([0,0,0,0],np.eye(4),0)
        for dt,z,R in [(0,None,None),(True,None,None),(1,[1,2],np.zeros((2,2))),(1,None,np.eye(2)),(1,[float('nan'),0],np.eye(2))]:
            state=f.state.copy();P=f.covariance.copy()
            with self.assertRaises(ValueError):f.step(dt,z,R)
            np.testing.assert_array_equal(f.state,state);np.testing.assert_array_equal(f.covariance,P)
        with self.assertRaises(ValueError):ConstantVelocity([0]*4,np.diag([-1,1,1,1]),0)
        with self.assertRaises(ValueError):ConstantVelocity([0]*4,np.eye(4),-1)

if __name__=='__main__':unittest.main(verbosity=2)
