import unittest,os,json
from unittest.mock import patch
import numpy as np
from audit import snapshot,isolation,encode,finite,run_case,Invalid
class Development(unittest.TestCase):
    def base(self):return {'name':'dev','means':[[1,2,3,4]],'covs':[np.eye(4).astype(int).tolist()],'predictions':[],'pcs':[],'Fs':[],'inject':None,'expected':'REFUSE'}
    def test_genuine_copy(self):
        a=np.arange(4);s=snapshot(a);a[0]=9;self.assertNotEqual(s,snapshot(a))
    def test_isolation_large_zero(self):
        inputs=[np.array([1.])];a=np.array([1e308]);b=np.array([0.]);original=[snapshot(a),snapshot(b)]
        flags,probes=isolation([a,b],inputs);self.assertTrue(all(all(p.values()) for p in probes));self.assertEqual(original,[snapshot(a),snapshot(b)])
    def test_alias_detected(self):
        a=np.array([2.]);flags,probes=isolation([a,a],[a]);self.assertTrue(flags['output_output']);self.assertTrue(flags['output_input'][0][0]);self.assertFalse(probes[0]['inputs_unchanged'])
    def test_finite_tag(self):self.assertFalse(finite([np.inf]));self.assertIn('+Inf',json.dumps(encode(np.array([np.inf])),allow_nan=False))
    def test_refusal_mutation_and_restore(self):
        def fail(*args):raise ValueError('dev')
        c=self.base();c['inject']='raise';old=np.linalg.solve;r=run_case(c,fail);self.assertTrue(r['success']);self.assertIs(old,np.linalg.solve)
        def mutate(*args):args[0][0,0]=9;raise ValueError('dev')
        self.assertFalse(run_case(c,mutate)['success'])
    def test_toy_valid_empty_shapes(self):
        c=self.base();c.update(expected='VALID',oracle_means=[[1,2,3,4]],oracle_covs=c['covs'])
        def toy(*a):
            self.assertEqual(a[2].shape,(0,4));self.assertEqual(a[3].shape,(0,4,4));return a[0].copy(),a[1].copy()
        self.assertTrue(run_case(c,toy)['success'])
        self.assertFalse(run_case(self.base(),toy)['success'])
    def test_thread_gate(self):
        from audit import gate
        with patch.dict(os.environ,{'OPENBLAS_NUM_THREADS':'2'}):
            with self.assertRaises(Invalid):gate()
if __name__=='__main__':unittest.main()
