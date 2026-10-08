import unittest
import numpy as np
import json,sys,tempfile,hashlib,zipfile
from pathlib import Path
from diagnose import diagnostic,fit,load
class Tests(unittest.TestCase):
    def test_literal_exact(self):
        a=np.array([[-25,3.],[0,4.],[25,3.]])
        r=diagnostic(a);self.assertEqual(r['amplitude_um_per_s'],4);self.assertEqual(r['in_sample']['sse'],0)
        self.assertEqual(r['leave_one_location']['sse'],0)
    def test_missing(self):
        a=np.array([[-25,3.],[0,4.],[25,np.nan]])
        r=diagnostic(a);self.assertEqual((r['finite_rows'],r['missing_rows']),(2,1));self.assertIsNone(r['rows'][2]['residual_um_per_s']);self.assertEqual(r['rows'][2]['predicted_um_per_s'],3)
    def test_fold_guard(self):
        with self.assertRaises(ValueError):diagnostic(np.array([[0,1.],[50,0.]]))
        with self.assertRaises(ValueError):fit(np.array([0.]),np.array([1.]))
    def test_invalid(self):
        for a in (np.array([[np.nan,1.],[0,1.]]),np.array([[0,np.inf],[1,1.]]),np.array([[0,np.nan],[1,1.]])):
            with self.assertRaises(ValueError):diagnostic(a)
    def test_nonzero_literal(self):
        r=diagnostic(np.array([[-25,2.],[0,4.],[25,3.]]));self.assertAlmostEqual(r['amplitude_um_per_s'],31/8.5)
    def test_literal_archive_pins(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'literal.zip';raw=b'#literal\n-25 3\n0 4\n25 3\n';profiles=[]
            with zipfile.ZipFile(path,'w') as z:
                for v in range(1,6):
                    name=f'Fig3/Poiseuille_E0V_flowprofile_{v}V.txt';z.writestr(name,raw)
                    profiles.append({'name':name,'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'header':'#literal','shape':[3,2],'nonfinite_count':0})
            p={'python':sys.version,'packages':{},'subset_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'profiles':profiles}
            self.assertEqual(len(load(path,p)),5)
            bad=json.loads(json.dumps(p));bad['profiles'][0]['sha256']='wrong'
            with self.assertRaises(ValueError):load(path,bad)
            bad=json.loads(json.dumps(p));bad['profiles'].reverse()
            with self.assertRaises(ValueError):load(path,bad)
            bad=json.loads(json.dumps(p));bad['profiles'][0]['nonfinite_count']=1
            with self.assertRaises(ValueError):load(path,bad)
            bad=json.loads(json.dumps(p));bad['subset_sha256']='wrong'
            with self.assertRaises(ValueError):load(path,bad)
    def test_environment_refusal(self):
        with self.assertRaises(ValueError):load('not-read',{'python':'bad','packages':{}})
if __name__=='__main__':unittest.main()
