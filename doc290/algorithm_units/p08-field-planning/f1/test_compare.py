import unittest,json,pathlib,numpy as np
from compare import instance,call
class HarnessTests(unittest.TestCase):
    def test_development_reproducibility_and_expected_status(self):
        spec=json.loads(pathlib.Path(__file__).with_name('protocol.json').read_text())
        for kind in spec['classes']:
            a=instance(spec,2999,8,kind);b=instance(spec,2999,8,kind)
            for x,y in zip(a,b):np.testing.assert_array_equal(x,y)
            expected='primal_checked' if kind=='constructed_feasible' else 'solver_infeasible'
            for method in ('full','reduced'):self.assertEqual(call(method,a)['status'],expected)
    def test_exception_retention(self):
        from unittest.mock import patch
        with patch('compare.solve',side_effect=ValueError('development negative control')):
            r=call('full',[]);self.assertEqual(r['status'],'exception');self.assertIn('ValueError',r['exception'])
if __name__=='__main__':unittest.main()
