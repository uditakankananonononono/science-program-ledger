import unittest,io,json,tempfile
from pathlib import Path
from unittest.mock import patch
import check
from PIL import Image
from check import labels,decode,download
class Response:
    status=200
    def __init__(self,data,headers=None):self.headers=headers or {};self.io=io.BytesIO(data)
    def read(self,n):return self.io.read(n)
    def __enter__(self):return self
    def __exit__(self,*a):pass
class Open:
    def __init__(self,r):self.r=r
    def open(self,*a,**kw):return self.r
class Tests(unittest.TestCase):
    def test_labels(self):
        self.assertEqual(labels(b'',20,10)['status'],'empty')
        self.assertEqual(labels(b'0 .5 .5 .2 .4\n1 .6 .6 .1 .1',20,10)['row_count'],2)
        self.assertEqual(labels(b'0 .5 .5 .2 .4',20,10)['rows'][0]['corners_px'],[8.,3.,12.,7.])
        for raw in [b'0 1 2',b'0 nan .5 .1 .1',b'-.5 .5 .5 .2 .2',b'0 .5 .5 0 .1',b'0 1 .5 .2 .2']:
            self.assertEqual(labels(raw,20,10)['invalid_rows'],1)
    def test_stream(self):
        self.assertEqual(download('https://example.invalid',3,[3],Open(Response(b'abc',{'Content-Length':'3'}))),b'abc')
        with self.assertRaises(ValueError):download('https://example.invalid',2,[9],Open(Response(b'abc')))
        with self.assertRaises(ValueError):download('https://example.invalid',2,[9],Open(Response(b'',{'Content-Length':'3'})))
    def test_overflow(self):
        r=labels(b'0 1e308 .5 1e308 .1',20,10)
        self.assertIn('derived_arithmetic_nonfinite',r['rows'][0]['issues']);self.assertIsNone(r['rows'][0]['corners_px'])
        json.dumps(r,allow_nan=False)
    def test_truncated(self):
        with self.assertRaises(ValueError):download('https://example.invalid',9,[9],Open(Response(b'ab',{'Content-Length':'3'})))
    def test_end_to_end_invalid(self):
        b=io.BytesIO();Image.new('RGB',(20,10)).save(b,format='PNG');image=b.getvalue()
        for label in [b'\xff',b'0 1e308 .5 1e308 .1']:
            def fake(url,*args):
                if '/images/' in url:return image
                if '/labels/' in url:return label
                return b'nc: 1\n'
            with tempfile.TemporaryDirectory() as d,patch.object(check,'download',side_effect=fake):
                check.run(str(Path(d)/'out'));r=json.load(open(Path(d)/'out/integrity.json'))
                self.assertEqual(len(r['records']),24)
                if label==b'\xff':self.assertTrue(all(a['status']=='unavailable' for a in r['records']))
                else:self.assertTrue(all(a['annotation']['invalid_rows']==1 for a in r['records']))
                self.assertTrue((Path(d)/'out/overlay_1.png').exists())
    def test_decode(self):
        b=io.BytesIO();Image.new('RGB',(20,10)).save(b,format='PNG');self.assertEqual(decode(b.getvalue()).size,(20,10))
        b=io.BytesIO();Image.new('RGB',(4097,1)).save(b,format='PNG')
        with self.assertRaises(ValueError):decode(b.getvalue())
if __name__=='__main__':unittest.main()
