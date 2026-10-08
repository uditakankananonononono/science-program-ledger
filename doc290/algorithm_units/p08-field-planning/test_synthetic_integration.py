import unittest,numpy as np
from synthetic_integration import run
class IntegrationTests(unittest.TestCase):
    def test_unique_saturated_schedule_and_force_replay(self):
        r=run();np.testing.assert_allclose(r['schedule']['controls'],np.full((2,3),.5),atol=1e-8)
        np.testing.assert_allclose(r['independent_force_replay_terminal'],[1,2,3],atol=1e-8)
        self.assertLessEqual(r['replay_max_abs_error'],1e-8)
if __name__=='__main__':unittest.main()
