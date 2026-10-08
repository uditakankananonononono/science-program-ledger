import io,tempfile,unittest,zipfile
from pathlib import Path
try:
    import numpy as np
    from PIL import Image
    from hrf_extract import extract_member
    AVAILABLE=True
except ImportError:AVAILABLE=False

@unittest.skipUnless(AVAILABLE,'optional imaging dependencies unavailable')
class ExtractionTests(unittest.TestCase):
    def fixture(self,array):
        raw=io.BytesIO();Image.fromarray(array).save(raw,format='TIFF')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'fixture.zip'
            with zipfile.ZipFile(p,'w') as z:z.writestr('mask.tif',raw.getvalue())
            return extract_member(p,'mask.tif')
    def test_known_chain(self):
        a=np.zeros((5,5),dtype=np.uint8);a[2,1:4]=255
        record,skeleton=self.fixture(a)
        self.assertEqual(record['vertices'],3);self.assertEqual(record['directed_edges'],4)
        self.assertEqual(record['components_8_before'],1);self.assertEqual(record['components_8_after'],1)
        self.assertEqual(int(skeleton.sum()),3)
    def test_invalid_gray(self):
        with self.assertRaises(ValueError):self.fixture(np.full((5,5),128,dtype=np.uint8))

    def test_equal_rgb_channels(self):
        a=np.zeros((5,5),dtype=np.uint8);a[2,1:4]=255
        record,_=self.fixture(np.repeat(a[:,:,None],3,axis=2))
        self.assertEqual(record['vertices'],3)
        self.assertEqual(record['original_shape'],[5,5,3])
    def test_unequal_rgb_rejected(self):
        a=np.zeros((5,5,3),dtype=np.uint8);a[2,1:4,0]=255
        with self.assertRaises(ValueError):self.fixture(a)
