"""Injected successful-solver outputs must not bypass primal verification."""
import unittest
from unittest.mock import patch
from types import SimpleNamespace
import numpy as np
from feasibility import solve
from corridor import solve_corridor
from scenarios import solve_scenarios

class SolverCorruptionTests(unittest.TestCase):
    def fake(self,u):return SimpleNamespace(status=0,success=True,x=np.array(u,float))
    def calls(self):
        return [('feasibility.linprog',lambda:solve([0],[1],[1],[[1]],[1],[1],[0])),
                ('corridor.linprog',lambda:solve_corridor([0],[1],[1],[[1]],[1],[1],[0],[[0],[1]],[[0],[1]])),
                ('scenarios.linprog',lambda:solve_scenarios([0],[1],[[[1]]],[1],[1],[0],[[1]],[[1]]))]
    def test_nonfinite_success_rejected_all_modules(self):
        for route,call in self.calls():
            for value in (np.nan,np.inf,-np.inf):
                with self.subTest(route=route,value=value),patch(route,return_value=self.fake([value])):
                    with self.assertRaises(RuntimeError):call()
    def test_wrong_terminal_success_rejected_all_modules(self):
        for route,call in self.calls():
            with self.subTest(route=route),patch(route,return_value=self.fake([0])):
                with self.assertRaises(RuntimeError):call()
    def test_actuator_and_slew_success_rejected(self):
        with patch('feasibility.linprog',return_value=self.fake([2])):
            with self.assertRaises(RuntimeError):solve([0],[2],[1],[[1]],[1],[10],[0])
        with patch('scenarios.linprog',return_value=self.fake([1])):
            with self.assertRaises(RuntimeError):solve_scenarios([0],[1],[[[1]]],[2],[.5],[0],[[1]],[[1]])
    def test_corridor_only_violation_success_rejected(self):
        with patch('corridor.linprog',return_value=self.fake([1,0])):
            with self.assertRaises(RuntimeError):solve_corridor([0],[1],[1,1],[[1]],[2],[10],[0],[[0],[.2],[1]],[[0],[.2],[1]])
    def test_correct_injected_output_accepted(self):
        for route,call in self.calls():
            with self.subTest(route=route),patch(route,return_value=self.fake([1])):
                self.assertEqual(call()['status'],'primal_checked')
if __name__=='__main__':unittest.main()
