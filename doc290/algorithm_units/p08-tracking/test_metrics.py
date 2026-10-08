import unittest
import numpy as np
from metrics import evaluate

class MetricTests(unittest.TestCase):
    def test_hand_computed_errors(self):
        r=evaluate(np.zeros((2,4)),[[3,4,0,0],[0,0,6,8]],[np.eye(4),2*np.eye(4)],[True,True])
        self.assertAlmostEqual(r['position_rmse'],np.sqrt(12.5))
        self.assertAlmostEqual(r['velocity_rmse'],np.sqrt(50))
        self.assertEqual(r['nees'],[25,50]);self.assertEqual(r['mean_nees'],37.5)
    def test_missing_truth_counted_not_zero_filled(self):
        r=evaluate([[float('nan')]*4,[0]*4],[[0]*4,[1]*4],[np.eye(4)]*2,[False,True])
        self.assertEqual(r['scored_records'],1);self.assertEqual(r['excluded_missing_truth'],1)
        self.assertEqual(r['mean_nees'],4)
    def test_all_missing_explicit(self):
        r=evaluate([[float('nan')]*4],[[0]*4],[np.eye(4)],[False])
        self.assertIsNone(r['position_rmse']);self.assertIsNone(r['mean_nees']);self.assertEqual(r['nees'],[])
    def test_invalid_inputs_and_unused_covariance(self):
        for p in (np.zeros((4,4)),np.diag([-1,1,1,1])):
            with self.assertRaises(ValueError):evaluate([[0]*4],[[0]*4],[p],[False])
        with self.assertRaises(ValueError):evaluate([[0]*4],[[0]*4],[np.eye(4)],[1])
        with self.assertRaises(ValueError):evaluate([[float('nan')]*4],[[0]*4],[np.eye(4)],[True])
    def test_nees_coordinate_transform_invariant(self):
        error=np.array([1.,2.,3.,4.]);P=np.diag([1.,2.,3.,4.]);A=np.array([[2.,0,0,0],[0,.5,0,0],[0,0,3,0],[0,0,0,4]])
        a=evaluate([np.zeros(4)],[error],[P],[True])
        b=evaluate([np.zeros(4)],[A@error],[A@P@A.T],[True])
        self.assertAlmostEqual(a['mean_nees'],b['mean_nees'])
