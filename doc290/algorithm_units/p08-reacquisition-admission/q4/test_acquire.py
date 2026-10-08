import copy,email.message,io,json,tempfile,unittest,unittest.mock as mock
from pathlib import Path
import acquire as a
S={'url':'https://fixture.invalid/fixed','metadata_bytes':10,'range_bytes':4,'stream_chunk_bytes':3,'max_archive_bytes':12,'ranges_per_invocation':3}
class Resp(io.BytesIO):
    def __init__(self,lo,hi,b=b'abcdefghij',status=206,headers=None):
        super().__init__(b[lo:hi+1]);self.status=status;self.headers=email.message.Message()
        for k,v in headers or [('Content-Type','application/octet-stream'),('Content-Range',f'bytes {lo}-{hi}/10'),('Content-Length',str(hi-lo+1))]:self.headers[k]=v
    def geturl(self):return S['url']
class Op:
    def __init__(self,fail=None):self.calls=[];self.fail=fail
    def open(self,r,timeout):
        self.calls.append(r);lo,hi=map(int,r.get_header('Range')[6:].split('-'))
        if self.fail:return self.fail(len(self.calls),lo,hi)
        return Resp(lo,hi)
class Tests(unittest.TestCase):
    def test_complete_last_remainder(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'state';op=Op();self.assertEqual(a.batch(p,S,op)['completed_ranges'],3);self.assertEqual(a.batch(p,S,op)['completed_ranges'],6)
            m=a.batch(p,S,op);self.assertTrue(m['full_stream_compare']);self.assertEqual(len(op.calls),6)
            self.assertEqual(a.load(p/'checkpoint.json')['receipts'][-1]['bytes'],2)
            self.assertEqual((p/'opaque-pass1.bin').read_bytes(),b'abcdefghij')
    def failure(self,fn):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'state';op=Op(fn)
            with self.assertRaises(BaseException):a.batch(p,S,op)
            self.assertTrue((p/'TERMINAL-FAILED.json').exists());calls=len(op.calls)
            with self.assertRaises(ValueError):a.batch(p,S,op)
            self.assertEqual(calls,len(op.calls));self.assertFalse((p/'manifest.json').exists())
    def test_headers(self):
        for h in [[('Content-Type','text/html'),('Content-Range','bytes 0-3/10'),('Content-Length','4')],[('Content-Type','application/octet-stream'),('Content-Range','bytes 0-3/11'),('Content-Length','4')],[('Content-Type','application/octet-stream'),('Content-Range','bytes 0-3/10'),('Content-Length','04')],[('Content-Type','application/octet-stream'),('Content-Range','bytes 0-3/10'),('Content-Length','4'),('Content-Length','4')]]:
            self.failure(lambda n,lo,hi,h=h:Resp(lo,hi,headers=h))
        self.failure(lambda n,lo,hi:Resp(lo,hi,status=200))
    def test_late_pass2_terminal(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'state';op=Op();a.batch(p,S,op)
            fail=Op(lambda n,lo,hi:Resp(lo,hi,status=200 if n==3 else 206))
            with self.assertRaises(ValueError):a.batch(p,S,fail)
            self.assertTrue((p/'TERMINAL-FAILED.json').exists());self.assertFalse((p/'manifest.json').exists())
    def test_mutation_paths_types(self):
        for action in ['chunk','count','hash','pass','foreign','missing','path','duplicate','bool','inflight','orphan']:
            with self.subTest(action=action),tempfile.TemporaryDirectory() as d:
                p=Path(d)/'state';op=Op();a.batch(p,S,op);c=a.load(p/'checkpoint.json')
                if action=='chunk':(p/c['receipts'][0]['file']).write_bytes(b'abcd'[:: -1])
                elif action=='foreign':(p/'extra').write_text('x')
                elif action=='missing':(p/c['receipts'][0]['file']).unlink()
                elif action=='orphan':(p/'checkpoint.json.tmp').write_text('{}')
                elif action=='duplicate':(p/'checkpoint.json').write_text('{"version":1,"version":1}')
                else:
                    if action=='count':c['receipts'][0]['bytes']=3
                    if action=='hash':c['receipts'][0]['sha256']='0'*64
                    if action=='pass':c['receipts'][0]['pass']=2
                    if action=='path':c['receipts'][0]['file']='../foreign'
                    if action=='bool':c['receipts'][0]['index']=False
                    if action=='inflight':c['inflight']={'pass':2,'index':0}
                    (p/'checkpoint.json').write_text(json.dumps(c))
                before=len(op.calls)
                with self.assertRaises(ValueError):a.batch(p,S,op)
                self.assertEqual(before,len(op.calls));self.assertTrue((p/'TERMINAL-FAILED.json').exists())
    def test_interrupted_chunk(self):
        self.failure(lambda n,lo,hi:(_ for _ in ()).throw(KeyboardInterrupt()))
    def test_compare_before_success(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'state';a.batch(p,S,Op());a.batch(p,S,Op())
            with mock.patch.object(a,'compare',side_effect=ValueError('cmp')):
                with self.assertRaises(ValueError):a.batch(p,S,Op())
            self.assertFalse((p/'manifest.json').exists());self.assertTrue((p/'TERMINAL-FAILED.json').exists())
    def test_no_parser(self):
        import zipfile,subprocess
        with mock.patch.object(zipfile,'ZipFile',side_effect=AssertionError('parser')),mock.patch.object(subprocess,'run',side_effect=AssertionError('execution')),tempfile.TemporaryDirectory() as d:
            p=Path(d)/'state';a.batch(p,S,Op());a.batch(p,S,Op());a.batch(p,S,Op())
if __name__=='__main__':unittest.main()

class MoreControls(unittest.TestCase):
    def test_atomic_windows(self):
        for point in ['inflight','rename','receipt']:
            with self.subTest(point=point),tempfile.TemporaryDirectory() as d:
                p=Path(d)/'state';real=a.atomic;rename=a.os.rename
                def atomic(path,value):
                    if point=='inflight' and value.get('inflight'):real(path,value);raise KeyboardInterrupt()
                    if point=='receipt' and value.get('receipts'):raise KeyboardInterrupt()
                    return real(path,value)
                def ren(src,dest):
                    rename(src,dest)
                    if point=='rename':raise KeyboardInterrupt()
                with mock.patch.object(a,'atomic',side_effect=atomic),mock.patch.object(a.os,'rename',side_effect=ren):
                    with self.assertRaises(KeyboardInterrupt):a.batch(p,S,Op())
                self.assertTrue((p/'TERMINAL-FAILED.json').exists())
                op=Op()
                with self.assertRaises(ValueError):a.batch(p,S,op)
                self.assertEqual(op.calls,[])
    def test_disk_before_write(self):
        with tempfile.TemporaryDirectory() as d,mock.patch.object(a,'DISK_CAP',10):
            p=Path(d)/'state'
            with self.assertRaises(ValueError):a.batch(p,S,Op())
            self.assertTrue((p/'TERMINAL-FAILED.json').exists())
    def test_complete_mutation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'state';a.batch(p,S,Op());a.batch(p,S,Op());a.batch(p,S,Op())
            (p/'opaque-pass2.bin').write_bytes(b'jihgfedcba')
            with self.assertRaises(ValueError):a.batch(p,S,Op())
            self.assertTrue((p/'TERMINAL-FAILED.json').exists())
    def test_checkpoint_duplicate_receipt_and_foreign_binding(self):
        for kind in ['receipt','binding']:
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'state';a.batch(p,S,Op());c=a.load(p/'checkpoint.json')
                if kind=='receipt':c['receipts'].append(c['receipts'][0])
                else:c['binding']['code_sha256']='0'*64
                (p/'checkpoint.json').write_text(json.dumps(c))
                op=Op()
                with self.assertRaises(ValueError):a.batch(p,S,op)
                self.assertEqual(op.calls,[])
