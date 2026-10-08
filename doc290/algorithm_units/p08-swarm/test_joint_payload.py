import unittest
from fractions import Fraction as F
from joint_payload import joint_payload
class JointTests(unittest.TestCase):
    def test_same_marginals_different_full_payload_success(self):
        cases=[([[0,0],[1,1]],['1/2','1/2'],F(1,2)),([[0,1],[1,0]],['1/2','1/2'],F(0)),([[0,0],[0,1],[1,0],[1,1]],['1/4']*4,F(1,4))]
        for bits,masses,success in cases:
            r=joint_payload(bits,masses,['1/2']*2,1);self.assertEqual(r['target_marginals'],[F(1,2)]*2)
            self.assertEqual(r['expected_target_payload'],F(1,2));self.assertEqual(r['threshold_success_probability'],success)
    def test_duplicate_outcomes_aggregate(self):
        r=joint_payload([[0],[1],[1]],['1/2','1/4','1/4'],[1],1)
        self.assertEqual(r['target_payload_distribution'],{F(0):F(1,2),F(1):F(1,2)})
    def test_heterogeneous_weights(self):
        r=joint_payload([[0,1],[1,0]],['1/3','2/3'],['1/4','3/4'],'3/4')
        self.assertEqual(r['threshold_success_probability'],F(1,3));self.assertEqual(r['expected_target_payload'],F(5,12))
    def test_bad_mass_and_boolean_outcome(self):
        for bits,masses in (([[1]],['1/2']),([[1]],[-1]),([[True]],[1]),([[2]],[1])):
            with self.assertRaises(ValueError):joint_payload(bits,masses,[1],1)
if __name__=='__main__':unittest.main()
