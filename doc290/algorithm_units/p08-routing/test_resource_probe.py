import unittest
from resource_probe import probe

class ResourceProbeTests(unittest.TestCase):
    def test_real_worker_and_objective(self):
        got=probe(sizes=(3,),timeout=5)['records'][0]
        self.assertEqual(got['status'],'passed')
        self.assertEqual(got['vertices'],9)
        self.assertEqual(got['directed_edges'],24)
        self.assertEqual(got['scenario_totals'],[4,8])
        self.assertGreater(got['peak_process_rss_kib'],0)
        self.assertGreaterEqual(got['solve_seconds'],0)
    def test_invalid_worker_captured(self):
        got=probe(sizes=(31,),timeout=5)['records'][0]
        self.assertEqual(got['status'],'failed')
        self.assertEqual(got['returncode'],2)
