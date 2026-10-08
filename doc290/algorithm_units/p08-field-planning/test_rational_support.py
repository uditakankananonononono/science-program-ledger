import unittest
from fractions import Fraction as F
from rational_support import support
class RationalTests(unittest.TestCase):
    def test_exact_boundary_and_tiny_separation(self):
        args=([0],[1,1],[[1]],[2],['1/2'],[0],[1])
        a=support(*args,['3/2']);self.assertFalse(a['separates_target']);self.assertEqual(a['max'],F(3,2))
        b=support(*args,['1.50000000000000000000000001']);self.assertTrue(b['separates_target'])
    def test_joint_separator(self):
        r=support([0,0],[1],[[1],[1]],[1],[1],[0],[1,-1],[1,-1])
        self.assertTrue(r['separates_target']);self.assertEqual(r['max'],0);self.assertEqual(r['target_projection'],2)
    def test_witness_exact_replay_and_slew(self):
        times=[F(1,3),F(2,7)];r=support([0],times,[[2]],['4/5'],['1/2'],['1/5'],[-1],[0])
        for key,expected in (('min_controls',r['min']),('max_controls',r['max'])):
            u=r[key];self.assertEqual(-sum(t*2*row[0] for t,row in zip(times,u)),expected)
            previous=F(1,5)
            for t,row in zip(times,u):self.assertLessEqual(abs(row[0]-previous),t/2);previous=row[0]
    def test_float_and_bool_rejected(self):
        for val in (.5,True):
            with self.assertRaises(ValueError):support([0],[1],[[1]],[1],[val],[0],[1],[0])
if __name__=='__main__':unittest.main()
