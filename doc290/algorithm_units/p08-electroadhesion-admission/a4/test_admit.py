import admit as a,scanner,io,zipfile,tempfile,unittest,gzip,json
from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
CAP={'max_entries':100000,'max_central_directory_bytes':16777216,'max_member_name_characters':4096}
def fixture(last=b'A,B\r\n'):
 f=io.BytesIO()
 with zipfile.ZipFile(f,'w') as z:
  z.writestr('OTHER.csv',b'no')
  for i in range(45):z.writestr('B/'+str(i)+'.csv',last if i==44 else b'A,B\r\n')
 raw=f.getvalue(); inv=scanner.directory(io.BytesIO(raw),CAP);s={'archive_bytes':len(raw),'archive_md5':scanner.hashlib.md5(raw).hexdigest(),'archive_sha256':scanner.sha(raw),'files':inv['entries'][1:],'selection_rule':{'exact_prefix':'B/','exact_suffix':'.csv'},'max_members':45,'max_member_bytes':16,'max_total_decompressed_bytes':225,'max_line_bytes':100000,'max_total_lines':45}
 return raw,s
def acquire(raw,s,root):
 p=root/'archive';p.write_bytes(raw);scratch=root/'raw';scratch.mkdir()
 with p.open('rb') as f:r=a.acquire(f,s,CAP,scratch)
 return r,scratch
class Tests(unittest.TestCase):
 def test_all45_selected_only(self):
  raw,s=fixture();real=zipfile.ZipFile.open;seen=[]
  def guarded(z,name,*args,**kwargs):
   self.assertIsInstance(name,zipfile.ZipInfo);self.assertTrue(name.filename.startswith('B/'));seen.append(name.filename);return real(z,name,*args,**kwargs)
  with tempfile.TemporaryDirectory() as d,ExitStack() as st:
   st.enter_context(patch.object(zipfile.ZipFile,'open',guarded))
   for method in ('read','extract','extractall','testzip'):st.enter_context(patch.object(zipfile.ZipFile,method,side_effect=AssertionError('route trap')))
   st.enter_context(patch('scanner.download',side_effect=AssertionError('fallback trap')));st.enter_context(patch('urllib.request.urlopen',side_effect=AssertionError('network trap')))
   root=Path(d);r,scratch=acquire(raw,s,root);self.assertEqual(len(seen),45);a.analyze_transaction(r,s,scratch,root/'inventory')
   a.analyze_transaction(r,s,scratch,root/'inventory2')
   for p in (root/'inventory').iterdir():self.assertEqual(p.read_bytes(),(root/'inventory2'/p.name).read_bytes())
 def test_exact_caps(self):
  raw,s=fixture()
  for field,value in [('max_member_bytes',4),('max_total_decompressed_bytes',224)]:
   bad=dict(s);bad[field]=value
   with tempfile.TemporaryDirectory() as d:
    with self.assertRaises(ValueError):acquire(raw,bad,Path(d))
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);r,scratch=acquire(raw,s,root)
   for field,value in [('max_total_lines',44),('max_line_bytes',2)]:
    bad=dict(s);bad[field]=value
    with self.assertRaises(ValueError):a.analyze_transaction(r,bad,scratch,root/field)
    self.assertFalse((root/field).exists())
 def test_late45_crc_and_encoding(self):
  raw,s=fixture();change=bytearray(raw);p=raw.rfind(b'A,B\r\n');change[p]=ord('Z');bad=dict(s);bad.update(archive_md5=scanner.hashlib.md5(change).hexdigest(),archive_sha256=scanner.sha(change))
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(zipfile.BadZipFile):acquire(change,bad,Path(d))
  raw,s=fixture(b'\xff')
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);r,scratch=acquire(raw,s,root)
   with self.assertRaises(UnicodeDecodeError):a.analyze_transaction(r,s,scratch,root/'inventory')
   self.assertFalse((root/'inventory').exists())
 def test_original_and_scratch_mutation(self):
  raw,s=fixture();real=a.identity;n=[0]
  def mutate(f,s):
   n[0]+=1
   if n[0]==2:f.seek(0);f.write(b'x');f.flush()
   return real(f,s)
  with tempfile.TemporaryDirectory() as d,patch('admit.identity',side_effect=mutate):
   with self.assertRaises(ValueError):acquire(raw,s,Path(d))
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);r,scratch=acquire(raw,s,root);(scratch/r[-1]['scratch_filename']).write_bytes(b'bad')
   with patch('admit.line_records',side_effect=AssertionError('analysis trap')):
    with self.assertRaises(ValueError):a.analyze_transaction(r,s,scratch,root/'inventory')
 def test_identity_metadata_zero_open(self):
  raw,s=fixture()
  with tempfile.TemporaryDirectory() as d,patch('scanner.directory',side_effect=AssertionError('parse trap')):
   bad=dict(s);bad['archive_sha256']='x'
   with self.assertRaises(ValueError):acquire(raw,bad,Path(d))
  with tempfile.TemporaryDirectory() as d,patch.object(zipfile.ZipFile,'open',side_effect=AssertionError('open trap')):
   bad=dict(s);bad['files']=s['files'][:-1]
   with self.assertRaises(ValueError):acquire(raw,bad,Path(d))
 def test_grammar_offsets_chunks(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x';s={'max_line_bytes':100000}
   p.write_bytes(b'A\r\n\rB\nC\v\f\xc2\x85\xe2\x80\xa8');x=list(a.line_records(p,s))
   self.assertEqual([r['byte_offset_0based'] for r in x],[0,3,4,6]);self.assertEqual([r['terminator'] for r in x],['CRLF','CR','LF','NONE']);self.assertIn('\u2028',x[-1]['text'])
   p.write_bytes(b'a'*65535+b'\r\n'+b'\xc3\xa9'+b'\n');x=list(a.line_records(p,s));self.assertEqual(x[0]['body_byte_count'],65535);self.assertEqual(x[1]['text'],'é')
   p.write_bytes(b'a'*65535+b'\xc3\xa9'+b'\n');x=list(a.line_records(p,s));self.assertTrue(x[0]['text'].endswith('é'))
   p.write_bytes(b'');self.assertEqual(list(a.line_records(p,s)),[])
   p.write_bytes(b'\n');self.assertEqual(len(list(a.line_records(p,s))),1)
 def test_late_disk_error_no_success(self):
  raw,s=fixture()
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);r,scratch=acquire(raw,s,root);real=a.line_records;n=[0]
   def fail(path,s):
    n[0]+=1
    if n[0]==45:raise OSError('disk trap')
    return real(path,s)
   with patch('admit.line_records',side_effect=fail):
    with self.assertRaises(OSError):a.analyze_transaction(r,s,scratch,root/'inventory')
   self.assertFalse((root/'inventory').exists());self.assertEqual((scratch/r[0]['scratch_filename']).read_bytes(),b'A,B\r\n')
if __name__=='__main__':unittest.main()
