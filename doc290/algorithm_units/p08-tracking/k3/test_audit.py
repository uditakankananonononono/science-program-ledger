import unittest,os,json
from unittest.mock import patch
import numpy as np
from audit import run_case,oracle_agreement,snapshot,encode,finite,Invalid
class Development(unittest.TestCase):
    def base(self):return {'name':'dev','truth':[[0]*4],'estimated':[[0]*4],'covariances':[np.eye(4).astype(int).tolist()],'available':[True],'inject':None,'expected':'REFUSE'}
    def test_oracle_counts_and_order(self):
        o={'total':2,'scored':2,'excluded':0,'position_squared':'25/2','velocity_squared':'25/2','nees':[25,'25/2'],'mean':'75/4'}
        r={'total_records':2,'scored_records':2,'excluded_missing_truth':0,'position_rmse':(25/2)**.5,'velocity_rmse':(25/2)**.5,'nees':[25,12.5],'mean_nees':18.75,'scope':'test'}
        self.assertTrue(all(oracle_agreement(r,o).values()));r['nees'].reverse();self.assertFalse(oracle_agreement(r,o)['nees'])
    def test_none_semantics(self):
        o={'total':1,'scored':0,'excluded':1,'position_squared':None,'velocity_squared':None,'nees':[],'mean':None};r={'total_records':1,'scored_records':0,'excluded_missing_truth':1,'position_rmse':None,'velocity_rmse':None,'nees':[],'mean_nees':None,'scope':'test'}
        self.assertTrue(all(oracle_agreement(r,o).values()));r['position_rmse']=0;self.assertFalse(oracle_agreement(r,o)['position_rmse'])
    def test_snapshots_and_tag(self):
        a=np.arange(4);s=snapshot(a);a[0]=9;self.assertNotEqual(s,snapshot(a));self.assertFalse(finite([np.inf]));self.assertIn('+Inf',json.dumps(encode(np.inf),allow_nan=False))
    def test_mutation_and_restore(self):
        def refuse(*a):raise ValueError('dev')
        c=self.base();c['inject']='raise';old=np.linalg.solve;self.assertTrue(run_case(c,refuse)['success']);self.assertIs(np.linalg.solve,old)
        def mutate(*a):a[1][0,0]=9;raise ValueError('dev')
        self.assertFalse(run_case(c,mutate)['success'])
    def test_availability_no_bool_coercion(self):
        c=self.base();c['available']=[1]
        def refuse(*a):self.assertEqual(a[3].dtype.kind,'i');raise ValueError('dev')
        self.assertTrue(run_case(c,refuse)['success'])
    def test_finite_unexpected_mismatch(self):
        def result(*a):return {'total_records':1,'scored_records':1,'excluded_missing_truth':0,'position_rmse':0,'velocity_rmse':0,'nees':[0],'mean_nees':0,'scope':'test'}
        self.assertFalse(run_case(self.base(),result)['success'])
    def test_thread_gate(self):
        from audit import gate
        with patch.dict(os.environ,{'OPENBLAS_NUM_THREADS':'2'}):
            with self.assertRaises(Invalid):gate()
if __name__=='__main__':unittest.main()
