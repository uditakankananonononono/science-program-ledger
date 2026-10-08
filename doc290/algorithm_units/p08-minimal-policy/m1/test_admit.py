import io,json,unittest
import admit
class Response(io.BytesIO):
    status=200
    def __init__(self,b,headers=None,url='https://fixed.test/file'):
        super().__init__(b);self.headers=headers or {};self.url=url
    def geturl(self):return self.url
class Opener:
    def __init__(self,r):self.r=r
    def open(self,req,timeout):return self.r
class Tests(unittest.TestCase):
    def test_transport(self):
        u='https://fixed.test/file'
        self.assertEqual(admit.download(u,8,[8],Opener(Response(b'abc',{'Content-Length':'3'}))),b'abc')
        for r in [Response(b'a',{'Content-Length':'2'}),Response(b'a',{'Content-Encoding':'gzip'}),Response(b'a',url='https://other.test/'),Response(b'abc',{'Content-Length':'9'}),Response(b'a',{'Content-Length':'x'}),Response(b'abc')]:
            with self.assertRaises(ValueError):admit.download(u,3,[3],Opener(r))
        self.assertIsNone(admit.NoRedirect().redirect_request(None,None,302,None,None,None))
    def test_identity(self):
        s={'metadata_blob_size':3,'git_blob_oid':'f2ba8f84ab5c1bce84a7b441cb1959cfc7093b7f'}
        admit.verify(b'abc',s)
        for b in [b'ab',b'xyz']:
            with self.assertRaises(ValueError):admit.verify(b,s)
    def test_utf8_boundaries(self):
        with self.assertRaises(UnicodeError):admit.structural(b'\xff')
        r=admit.structural(b'a\n\nB\x0bC\x0cD')
        self.assertEqual([x['text'] for x in r['lines']],['a','','B','C','D'])
        self.assertEqual(r['VT_count'],1);self.assertEqual(r['FF_count'],1)
    def test_ast_errors(self):
        r=admit.structural(b'def broken(',True)
        self.assertEqual(r['ast_status'],'error_retained')
        json.dumps(r,allow_nan=False)
    def test_no_execution(self):
        raw=b'import unavailable_module\nraise RuntimeError("MUST NOT RUN")\ncheckpoint="outside/weights"\ndef policy(x): return x\n'
        r=admit.structural(raw,True)
        self.assertEqual(r['ast_status'],'parsed');self.assertEqual(r['definitions'][0]['name'],'policy')
        self.assertTrue(r['imports']);self.assertTrue(r['string_literals'])
if __name__=='__main__':unittest.main()
