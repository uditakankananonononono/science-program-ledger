import unittest
from fractions import Fraction as F
from payload import independent_payload
class PayloadTests(unittest.TestCase):
    def test_equal_total_payload_success_is_not_any_arrival(self):
        single=independent_payload(['1/2'],['1/4'],[1],1)
        swarm=independent_payload(['1/2']*2,['1/4']*2,['1/2']*2,1)
        self.assertEqual(single['total_payload'],swarm['total_payload'])
        self.assertEqual(swarm['at_least_one_target_probability'],F(3,4))
        self.assertEqual(swarm['threshold_success_probability'],F(1,4))
        self.assertEqual(single['threshold_success_probability'],F(1,2))
        self.assertEqual(single['expected_target_payload'],swarm['expected_target_payload'])
        self.assertEqual(single['expected_offtarget_payload'],swarm['expected_offtarget_payload'])
    def test_half_payload_threshold(self):
        r=independent_payload(['1/2']*2,[0,0],['1/2']*2,'1/2')
        self.assertEqual(r['threshold_success_probability'],F(3,4))
        self.assertEqual(r['target_payload_distribution'],{F(0):F(1,4),F(1,2):F(1,2),F(1):F(1,4)})
    def test_heterogeneous_probabilities_and_weights(self):
        r=independent_payload(['1/3','2/3'],['1/3',0],['1/4','3/4'],'3/4')
        self.assertEqual(r['threshold_success_probability'],F(2,3));self.assertEqual(r['expected_target_payload'],F(7,12))
    def test_invalid_refused(self):
        for p,q,w,t in (([1],[1],[1],1),([.5],[0],[1],1),([1],[0],[0],1),([1],[0],[1],2)):
            with self.assertRaises(ValueError):independent_payload(p,q,w,t)
if __name__=='__main__':unittest.main()
