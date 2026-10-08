import importlib.util,json,tempfile,unittest,sys,zipfile,io,hashlib
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('wrapper',Path(__file__).parent/'continue.py');w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)
import admit as old,scanner
CAP={'max_entries':100000,'max_central_directory_bytes':16777216,'max_member_name_characters':4096}
def fixture(root):
 f=io.BytesIO()
 with zipfile.ZipFile(f,'w') as z:
  for i in range(45):z.writestr('B/'+str(i)+'.csv',b'A,B\r\n')
 raw=f.getvalue();archive=root/'archive';archive.write_bytes(raw);inv=scanner.directory(io.BytesIO(raw),CAP)
 sel={'archive_bytes':len(raw),'archive_md5':hashlib.md5(raw).hexdigest(),'archive_sha256':scanner.sha(raw),'files':inv['entries'],'selection_rule':{'exact_prefix':'B/','exact_suffix':'.csv'},'max_members':45,'max_member_bytes':16,'max_total_decompressed_bytes':225,'max_line_bytes':65536,'max_total_lines':45}
 scratch=root/'raw';scratch.mkdir()
 with archive.open('rb') as f:rs=old.acquire(f,sel,CAP,scratch)
 scanner.dump(root/'inputs.json',rs);return archive,scratch,sel,rs
def setup(root):
 archive,scratch,sel,rs=fixture(root);stage=root/'stage';stage.mkdir();keypath=root/'key';keypath.write_bytes(b'x'*32)
 w.save(stage,{'type':w.TYPE,'pins':w.codepins(),'raw_records':rs,'members':[]},keypath.read_bytes());return archive,scratch,sel,rs,stage,keypath
# isolated invocation with fixture selection, while preserving all algorithm gates
class PatchConfig:
 def __init__(self,sel):self.sel=sel
 def __enter__(self):
  self.orig=json.loads
  def loads(text,*args,**kwargs):
   x=self.orig(text,*args,**kwargs)
   if isinstance(x,dict) and x.get('max_members')==45 and 'files' in x:return self.sel
   return x
  self.p=patch('json.loads',side_effect=loads);self.p.start()
 def __exit__(self,*args):self.p.stop()
class Tests(unittest.TestCase):
 def test_resumed_identical(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);archive,scratch,sel,rs,stage,key=setup(root)
   with PatchConfig(sel):
    for i in range(15):r=w.run(stage,scratch,archive,key,'batch');self.assertLessEqual(r['members_processed_this_call'],3)
    w.run(stage,scratch,archive,key,'final',root/'success')
   old.analyze_transaction(rs,sel,scratch,root/'original')
   self.assertEqual({p.name:p.read_bytes() for p in (root/'success').iterdir()},{p.name:p.read_bytes() for p in (root/'original').iterdir()})
 def test_coherent_mutation_reject(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);archive,scratch,sel,rs,stage,key=setup(root)
   with PatchConfig(sel):w.run(stage,scratch,archive,key,'batch')
   doc=json.loads((stage/'state.json').read_text());doc['payload']['members'][0]['line_count']=999
   scanner.dump(stage/'state.json',doc)
   with PatchConfig(sel):
    with self.assertRaises(ValueError):w.run(stage,scratch,archive,key,'batch')
 def test_gzip_changed(self):
  for append in (b'x',b'\x1f\x8b\x08'+b'junk',b''):
   with tempfile.TemporaryDirectory() as d:
    root=Path(d);archive,scratch,sel,rs,stage,key=setup(root)
    with PatchConfig(sel):w.run(stage,scratch,archive,key,'batch')
    p=next(stage.glob('*.gz'));raw=p.read_bytes();p.write_bytes(raw+append if append else raw[:-1])
    with PatchConfig(sel):
     with self.assertRaises(ValueError):w.run(stage,scratch,archive,key,'final',root/'success')
    self.assertFalse((root/'success').exists())
 def test_raw_swap_and_foreign(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);archive,scratch,sel,rs,stage,key=setup(root);p=scratch/rs[-1]['scratch_filename'];p.write_bytes(b'Z,Z\r\n')
   with PatchConfig(sel),patch.object(w,'replay',side_effect=AssertionError('analysis trap')):
    with self.assertRaises(ValueError):w.run(stage,scratch,archive,key,'batch')
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);archive,scratch,sel,rs,stage,key=setup(root);(stage/'temp.gz').write_bytes(b'bad')
   with PatchConfig(sel):
    with self.assertRaises(ValueError):w.run(stage,scratch,archive,key,'batch')
 def test_final_change_after_receipt(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);archive,scratch,sel,rs,stage,key=setup(root)
   with PatchConfig(sel):
    for i in range(15):w.run(stage,scratch,archive,key,'batch')
   archive.write_bytes(b'x'+archive.read_bytes()[1:])
   with PatchConfig(sel):
    with self.assertRaises(ValueError):w.run(stage,scratch,archive,key,'final',root/'success')
   self.assertFalse((root/'success').exists())
if __name__=='__main__':unittest.main()
