import admit as a,io,struct,tempfile,unittest,zipfile,hashlib
from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
S={'max_entries':100000,'max_central_directory_bytes':16777216,'max_member_name_characters':4096}
def blob(name='d/readme.txt'):
 f=io.BytesIO()
 with zipfile.ZipFile(f,'w') as z:z.writestr(name,b'not read')
 return f.getvalue()
def pin(raw):return {'metadata_size':len(raw),'metadata_md5':hashlib.md5(raw).hexdigest()}
class Tests(unittest.TestCase):
 def test_no_member_routes(self):
  with tempfile.TemporaryFile() as f:
   raw=blob();f.write(raw);f.flush()
   with ExitStack() as stack:
    for method in ('open','read','extract','extractall','testzip'):stack.enter_context(patch.object(zipfile.ZipFile,method,side_effect=AssertionError('member route trap')))
    h,v=a.inspect(f,pin(raw),S)
   self.assertEqual(v['entry_count'],1);self.assertEqual(v['entries'][0]['filename'],'d/readme.txt')
 def test_identity_zero_parse(self):
  with tempfile.TemporaryFile() as f:
   f.write(blob())
   with patch('admit.directory',side_effect=AssertionError('parse trap')):
    with self.assertRaises(ValueError):a.inspect(f,{'metadata_size':1,'metadata_md5':'x'},S)
 def test_unsafe(self):
  for name in ('../escape','/absolute','C:\\drive','d/../escape','\\absolute'):
   with self.assertRaises(ValueError):a.directory(io.BytesIO(blob(name)),S)
  for name,flag,creator,attr in [('x\x00',0,0,0),('x',1,0,0),('x',64,0,0),('x',0,3<<8,0o120777<<16)]:
   with self.assertRaises(ValueError):a.unsafe(name,flag,creator,attr)
 def test_count_range_zip64_eocd(self):
  good=blob();offset=len(good)-22
  changes=[(offset+4,'H',1),(offset+6,'H',1),(offset+8,'H',2),(offset+10,'H',65535),(offset+12,'I',4294967295),(offset+16,'I',0)]
  for pos,fmt,val in changes:
   raw=bytearray(good);struct.pack_into('<'+fmt,raw,pos,val)
   with self.assertRaises(ValueError):a.directory(io.BytesIO(raw),S)
  for raw in (good+b'x',good[:-1],good[:-22]+b'PK\x06\x07'+b'\0'*16+good[-22:]):
   with self.assertRaises(ValueError):a.directory(io.BytesIO(raw),S)
 def test_central_malformed_caps(self):
  good=blob();pos=good.index(b'PK\x01\x02')
  for delta,fmt,val in [(0,'I',0),(6,'H',45),(8,'H',1),(28,'H',65535),(34,'H',1),(42,'I',4294967295)]:
   raw=bytearray(good);struct.pack_into('<'+fmt,raw,pos+delta,val)
   with self.assertRaises(ValueError):a.directory(io.BytesIO(raw),S)
  for k in S:
   caps=dict(S);caps[k]=0
   with self.assertRaises(ValueError):a.directory(io.BytesIO(good),caps)
 def test_duplicate(self):
  f=io.BytesIO()
  with zipfile.ZipFile(f,'w') as z:z.writestr('same',b'1');z.writestr('same',b'2')
  with self.assertRaises(ValueError):a.directory(io.BytesIO(f.getvalue()),S)
 def test_mutation_no_partial(self):
  with tempfile.TemporaryFile() as f:
   raw=blob();f.write(raw);f.flush();original=a.directory
   def mutate(f,sel):
    x=original(f,sel);f.seek(0);f.write(b'x');f.flush();return x
   with patch('admit.directory',side_effect=mutate):h,x=a.inspect(f,pin(raw),S)
   self.assertNotIn('entries',x);self.assertFalse(x['partial_inventory_exposed'])
 def test_transport(self):
  class Resp:
   status=200
   def __init__(self,length,data):self.headers={} if length is None else {'Content-Length':length};self.data=io.BytesIO(data)
   def __enter__(self):return self
   def __exit__(self,*args):pass
   def geturl(self):return 'https://x'
   def read(self,n):return self.data.read(n)
  class Opener:
   def __init__(self,r):self.r=r
   def open(self,*args,**kwargs):return self.r
  with tempfile.TemporaryDirectory() as d:
   for i,(length,data,limit) in enumerate([(None,b'abc',3),('2',b'abc',3),('3',b'ab',3),('3',b'abcd',3)]):
    with self.assertRaises(ValueError):a.download('https://x',Path(d)/str(i),limit,3,Opener(Resp(length,data)))
   a.download('https://x',Path(d)/'pass',3,3,Opener(Resp('3',b'abc')))
  self.assertIsNone(a.NoRedirect().redirect_request(None,None,None,None,None,None))
if __name__=='__main__':unittest.main()
