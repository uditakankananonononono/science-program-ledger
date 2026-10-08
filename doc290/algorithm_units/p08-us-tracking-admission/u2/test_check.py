import io,json,unittest
from unittest.mock import patch
from PIL import Image
import check
class Response(io.BytesIO):
    status=200
    def __init__(self,body,headers=None,url='https://fixed.test/file'):
        super().__init__(body); self.headers=headers or {};self.url=url
    def geturl(self):return self.url
class Opener:
    def __init__(self,r):self.r=r
    def open(self,req,timeout):return self.r
class Tests(unittest.TestCase):
    def test_transport(self):
        u='https://fixed.test/file'
        self.assertEqual(check.download(u,8,[8],Opener(Response(b'abc',{'Content-Length':'3'}))),b'abc')
        for r in [Response(b'a',{'Content-Length':'2'}),Response(b'a',{'Content-Encoding':'gzip'}),Response(b'a',url='https://other.test/'),Response(b'123456789',{'Content-Length':'9'}),Response(b'abc',{'Content-Length':'x'})]:
            with self.assertRaises(ValueError):check.download(u,8,[8],Opener(r))
        with self.assertRaises(ValueError):check.download(u,3,[3],Opener(Response(b'abc')))
    def test_redirect_handler(self):
        self.assertIsNone(check.NoRedirect().redirect_request(None,None,302,None,None,None))
    def test_blob(self):
        raw=b'abc';s={'metadata_blob_size':3,'git_blob_oid':'f2ba8f84ab5c1bce84a7b441cb1959cfc7093b7f'}
        check.verify(raw,s)
        with self.assertRaises(ValueError):check.verify(b'ab',s)
        with self.assertRaises(ValueError):check.verify(b'xyz',s)
    def test_literal_rows(self):
        raw=b'1,2,3,4\n\n1,2,3\nnan,2,3,4\n1e999,2,3,4\n1e308,2,1e308,4\n-1,2,3,4\n1,2,0,4\n'
        r=check.rows(raw,{1:(20,20)})
        self.assertEqual(len(r),8);self.assertEqual(r[1]['raw_row_ordinal'],2)
        self.assertIn('blank_row',r[1]['issues']);self.assertIn('field_count',r[2]['issues'])
        self.assertTrue(r[3]['issues']);self.assertTrue(r[4]['issues']);self.assertTrue(r[5]['issues'])
        self.assertIsNone(r[5]['candidate_corners']);self.assertIn('candidate_nonpositive_wh',r[7]['issues'])
        json.dumps(r,allow_nan=False)
        with self.assertRaises(UnicodeError):check.rows(b'\xff',{})
        self.assertEqual(check.rows(b'',{})[0]['status'],'missing')
        self.assertEqual(check.rows(b'1,2,3',{})[0]['issues'],['field_count'])
    def test_fraction(self):
        r=check.rows(b'0.1,0.2,0.3,0.4\n',{1:(1,1)})[0]
        self.assertEqual(r['candidate_corners']['exact'],['1/10','1/5','2/5','3/5'])
        self.assertEqual(r['mapping'],'UNRESOLVED')
    def test_static(self):
        self.assertEqual(check.static(b'0,1,0')['comma_token_count'],3)
        self.assertEqual(check.static(b'0,1,0')['line_count'],1)
    def test_real_decode_fixture(self):
        im=Image.new('RGB',(10,10));b=io.BytesIO();im.save(b,format='PNG')
        self.assertEqual(check.decode(b.getvalue()).size,(10,10))
    def test_preload_gates(self):
        class Fake:
            format='PNG';size=(10,10);mode='RGB';n_frames=1;loaded=False
            def __enter__(self):return self
            def __exit__(self,*a):pass
            def load(self):self.loaded=True
            def convert(self,mode):return self
        for size,frames,mode,mem in [((4097,1),1,'RGB',check.WORK_BYTES),((2000,2000),1,'RGB',check.WORK_BYTES),((10,10),2,'RGB',check.WORK_BYTES),((10,10),1,'I',check.WORK_BYTES),((10,10),1,'RGB',1)]:
            f=Fake();f.size=size;f.n_frames=frames;f.mode=mode
            with patch.object(check.Image,'open',return_value=f),patch.object(check,'WORK_BYTES',mem):
                with self.assertRaises(ValueError):check.decode(b'fixture')
            self.assertFalse(f.loaded)
if __name__=='__main__':unittest.main()
