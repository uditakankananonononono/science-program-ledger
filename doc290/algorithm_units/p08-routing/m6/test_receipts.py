import unittest,json,subprocess,sys
from pathlib import Path
class ReceiptPersistence(unittest.TestCase):
    def test_real_persisted_type_mutations(self):
        p=subprocess.run([sys.executable,str(Path(__file__).resolve().parent/'receipt_mutation_dev.py')],capture_output=True,text=True,timeout=20);self.assertEqual(p.returncode,0,p.stderr)
        results=json.loads(Path('/tmp/m6-persisted-mutations.json').read_text());self.assertEqual(len(results),4);self.assertTrue(all(r['durable_FAIL'] and r['no_new_launches'] and r['stdout_unchanged'] for r in results))
