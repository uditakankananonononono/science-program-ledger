import unittest,json,os
from unittest.mock import patch
import numpy as np
from audit import snapshot,encode,finite,run_case,Invalid
class Toy:
    def __init__(self,state,P,q):self.state=state.copy();self.covariance=P.copy()
    def step(self,dt,z,R):
        out=self.state.copy();out[:2]+=dt*out[2:];self.state=out
        return {'state':out.copy(),'covariance':self.covariance.copy(),'innovation':None,'nis':None,'observed':False}
class Failing(Toy):
    def step(self,dt,z,R):raise ValueError('toy refusal')
class MutatingFailure(Toy):
    def step(self,dt,z,R):self.state[0]=9;raise ValueError('toy mutation')
class ConstructorFailure:
    def __init__(self,*a):raise ValueError('toy constructor refusal')
class Development(unittest.TestCase):
    def base(self):return {'name':'development','state':[1,2,3,4],'P':[[0]*4 for _ in range(4)],'q':0,'dt':2,'measurement':None,'R':None,'inject':None,'expected':'REFUSE'}
    def test_snapshots_genuine(self):
        a=np.arange(8).reshape(2,4)[:,::2];s=snapshot(a);a[0,0]=99;self.assertNotEqual(s,snapshot(a));self.assertEqual(s['strides'],[32,16]);self.assertEqual(len(bytes.fromhex(s['bytes_hex'])),32)
    def test_nonfinite_serialization(self):
        v={'x':np.array([np.nan,np.inf,-np.inf,1.])};self.assertFalse(finite(v['x']));s=json.dumps(encode(v),allow_nan=False);self.assertIn('NaN',s);self.assertIn('+Inf',s)
    def test_failed_atomic_not_constructor(self):
        a=run_case(self.base(),Failing);self.assertTrue(a['success']);self.assertTrue(a['atomic_preserved'])
        b=run_case(self.base(),MutatingFailure);self.assertFalse(b['success']);self.assertFalse(b['atomic_preserved'])
        c=run_case(self.base(),ConstructorFailure);self.assertFalse(c['success']);self.assertIsNone(c['atomic_preserved']);self.assertEqual(c['stage'],'constructor')
    def test_valid_toy(self):
        c=self.base();c['expected']='VALID';c['oracle']={'state':[7,10,3,4],'P':[[0]*4 for _ in range(4)],'innovation':None,'nis':None};self.assertTrue(run_case(c,Toy)['success'])
    def test_finite_unexpected_mismatch(self):self.assertFalse(run_case(self.base(),Toy)['success'])
    def test_restore_injection(self):
        original=np.linalg.solve;c=self.base();c['inject']='raise';run_case(c,Failing);self.assertIs(np.linalg.solve,original)
    def test_gate_thread(self):
        from audit import gate
        with patch.dict(os.environ,{'OPENBLAS_NUM_THREADS':'2'}):
            with self.assertRaises(Invalid):gate()
if __name__=='__main__':unittest.main()
