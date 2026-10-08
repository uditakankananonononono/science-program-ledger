import unittest,json,tempfile,shutil
from pathlib import Path
from unittest.mock import patch
import compare
ROOT=Path(__file__).resolve().parent.parent
class Tests(unittest.TestCase):
    def test_admission_no_runtime(self):
        m=json.loads((ROOT/'d3/manifest.json').read_text());a=compare.admit(ROOT,m)
        self.assertEqual(len(a['cases'])*len(a['policies']),32);self.assertEqual(len(a['cases'])*2,16)
    def test_typed_manifest_refusal_before_import(self):
        for key,val in [('dt','1/5'),('policies',['hold_p']),('policy_reset_and_action_wall_seconds',1)]:
            m=json.loads((ROOT/'d3/manifest.json').read_text());m[key]=val
            with patch.object(compare,'load_runtime',side_effect=AssertionError('must not import')):
                with self.assertRaises(ValueError):compare.score(m)
        m=json.loads((ROOT/'d3/manifest.json').read_text());m['cases'][0]['sequence']['observed'][0]=1
        with patch.object(compare,'load_runtime',side_effect=AssertionError('must not import')):
            with self.assertRaises(ValueError):compare.score(m)
    def test_pin_tamper_before_import(self):
        for name in compare.PINS:
            with tempfile.TemporaryDirectory() as temp:
                root=Path(temp)
                for item in compare.PINS:
                    dest=root/item;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/item,dest)
                with (root/name).open('a') as f:f.write('\n# tamper')
                m=json.loads((ROOT/'d3/manifest.json').read_text())
                with patch.object(compare,'load_runtime',side_effect=AssertionError('must not import')):
                    with self.assertRaises(ValueError):compare.score(m,root)
    def test_partial_runtime(self):
        # One one-step nominal fixture, not factorial/full battery.
        m=json.loads((ROOT/'d3/manifest.json').read_text());compare.admit(ROOT,m);h,c=compare.load_runtime(ROOT)
        from fractions import Fraction as F
        seq={'gain':[F(1)],'drift':[F(0)],'observed':[True],'immobilized':[False]}
        a=h.run(h.HoldP,seq);b=h.run(h.PredictP,seq)
        self.assertEqual(a['states'],[0,F(1,10)]);self.assertEqual(c.pair(a,b,1)['final_error']['predict_minus_hold'],0)
if __name__=='__main__':unittest.main()
