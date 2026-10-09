import unittest,json
from pathlib import Path
from core import launch,gate,Invalid
class WorkerControls(unittest.TestCase):
    def test_real_kill_cap_gate_parse(self):
        rows={m:launch([m],timeout=.3 if m=='sleep' else 5) for m in ('sleep','memory','gatefail','badjson')}
        for r in rows.values():self.assertEqual(r['status'],'FAIL');self.assertTrue(r['reaped'])
        self.assertEqual(rows['sleep']['returncode'],-9);self.assertTrue(rows['sleep']['kill_sent']);self.assertEqual(rows['sleep']['stdout'],'sleep-ready\n');self.assertIn('MemoryError',rows['memory']['stdout']);self.assertIn('intentional gate refusal',rows['gatefail']['stdout']);self.assertIn('JSONDecodeError',rows['badjson']['reason'])
        Path('/tmp/p3-dev-controls-current.json').write_text(json.dumps(rows,sort_keys=True,indent=2)+'\n')
    def test_sourcegate(self):self.assertEqual(set(gate()),{'manifest_sha256','runtime_sha256'})
