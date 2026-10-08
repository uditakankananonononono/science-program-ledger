import unittest,numpy as np
from scenarios import solve_scenarios
class ScenarioTests(unittest.TestCase):
    def call(self,maps,lo,hi,**kw):return solve_scenarios([0],[1],maps,[2],[2],[0],lo,hi,**kw)
    def test_common_schedule_two_gain_maps(self):
        r=self.call([[[1]],[[2]]],[[1],[2]],[[1],[2]])
        np.testing.assert_allclose(r['controls'],[[1]])
        np.testing.assert_allclose(np.array(r['scenario_trajectories'])[:,-1,0],[1,2])
    def test_individual_feasible_but_joint_infeasible(self):
        for B in ([[[1]]],[[[2]]]):self.assertEqual(self.call(B,[[1]],[[1]])['status'],'primal_checked')
        self.assertEqual(self.call([[[1]],[[2]]],[[1],[1]],[[1],[1]])['status'],'solver_infeasible')
    def test_interval_shared_solution(self):
        r=self.call([[[1]],[[1.1]]],[[.9],[.9]],[[1.1],[1.1]])
        self.assertEqual(r['status'],'primal_checked')
        self.assertTrue(all(v<=1e-8 for v in r['residuals']['terminal_box_violation_per_scenario']))
    def test_unlisted_map_is_not_guaranteed(self):
        r=self.call([[[1]],[[1.1]]],[[.9],[.9]],[[1.1],[1.1]])
        u=r['controls'][0][0];self.assertGreater(2*u,1.1)
    def test_strict_tolerance_and_invalid_map(self):
        for t in (True,np.bool_(True),np.bool_(False),'1',float('nan'),0):
            with self.assertRaises(ValueError):self.call([[[1]]],[[0]],[[1]],tolerance=t)
        with self.assertRaises(ValueError):self.call([[[float('inf')]]],[[0]],[[1]])
if __name__=='__main__':unittest.main()
