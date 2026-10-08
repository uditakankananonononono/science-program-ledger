import base64,io,json,tempfile,unittest
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
    def test_json(self):
        for b in [b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":Infinity}',b'\xff']:
            with self.assertRaises((ValueError,UnicodeError)):admit.strict_json(b)
    def test_envelope(self):
        s={'url':'https://fixed.test/file','metadata_size':1,'git_blob_sha1':admit.blobsha(b'x')}
        j={'url':s['url'],'size':1,'sha':s['git_blob_sha1'],'encoding':'base64','content':'eA==\n'}
        self.assertEqual(admit.envelope(json.dumps(j).encode(),s,3),b'x')
        for key,value in [('size',True),('size',2),('content','e A=='),('content','eA='),('content','eB=='),('content','eA==\r'),('sha','0'*40),('encoding','utf8')]:
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):admit.envelope(json.dumps({**j,key:value}).encode(),s,3)
        with self.assertRaises(ValueError):admit.envelope(json.dumps(j).encode(),s,0)
    def test_pointers(self):
        p='version https://git-lfs.github.com/spec/v1\noid sha256:'+'a'*64+'\nsize 999999999999\n'
        d=admit.parse(p.encode(),'x.pkl');self.assertEqual(d['declared_payload_size'],999999999999);self.assertFalse(d['payload_accessed'])
        for separator in ['\v','\f','\u2028','\u0085','\r\n']:
            bad=p.replace('\n',separator,2)
            self.assertEqual(admit.parse(bad.encode(),'x.pkl')['format'],'unresolved_pointer_like')
        for bad in [p.replace('size 999999999999','size -1'),p.replace('size 999999999999','size 01'),p.replace('a'*64,'z'*64),p+'extra\n',p.rstrip('\n')]:
            self.assertEqual(admit.parse(bad.encode(),'x.pkl')['format'],'unresolved_pointer_like')
    def test_notebook(self):
        j={'nbformat':4,'cells':[{'cell_type':'code','source':['DO NOT EXECUTE\n'],'outputs':[{'text':'untrusted result'}]}]}
        d=admit.parse(json.dumps(j).encode(),'x.ipynb');self.assertFalse(d['static_cells'][0]['executed']);self.assertFalse(d['outputs_used_as_evidence'])
        for source in [5,[5],None]:
            with self.assertRaises(ValueError):admit.parse(json.dumps({'nbformat':4,'cells':[{'cell_type':'code','source':source}]}).encode(),'x.ipynb')
    def test_utf8_boundaries(self):
        with self.assertRaises(UnicodeError):admit.parse(b'valid\n\xff','x')
        d=admit.parse('\ufeffA\r\n\r\nB\vC\fD\u2028nan inf bad'.encode(),'x')
        self.assertEqual([r['text'] for r in d['raw_lines']],['\ufeffA','','B','C','D','nan inf bad'])
    def test_binding(self):
        root=Path(admit.__file__).parent;sel=admit.strict_json((root/'selection.json').read_bytes());c=admit.strict_json((root/'commit-metadata.json').read_bytes());t=admit.strict_json((root/'pinned-tree-metadata.json').read_bytes());admit.binding(sel,c,t)
        for changed in [{**t,'truncated':True},{**t,'sha':'0'*40}]:
            with self.assertRaises(ValueError):admit.binding(sel,c,changed)
        with self.assertRaises(ValueError):admit.binding(sel,{**c,'sha':'0'*40},t)
        x=json.loads(json.dumps(sel));x['files'][0]['metadata_size']=True
        with self.assertRaises(ValueError):admit.binding(x,c,t)
    def test_all62_gate(self):
        root=Path(admit.__file__).parent;actual=admit.strict_json((root/'selection.json').read_bytes());payload=b'x'
        files=[{'path':f'f{i}.txt','url':f'https://fixed.test/{i}','metadata_size':1,'git_blob_sha1':admit.blobsha(payload)} for i in range(62)];fake={**actual,'files':files};envelopes=[json.dumps({'url':s['url'],'size':1,'sha':s['git_blob_sha1'],'encoding':'base64','content':'eA=='}).encode() for s in files]
        original=Path.read_bytes
        original_text=Path.read_text
        def read_text(p,*a,**kw):
            if p==root/'freeze-hashes.sha256':
                return ''.join((admit.sha(json.dumps(fake).encode()) if n=='selection.json' else h)+'  '+n+'\n' for h,n in [line.split('  ',1) for line in original_text(p).splitlines()])
            return original_text(p,*a,**kw)
        def read(p):
            if p==root/'selection.json':return json.dumps(fake).encode()
            return original(p)
        for i in range(62):
            with self.subTest(position=i),tempfile.TemporaryDirectory() as t:
                objects=envelopes.copy();objects[i]=b'{}'
                with patch.object(Path,'read_text',read_text),patch.object(Path,'read_bytes',read),patch.object(admit,'binding'),patch.object(admit,'download',side_effect=objects),patch.object(admit,'parse') as parser:
                    admit.run(Path(t)/'out');parser.assert_not_called()
                self.assertFalse(json.loads((Path(t)/'out/inventory.json').read_text())['analysis_performed'])
if __name__=='__main__':unittest.main()
