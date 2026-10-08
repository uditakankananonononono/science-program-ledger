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

    def test_timeout_branch_and_continue(self):
        from unittest.mock import patch
        import json, subprocess
        completed = subprocess.CompletedProcess(['worker'],0,stdout=json.dumps({'size':4,'status':'passed'}),stderr='')
        with patch('resource_probe.subprocess.run',side_effect=[subprocess.TimeoutExpired(['worker'],5),completed]) as mocked:
            records=probe(sizes=(3,4),timeout=5)['records']
        self.assertEqual(records,[{'size':3,'status':'timeout','timeout_seconds':5},{'size':4,'status':'passed'}])
        self.assertEqual(mocked.call_count,2)
        self.assertEqual(mocked.call_args_list[0].kwargs['timeout'],5)
        self.assertEqual(mocked.call_args_list[1].kwargs['timeout'],5)
