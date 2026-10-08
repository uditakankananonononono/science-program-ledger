import unittest
import numpy as np
from reproduce import transform_trajectory,transform_profile,transform_ramp,load_tables
class Tests(unittest.TestCase):
    def test_trajectory(self):
        a=np.array([[42.,21.,59.,3.]])
        np.testing.assert_allclose(transform_trajectory(a,2),[[-1,10,2,3]])
    def test_profile_nan(self):
        a=np.array([[21,np.nan],[-21,29.5]])
        b=transform_profile(a);self.assertTrue(np.isnan(b[0,0]));np.testing.assert_allclose(b[1],[1,-1])
    def test_ramp_origin(self):
        a=np.array([[42.,21.,29.5,0.],[63.,21.,29.5,5.]])
        b=transform_ramp(a);self.assertEqual(b[0,0],0)
        self.assertAlmostEqual(b[1,0]-b[0,0],-np.cos(np.deg2rad(.8)))
        self.assertAlmostEqual(b[1,1]-b[0,1],np.sin(np.deg2rad(.8)))
    def test_hash_refusal(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_bytes(b'bad')
            with self.assertRaises(ValueError):load_tables(p,{'subset_sha256':'0'})
if __name__=='__main__':unittest.main()
