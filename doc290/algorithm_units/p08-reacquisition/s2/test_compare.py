import unittest,json,pathlib
from compare import trajectory
class HarnessTests(unittest.TestCase):
    def test_development_reproducibility_and_missing_counts(self):
        spec=json.loads(pathlib.Path(__file__).with_name('protocol.json').read_text())
        scenario=spec['scenarios'][0]
        a=trajectory(spec,1999,scenario);b=trajectory(spec,1999,scenario)
        self.assertEqual(a,b);self.assertEqual(a['missing'],10);self.assertEqual(a['observed'],70)
        self.assertGreater(a['confirmation_delay'],0)
    def test_confirmation_schedule_rejected(self):
        spec=json.loads(pathlib.Path(__file__).with_name('protocol.json').read_text());spec['confirmation_index']=32
        with self.assertRaises(ValueError):trajectory(spec,1999,spec['scenarios'][0])
if __name__=='__main__':unittest.main()
