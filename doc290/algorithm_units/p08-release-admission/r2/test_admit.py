import io,json,tempfile,unittest
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
        s={'metadata_size':3,'metadata_md5':'900150983cd24fb0d6963f7d28e17f72'};admit.verify(b'abc',s)
        for b in [b'ab',b'xyz']:
            with self.assertRaises(ValueError):admit.verify(b,s)
    def test_literal_xls(self):
        root=Path(admit.__file__).parent;e=json.loads((root/'environment.json').read_text());d=admit.parse((root/'fixtures/literal.xls').read_bytes(),e['caps']);s=d['sheets'][0];self.assertEqual(s['merged_ranges_0based_halfopen'],[[0,1,0,2]])
        cells={(c['row_1based'],c['column_1based']):c for c in s['cells']}
        self.assertEqual((cells[1,2]['ctype'],cells[1,3]['ctype']),(6,0));self.assertEqual((cells[2,2]['ctype'],cells[2,2]['value']),(5,7));self.assertEqual(cells[2,1]['value'],2.5);self.assertIn('NOT established',d['claims'])
    def test_malformed_unsupported(self):
        caps={'sheets':8,'rows_per_sheet':4096,'columns_per_sheet':128,'cells_total':65536}
        for b in [b'',b'not xls',b'PK\x03\x04malformed']:
            with self.assertRaises(Exception):admit.parse(b,caps)
    def test_all_caps_before_cell_access(self):
        class S:
            nrows=2;ncols=2;name='x';visibility=0;merged_cells=[]
            def cell(self,r,c):raise AssertionError('cell must not accessed on failed cap')
        class B:
            nsheets=1
            def sheets(self):return [S()]
        caps={'sheets':8,'rows_per_sheet':4096,'columns_per_sheet':128,'cells_total':65536}
        for k,v in [('sheets',0),('rows_per_sheet',1),('columns_per_sheet',1),('cells_total',3)]:
            with self.assertRaises(ValueError):admit.inventory(B(),{**caps,k:v})
    def test_identity_gates_parser(self):
        with tempfile.TemporaryDirectory() as t,patch.object(admit,'download',return_value=b'bad'),patch.object(admit,'parse') as parser:
            admit.run(Path(t)/'out');parser.assert_not_called();d=json.loads((Path(t)/'out/inventory.json').read_text());self.assertFalse(d['analysis_performed']);self.assertFalse(d['visual_performed'])
if __name__=='__main__':unittest.main()
