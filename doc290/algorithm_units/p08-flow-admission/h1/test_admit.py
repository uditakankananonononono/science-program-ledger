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
        s={'metadata_size':3,'metadata_md5':'900150983cd24fb0d6963f7d28e17f72'}
        admit.verify(b'abc',s)
        for raw in [b'ab',b'xyz']:
            with self.assertRaises(ValueError):admit.verify(raw,s)
    def test_utf8(self):
        with self.assertRaises(UnicodeError):admit.parse(b'\xff')
    def test_multiline_and_boundaries(self):
        r=admit.parse(b'"a\r\nb",x\r\n\r\nc,d\re,\x0bv\x0cf\n')
        self.assertEqual(r['rows'][0]['fields'],['a\r\nb','x'])
        self.assertEqual(r['rows'][0]['csv_physical_end_line'],2)
        self.assertTrue(r['rows'][1]['blank_record'])
        self.assertEqual(r['VT_count'],1);self.assertEqual(r['FF_count'],1)
        self.assertEqual(r['rows'][-1]['csv_physical_end_line'],5)
        self.assertEqual(len(r['raw_lines']),7)
    def test_ragged_nonfinite(self):
        r=admit.parse(b'a,b\n1,nan,inf,bad\n\n')
        self.assertEqual([x['field_count'] for x in r['rows']],[2,4,0])
        self.assertEqual(r['rows'][1]['fields'],['1','nan','inf','bad'])
        self.assertEqual(r['semantic_status'],'UNRESOLVED; strict CSV syntax is not schema validation')
        json.dumps(r,allow_nan=False)
    def test_bad_quote(self):
        r=admit.parse(b'a,b\n"unfinished')
        self.assertEqual(r['syntax_status'],'error_retained')
        self.assertEqual(len(r['rows']),1)
if __name__=='__main__':unittest.main()
