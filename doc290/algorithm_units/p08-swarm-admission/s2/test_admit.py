import io,json,unittest,tempfile,hashlib
from pathlib import Path
from unittest.mock import patch
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
    def test_utf8_no_partial(self):
        with self.assertRaises(UnicodeError):admit.parse(b'valid\n\xff\n')
    def test_boundaries_raw(self):
        raw=b'\xef\xbb\xbfA\r\n\r\nB\rC\nD\x0bE\x0cF\n'
        d=admit.parse(raw)
        self.assertEqual([r['text'] for r in d['raw_lines']],['\ufeffA','','B','C','D','E','F'])
        self.assertEqual([r['raw_splitlines_ordinal'] for r in d['raw_lines']],list(range(1,8)))
        self.assertEqual((d['BOM_count'],d['VT_count'],d['FF_count']),(1,1,1))
    def test_no_numeric_or_quote_repair(self):
        d=admit.parse(b'nan\tinf -inf 1e999 bad\n"unfinished\n')
        self.assertEqual([r['text'] for r in d['raw_lines']],['nan\tinf -inf 1e999 bad','"unfinished'])
        json.dumps(d,allow_nan=False)
    def test_every_position_identity_gate(self):
        root=Path(admit.__file__).parent
        metadata=(root/'record-metadata.json').read_bytes()
        actual=json.loads((root/'selection.json').read_text())
        fake={**actual,'files':[{'path':f'f{i}.txt','url':f'https://fixed.test/{i}','metadata_size':3,'metadata_md5':hashlib.md5(b'abc').hexdigest()} for i in range(13)]}
        original_read=Path.read_text
        def read_text(p,*a,**kw):
            if p==root/'selection.json':return json.dumps(fake)
            return original_read(p,*a,**kw)
        for position in range(13):
            with self.subTest(position=position),tempfile.TemporaryDirectory() as t:
                payloads=[b'abc']*13;payloads[position]=b'bad'
                with patch.object(Path,'read_text',read_text),patch.object(admit,'download',side_effect=payloads),patch.object(admit,'parse') as parser:
                    admit.run(Path(t)/'out');parser.assert_not_called()
                d=json.loads((Path(t)/'out/inventory.json').read_text())
                self.assertFalse(d['analysis_performed'])
    def test_invalid_utf8_run(self):
        root=Path(admit.__file__).parent;actual=json.loads((root/'selection.json').read_text())
        fake={**actual,'files':[{'path':f'f{i}.txt','url':f'https://fixed.test/{i}','metadata_size':1,'metadata_md5':hashlib.md5(b'\xff' if i==0 else b'x').hexdigest()} for i in range(13)]}
        original_read=Path.read_text
        def read_text(p,*a,**kw):
            if p==root/'selection.json':return json.dumps(fake)
            return original_read(p,*a,**kw)
        with tempfile.TemporaryDirectory() as t,patch.object(Path,'read_text',read_text),patch.object(admit,'download',side_effect=[b'\xff']+[b'x']*12):
            admit.run(Path(t)/'out')
            d=json.loads((Path(t)/'out/inventory.json').read_text())['files']['f0.txt']
            self.assertEqual(d['status'],'invalid_utf8');self.assertNotIn('raw_lines',d)
            self.assertEqual((Path(t)/'out/sources/f0.txt').read_bytes(),b'\xff')
if __name__=='__main__':unittest.main()
