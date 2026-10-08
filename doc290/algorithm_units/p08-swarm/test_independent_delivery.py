import unittest,itertools
from fractions import Fraction as F
from independent_delivery import independent_delivery
from joint_delivery import delivery
class IndependentDeliveryTests(unittest.TestCase):
    def test_matches_explicit_joint_enumeration(self):
        p=[F(1,3),F(1,2)];q=[F(1,3),F(1,4)];weights=[F(1,4),F(3,4)];labels=['target','offtarget','lost']
        states=list(itertools.product(labels,repeat=2));mass=[]
        for row in states:
            product=F(1)
            for i,s in enumerate(row):product*=dict(target=p[i],offtarget=q[i],lost=1-p[i]-q[i])[s]
            mass.append(product)
        a=independent_delivery(p,q,weights,F(3,4),F(1,4));b=delivery(states,mass,weights,F(3,4),F(1,4))
        for key in ('target_threshold_probability','offtarget_exceedance_probability','delivery_within_collateral_cap_probability'):self.assertEqual(a[key],b[key])
        self.assertEqual(a['expected_target_payload'],b['expected_payloads']['target'])
    def test_budget_abort_not_truncation(self):
        with self.assertRaises(RuntimeError):independent_delivery(['1/3'],['1/3'],[1],1,0,max_states=2)
        r=independent_delivery(['1/3'],['1/3'],[1],1,0,max_states=3);self.assertEqual(r['peak_states'],3)
    def test_zero_branches_do_not_waste_budget(self):
        r=independent_delivery([1],[0],[1],1,0,max_states=1);self.assertEqual(r['peak_states'],1)
        self.assertEqual(r['delivery_within_collateral_cap_probability'],1)
    def test_budget_bool_and_invalid_probability_refused(self):
        with self.assertRaises(ValueError):independent_delivery([1],[0],[1],1,0,max_states=True)
        with self.assertRaises(ValueError):independent_delivery([1],[1],[1],1,0)
if __name__=='__main__':unittest.main()
