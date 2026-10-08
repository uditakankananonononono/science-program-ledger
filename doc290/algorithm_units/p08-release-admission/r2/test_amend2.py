import io,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import fetch_amend2 as a
URL='https://fixed.test/a';IPS=['2001:4860:4860::8888','8.8.8.8']
class R(io.BytesIO):
    status=200;headers={'Content-Length':'3'}
    def __init__(self):super().__init__(b'abc')
class C:
    made=[];fail_first=True;phase=None
    def __init__(self,host,ip):self.host=host;self.ip=ip;self.closed=False;self.tls=False;self.headers={};self.events=[];C.made.append(self)
    def connect(self):
        self.events.append('connect')
        if self.ip==IPS[0] and C.fail_first:raise OSError('IPv6 no route')
        self.tls=True
    def close(self):self.closed=True
    def putrequest(self,*args,**kw):
        assert self.tls;self.events.append('request')
    def putheader(self,k,v):self.headers[k]=v
    def endheaders(self):
        if C.phase=='write':raise OSError('partial write')
    def getresponse(self):
        if C.phase=='read':raise OSError('partial read')
        return R()
class Tests(unittest.TestCase):
    def setUp(self):C.made=[];C.fail_first=True;C.phase=None
    def test_failover_records(self):
        step={};r=a.request(URL,{'dns_addresses':IPS},step,C);self.assertEqual(len(C.made),2);self.assertTrue(C.made[0].closed);self.assertEqual(step['successful_address'],IPS[1]);self.assertIn('IPv6',step['address_attempts'][0]['error']);self.assertEqual(C.made[1].events,['connect','request']);self.assertEqual(C.made[1].headers['Host'],'fixed.test');r.close()
    def test_all_fail(self):
        class F(C):
            def connect(self):raise OSError('fail')
        step={}
        with self.assertRaises(OSError):a.request(URL,{'dns_addresses':IPS},step,F)
        self.assertEqual(len(step['address_attempts']),2);self.assertTrue(all(c.closed for c in C.made))
    def test_no_failover_after_tls(self):
        for phase in ['write','read']:
            C.made=[];C.fail_first=False;C.phase=phase
            with self.assertRaises(OSError):a.request(URL,{'dns_addresses':IPS},{},C)
            self.assertEqual(len(C.made),1);self.assertTrue(C.made[0].closed)
    def test_reconnect_guard(self):
        c=a.Connection('fixed.test','8.8.8.8');c.connect_called=True
        with self.assertRaises(ValueError):c.connect()
        with patch.object(a.previous.PinnedHTTPSConnection,'connect'):
            c=a.Connection('fixed.test','8.8.8.8');c.connect();self.assertEqual(c.auto_open,0)
            with self.assertRaises(ValueError):c.connect()
    def test_once_dns_and_pin(self):
        calls=[]
        def dns(host,port,type):calls.append(host);return [(2,1,6,'',('8.8.8.8',port))]
        def requester(url,checked,step):return a.previous.PinnedResponse(R(),C('fixed.test',checked['dns_addresses'][0]),url)
        self.assertEqual(a.fetch(URL,8,[8],[],dns,requester),b'abc');self.assertEqual(calls,['fixed.test'])
    def test_identity_gate(self):
        with tempfile.TemporaryDirectory() as t,patch.object(a,'fetch',return_value=b'bad'),patch.object(a.admit,'parse') as parser:
            a.run(Path(t)/'out');parser.assert_not_called();j=json.loads((Path(t)/'out/identity.json').read_text());self.assertEqual(j['status'],'unavailable');self.assertFalse(j['visual_performed'])
if __name__=='__main__':unittest.main()
