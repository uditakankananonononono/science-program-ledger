import io,json,tempfile,unittest,zipfile
from pathlib import Path
try:
    import numpy as np
    from PIL import Image
    from batch_extract_qc import run_batch
    AVAILABLE=True
except ImportError:AVAILABLE=False

@unittest.skipUnless(AVAILABLE,'optional imaging dependencies unavailable')
class BatchTests(unittest.TestCase):
    def archive(self,path,gray=False):
        a=np.zeros((5,5),dtype=np.uint8);a[2,1:4]=128 if gray else 255
        stream=io.BytesIO();Image.fromarray(a).save(stream,format='PNG')
        with zipfile.ZipFile(path,'w') as z:z.writestr('mask.png',stream.getvalue())
    def test_real_resume_and_retained_failure(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'a.zip';b=Path(d)/'b.zip';out=Path(d)/'qc.jsonl'
            self.archive(a);self.archive(b,True)
            sources=[('good',str(a)),('bad',str(b))]
            first=run_batch(sources,out,5)
            self.assertTrue(first['complete']);self.assertEqual(first['counts']['bad']['failed'],1)
            before=out.read_bytes();second=run_batch(sources,out,5)
            self.assertEqual(first,second);self.assertEqual(out.read_bytes(),before)
    def test_input_mutation_rejected_before_append(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'a.zip';out=Path(d)/'qc.jsonl';self.archive(a)
            sources=[('a',str(a))];run_batch(sources,out,5);before=out.read_bytes()
            self.archive(a,True)
            with self.assertRaises(ValueError):run_batch(sources,out,5)
            self.assertEqual(out.read_bytes(),before)
    def test_duplicate_legacy_and_pipeline_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'a.zip';out=Path(d)/'qc.jsonl';self.archive(a);sources=[('a',str(a))]
            run_batch(sources,out,5);row=json.loads(out.read_text())
            for records in ([row,row],[{'dataset':'a','member':'mask.png','status':'passed'}],[dict(row,pipeline_sha256='bad')]):
                out.write_text(''.join(json.dumps(x)+'\n' for x in records));before=out.read_bytes()
                with self.assertRaises(ValueError):run_batch(sources,out,5)
                self.assertEqual(out.read_bytes(),before)
    def test_zero_window_and_duplicate_sources(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'a.zip';out=Path(d)/'qc.jsonl';self.archive(a)
            got=run_batch([('a',str(a))],out,0)
            self.assertFalse(got['complete']);self.assertEqual(got['counts']['a']['processed'],0)
            with self.assertRaises(ValueError):run_batch([('a',str(a)),('a',str(a))],out,1)
