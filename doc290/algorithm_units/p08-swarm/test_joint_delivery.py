import unittest
from fractions import Fraction as F
from joint_delivery import delivery
class DeliveryTests(unittest.TestCase):
    def test_target_success_and_collateral_condition_differ(self):
        r=delivery([['target','offtarget'],['target','lost']],['1/2','1/2'],['1/2']*2,'1/2',0)
        self.assertEqual(r['target_threshold_probability'],1);self.assertEqual(r['delivery_within_collateral_cap_probability'],F(1,2))
        self.assertEqual(r['offtarget_exceedance_probability'],F(1,2));self.assertEqual(r['expected_payloads'],{'target':F(1,2),'offtarget':F(1,4),'lost':F(1,4)})
    def test_cap_equality_allowed(self):
        r=delivery([['target','offtarget']],[1],['1/2']*2,'1/2','1/2');self.assertEqual(r['delivery_within_collateral_cap_probability'],1)
    def test_duplicate_and_zero_mass(self):
        r=delivery([['target'],['target'],['lost']],['1/3','2/3',0],[1],1,0)
        self.assertEqual(r['expected_payloads']['target'],1);self.assertEqual(r['marginals'][0]['lost'],0)
    def test_invalid_states_threshold_mass(self):
        for states,ps,required,cap in (([['both']],[1],1,0),([['target']],['1/2'],1,0),([['target']],[1],1,-1),([['target']],[1],2,0)):
            with self.assertRaises(ValueError):delivery(states,ps,[1],required,cap)
if __name__=='__main__':unittest.main()
