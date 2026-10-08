import unittest
from marginal_bounds import bounds
class MarginalTests(unittest.TestCase):
    def test_full_payload_frechet_two_agents(self):
        r=bounds(['1/2']*2,[0,0],['1/2']*2,1,0)
        self.assertAlmostEqual(r['bounds']['minimum']['probability'],0);self.assertAlmostEqual(r['bounds']['maximum']['probability'],.5)
    def test_any_target_threshold(self):
        r=bounds(['1/2']*2,[0,0],['1/2']*2,'1/2',0)
        self.assertAlmostEqual(r['bounds']['minimum']['probability'],.5);self.assertAlmostEqual(r['bounds']['maximum']['probability'],1)
    def test_single_agent_fixed(self):
        r=bounds(['1/3'],['1/3'],[1],1,0)
        for o in r['bounds'].values():self.assertAlmostEqual(o['probability'],1/3)
    def test_size_guard_and_corrupted_mass(self):
        with self.assertRaises(ValueError):bounds([0]*6,[0]*6,[1]*6,1,0)
        from unittest.mock import patch
        from types import SimpleNamespace
        import numpy as np
        with patch('marginal_bounds.linprog',return_value=SimpleNamespace(success=True,x=np.array([np.nan]*3))):
            with self.assertRaises(RuntimeError):bounds([0],[0],[1],1,0)
if __name__=='__main__':unittest.main()
