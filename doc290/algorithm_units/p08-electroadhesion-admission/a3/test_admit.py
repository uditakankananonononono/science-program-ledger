import admit as a,scanner,io,os,zipfile,tempfile,unittest
from unittest.mock import patch
from contextlib import ExitStack
from pathlib import Path
CAP={'max_entries':100000,'max_central_directory_bytes':16777216,'max_member_name_characters':4096}
def fixture():
 f=io.BytesIO()
 with zipfile.ZipFile(f,'w') as z:z.writestr('other.csv',b'not read');z.writestr('Data/README.txt',b'A\r\n\rB\nC\v\f\xc2\x85\xe2\x80\xa8')
 raw=f.getvalue(); inv=scanner.directory(io.BytesIO(raw),CAP)
 return raw,{'archive_bytes':len(raw),'archive_md5':scanner.hashlib.md5(raw).hexdigest(),'archive_sha256':scanner.sha(raw),'files':[inv['entries'][1]],'max_decompressed_bytes':65536,'max_text_lines':1000,'max_line_characters':16384}
class Tests(unittest.TestCase):
 def test_line_grammar(self):
  raw,s=fixture();x=a.lines(b'A\r\n\rB\nC\v\f\xc2\x85\xe2\x80\xa8',s)
  self.assertEqual([r['terminator'] for r in x['lines']],['CRLF','CR','LF','NONE']);self.assertEqual(x['lines'][1]['text'],'');self.assertIn('\u2028',x['lines'][-1]['text']);self.assertEqual(a.lines(b'\n',s)['lines'],[{'line_ordinal_1based':1,'text':'','terminator':'LF'}]);self.assertTrue(a.lines(b'',s)['empty_original'])
 def test_selected_only_traps(self):
  raw,s=fixture();real=zipfile.ZipFile.open;opens=[]
  def guarded(z,name,*args,**kwargs):
   self.assertIsInstance(name,zipfile.ZipInfo);self.assertEqual(name.filename,'Data/README.txt');opens.append(name.filename);return real(z,name,*args,**kwargs)
  with tempfile.TemporaryFile() as f,ExitStack() as stack:
   f.write(raw);f.flush()
   stack.enter_context(patch.object(zipfile.ZipFile,'open',guarded))
   for method in ('read','extract','extractall','testzip'):stack.enter_context(patch.object(zipfile.ZipFile,method,side_effect=AssertionError('route trap')))
   stack.enter_context(patch('scanner.download',side_effect=AssertionError('fallback trap')));stack.enter_context(patch('urllib.request.urlopen',side_effect=AssertionError('network trap')))
   result=a.read_selected(f,s,CAP)
  self.assertEqual(len(opens),1);self.assertEqual(len(result),s['files'][0]['uncompressed_size'])
 def test_identity_and_metadata(self):
  raw,s=fixture()
  with tempfile.TemporaryFile() as f:
   f.write(raw);f.flush();bad=dict(s);bad['archive_sha256']='x'
   with patch('scanner.directory',side_effect=AssertionError('parse trap')):
    with self.assertRaises(ValueError):a.read_selected(f,bad,CAP)
   bad=dict(s);bad['files']=[dict(s['files'][0],ordinal_1based=1)]
   with patch.object(zipfile.ZipFile,'open',side_effect=AssertionError('open trap')):
    with self.assertRaises(ValueError):a.read_selected(f,bad,CAP)
 def test_caps_encoding(self):
  raw,s=fixture();bad=dict(s);bad['max_decompressed_bytes']=1
  with tempfile.TemporaryFile() as f:
   f.write(raw);f.flush()
   with self.assertRaises(ValueError):a.read_selected(f,bad,CAP)
  for raw in (b'\xff',):
   with self.assertRaises(UnicodeDecodeError):a.lines(raw,s)
  for k in ('max_text_lines','max_line_characters'):
   bad=dict(s);bad[k]=0
   with self.assertRaises(ValueError):a.lines(b'long\n',bad)
 def test_crc_and_mutation(self):
  raw,s=fixture();changed=bytearray(raw);p=raw.index(b'A\r\n');changed[p]=ord('Z');bad=dict(s);bad.update(archive_md5=scanner.hashlib.md5(changed).hexdigest(),archive_sha256=scanner.sha(changed))
  with tempfile.TemporaryFile() as f:
   f.write(changed);f.flush()
   with self.assertRaises(zipfile.BadZipFile):a.read_selected(f,bad,CAP)
  with tempfile.TemporaryFile() as f:
   f.write(raw);f.flush();real=a.identity;n=[0]
   def mutate(f,s):
    n[0]+=1
    if n[0]==2:f.seek(0);f.write(b'x');f.flush()
    return real(f,s)
   with patch('admit.identity',side_effect=mutate):
    with self.assertRaises(ValueError):a.read_selected(f,s,CAP)
if __name__=='__main__':unittest.main()
