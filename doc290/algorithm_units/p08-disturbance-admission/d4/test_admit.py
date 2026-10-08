import io,json,struct,tempfile,unittest,builtins
from pathlib import Path
from unittest.mock import patch
import admit
CAP={'opcodes':10000,'argument_repr_characters':4096}
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
        u='https://fixed.test/file';self.assertEqual(admit.download(u,8,[8],Opener(Response(b'abc',{'Content-Length':'3'}))),b'abc')
        for r in [Response(b'a',{'Content-Length':'2'}),Response(b'a',{'Content-Encoding':'gzip'}),Response(b'a',url='https://other.test/'),Response(b'abc',{'Content-Length':'9'}),Response(b'a',{'Content-Length':'x'}),Response(b'abc')]:
            with self.assertRaises(ValueError):admit.download(u,3,[3],Opener(r))
    def test_offsets_stop_trailing(self):
        d=admit.disassemble(b'N.',CAP);self.assertEqual(d['status'],'static_complete_opcode_stream');self.assertEqual(d['STOP_byte_offset_0based'],1)
        d=admit.disassemble(b'N.extra\x00',CAP);self.assertEqual(d['trailing_byte_count'],6);self.assertEqual(d['status'],'static_prefix_with_trailing_bytes');self.assertEqual(d['trailing_sha256'],admit.sha(b'extra\x00'))
    def test_malformed_no_partial(self):
        for b in [b'N',b'?',b'X\x05\x00\x00\x00ab']:
            d=admit.disassemble(b,CAP);self.assertEqual(d['status'],'unresolved_syntax_or_cap');self.assertNotIn('opcodes',d)
    def test_repr_nonfinite_unicode_caps(self):
        d=admit.disassemble(b'G'+struct.pack('>d',float('nan'))+b'.',CAP);self.assertEqual(d['opcodes'][0]['argument_literal_repr'],'nan');json.dumps(d,allow_nan=False)
        raw=b'Vhello\\u2028world\n.';d=admit.disassemble(raw,CAP);self.assertIn('hello',d['opcodes'][0]['argument_literal_repr'])
        for caps in [{**CAP,'opcodes':1},{**CAP,'argument_repr_characters':2}]:
            d=admit.disassemble(b'Vlongliteral\n.',caps);self.assertEqual(d['status'],'unresolved_syntax_or_cap');self.assertNotIn('opcodes',d)
    def test_executable_trap(self):
        raw=b'cbuiltins\neval\n(S\'1+1\'\ntR.'
        with patch.object(builtins,'eval',side_effect=AssertionError('CALLABLE INVOKED')) as trap:
            d=admit.disassemble(raw,CAP);trap.assert_not_called()
        self.assertIn('REDUCE',[r['opcode'] for r in d['opcodes']]);self.assertIn('GLOBAL',[r['opcode'] for r in d['opcodes']])
    def test_identity_gate(self):
        with tempfile.TemporaryDirectory() as t,patch.object(admit,'download',return_value=b'bad'),patch.object(admit,'disassemble') as dis:
            admit.run(Path(t)/'out');dis.assert_not_called();self.assertFalse(json.loads((Path(t)/'out/inventory.json').read_text())['analysis_performed'])
if __name__=='__main__':unittest.main()
