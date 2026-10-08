import unittest
from unittest.mock import patch
from compare import case
class BoundaryHarnessTests(unittest.TestCase):
    def test_separate_development_case(self):
        r=case('3','-1/2')
        self.assertEqual(r['declared_target'],'3');self.assertEqual(r['exact_status'],'exact_model_reachable')
        for out in r['float_results'].values():self.assertEqual(out['status'],'primal_checked');self.assertEqual(out['exact_slew_violation'],'0')
    def test_exception_preserved(self):
        with patch('compare.solve',side_effect=RuntimeError('development control')):
            r=case('3','-1/2');self.assertEqual(r['float_results']['full']['status'],'exception')
            self.assertEqual(r['float_results']['reduced']['status'],'primal_checked')
if __name__=='__main__':unittest.main()
