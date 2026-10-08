import io,json,tempfile,unittest,urllib.error
from pathlib import Path
from unittest.mock import patch
import fetch_amend1 as a
URL='https://fixed.test/a'
def dns(host,port,type):return [(2,1,6,'',('8.8.8.8',port))]
class R(io.BytesIO):
    def __init__(self,url,status=200,loc=None,data=b'abc'):
        super().__init__(data);self.url=url;self.status=status;self.headers={'Content-Length':str(len(data))}
        if loc is not None:self.headers['Location']=loc
    def geturl(self):return self.url
class O:
    def __init__(self,responses):self.responses=iter(responses);self.calls=[]
    def open(self,req,timeout):self.calls.append(req);return next(self.responses)
class Tests(unittest.TestCase):
    def test_hops(self):
        for n in range(4):
            urls=[URL]+[f'https://fixed.test/{i}' for i in range(n)]
            rs=[R(u,302,urls[i+1]) for i,u in enumerate(urls[:-1])]+[R(urls[-1])];o=O(rs);chain=[]
            self.assertEqual(a.fetch(URL,8,[8],chain,o,dns),b'abc');self.assertEqual(len(o.calls),n+1)
            for req in o.calls:self.assertNotIn('Authorization',req.headers);self.assertNotIn('Cookie',req.headers)
    def test_fourth(self):
        urls=[URL]+[f'https://fixed.test/{i}' for i in range(4)];o=O([R(u,302,urls[i+1]) for i,u in enumerate(urls[:-1])]);chain=[]
        with self.assertRaises(ValueError):a.fetch(URL,8,[8],chain,o,dns)
        self.assertEqual(len(o.calls),4);self.assertIn('fourth',chain[-1]['error'])
    def test_relative_loop(self):
        o=O([R(URL,302,'/b'),R('https://fixed.test/b')]);c=[];self.assertEqual(a.fetch(URL,8,[8],c,o,dns),b'abc');self.assertEqual(c[0]['resolved_url'],'https://fixed.test/b')
        o=O([R(URL,302,URL)]);c=[]
        with self.assertRaises(ValueError):a.fetch(URL,8,[8],c,o,dns)
        self.assertEqual(len(o.calls),1)
    def test_unsafe(self):
        for loc in ['https://localhost/x','https://127.0.0.1/x','https://user:pass@fixed.test/x','https://fixed.test:444/x','/x#f','/x\n','',None,'http://fixed.test/x','https://fixed.local/x']:
            o=O([R(URL,302,loc)]);c=[]
            with self.assertRaises(ValueError):a.fetch(URL,8,[8],c,o,dns)
            self.assertEqual(len(o.calls),1)
        for ip in ['127.0.0.1','10.0.0.1','169.254.1.2','::1','fc00::1']:
            def private(host,port,type):return [(2,1,6,'',(ip,port))]
            o=O([])
            with self.assertRaises(ValueError):a.fetch(URL,8,[8],[],o,private)
            self.assertEqual(len(o.calls),0)
    def test_final_and_implicit(self):
        for r in [R(URL,404),R('https://other.test/x')]:
            with self.assertRaises(ValueError):a.fetch(URL,8,[8],[],O([r]),dns)
    def test_identity_gate(self):
        with tempfile.TemporaryDirectory() as t,patch.object(a,'fetch',return_value=b'bad'),patch.object(a.admit,'parse') as parser:
            a.run(Path(t)/'out');parser.assert_not_called();j=json.loads((Path(t)/'out/identity.json').read_text());self.assertEqual(j['status'],'unavailable');self.assertFalse(j['visual_performed'])
if __name__=='__main__':unittest.main()
