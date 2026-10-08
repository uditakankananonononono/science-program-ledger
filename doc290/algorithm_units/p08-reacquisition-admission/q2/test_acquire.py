import copy,email.message,io,json,tempfile,unittest,unittest.mock as mock
from pathlib import Path
import acquire as a
S=json.loads((a.HERE/'selection.json').read_text())
class Response(io.BytesIO):
    def __init__(self,b=b'opaque fixture',headers=None,status=200,url=None):
        super().__init__(b);self.status=status;self.url=url or S['url'];self.headers=email.message.Message()
        for k,v in headers or [('ETag',S['opaque_etag']),('Content-Type','application/pdf')]:self.headers[k]=v
    def geturl(self):return self.url
class Opener:
    def __init__(self,fn):self.fn=fn;self.calls=[]
    def open(self,req,timeout):self.calls.append((req,timeout));return self.fn(len(self.calls))
class Tests(unittest.TestCase):
    def run_case(self,fn,success=False,sel=None,clock=None):
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)/'complete';op=Opener(fn)
            if success:
                result=a.acquire(sel or S,dest,op,clock or a.time.monotonic)
                self.assertEqual(len(op.calls),2);self.assertTrue(result['full_stream_compare'])
                self.assertEqual(op.calls[0][0].get_header('If-match'),S['opaque_etag'])
                self.assertEqual(op.calls[0][1],20);self.assertFalse(result['body_analysis'])
            else:
                with self.assertRaises(BaseException):a.acquire(sel or S,dest,op,clock or a.time.monotonic)
                self.assertFalse(dest.exists());self.assertEqual(list(Path(d).iterdir()),[])
    def test_success(self):self.run_case(lambda n:Response(),True)
    def test_length_success(self):self.run_case(lambda n:Response(headers=[('ETag',S['opaque_etag']),('Content-Type','APPLICATION/PDF'),('Content-Length','14')]),True)
    def test_headers(self):
        base=[('ETag',S['opaque_etag']),('Content-Type','application/pdf')]
        cases=[[],[('Content-Type','application/pdf')],[('ETag','W/'+S['opaque_etag']),('Content-Type','application/pdf')],[('ETag','"other"'),('Content-Type','application/pdf')],[('ETag',S['opaque_etag']),('Content-Type','text/html')]]
        cases += [base+[(name,value)] for name,value in [('Content-Length','014'),('Content-Length','+14'),('Content-Length','14,14'),('Content-Length','1048577'),('Content-Length','13'),('Content-Length','15'),('Content-Encoding','gzip'),('Transfer-Encoding','chunked'),('ETag',S['opaque_etag']),('Content-Type','application/pdf')]]
        cases += [base+[('Content-Length','14'),('Content-Length','14')]]
        for h in cases:
            with self.subTest(h=h):self.run_case(lambda n,h=h:Response(headers=h or [('X','none')]))
    def test_status_route(self):
        for status in [201,206,301,302,304,404,412]:self.run_case(lambda n,status=status:Response(status=status))
        self.run_case(lambda n:Response(url='https://other.invalid/'))
        self.assertIsNone(a.NoRedirect().redirect_request(None,None,302,None,None,None))
    def test_cap_empty_mismatch(self):
        sel=copy.deepcopy(S);sel['max_bytes']=13
        self.run_case(lambda n:Response(),sel=sel)
        self.run_case(lambda n:Response(b=b''))
        self.run_case(lambda n:Response(b=b'first' if n==1 else b'other'))
    def test_interrupt_timeout(self):
        def fail(n):
            if n==2:raise KeyboardInterrupt()
            return Response()
        self.run_case(fail)
        values=iter([0,121]);self.run_case(lambda n:Response(),clock=lambda:next(values))
    def test_truncate(self):
        class Bad(Response):
            def read(self,n=-1):raise IOError('truncated stream')
        self.run_case(lambda n:Bad())
    def test_compare_precedes_promotion(self):
        with mock.patch.object(a,'compare',side_effect=ValueError('cmp trap')):self.run_case(lambda n:Response())
    def test_parser_routes_trapped(self):
        import zipfile,subprocess
        with mock.patch.object(zipfile,'ZipFile',side_effect=AssertionError('parser')),mock.patch.object(subprocess,'run',side_effect=AssertionError('process')),mock.patch.object(a.os,'system',side_effect=AssertionError('shell')):
            self.run_case(lambda n:Response(),True)
    def test_existing_destination(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'existing';p.mkdir();op=Opener(lambda n:Response())
            with self.assertRaises(ValueError):a.acquire(S,p,op)
            self.assertEqual(op.calls,[])
if __name__=='__main__':unittest.main()
