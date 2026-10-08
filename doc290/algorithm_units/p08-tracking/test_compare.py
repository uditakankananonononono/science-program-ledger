import unittest,json,pathlib
import numpy as np
from compare import trajectory,model
class ComparisonTests(unittest.TestCase):
    def test_development_reproducibility_counts(self):
        spec=json.loads(pathlib.Path(__file__).with_name('comparison_protocol.json').read_text())
        spec['steps']=6
        for probability in (0.,1.):
            regime={'name':'development','measurement_sigma':1.,'dropout_probability':probability}
            a=trajectory(spec,999,regime);b=trajectory(spec,999,regime)
            self.assertEqual(a,b);self.assertEqual(a['missing'],int(6*probability));self.assertEqual(a['kalman']['scored_records'],6)
    def test_generator_model_matches_prediction(self):
        from kalman import ConstantVelocity
        state=np.array([1.,2.,3.,4.]);P=np.eye(4)
        F,Q=model(.13,.25);kf=ConstantVelocity(state,P,.25);r=kf.step(.13)
        np.testing.assert_allclose(r['state'],F@state);np.testing.assert_allclose(r['covariance'],F@P@F.T+Q)
