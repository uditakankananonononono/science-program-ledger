import io,struct,tempfile,unittest,unittest.mock as mock,zlib
from pathlib import Path
import admit as a
class Tests(unittest.TestCase):
 def fixture(self,descriptor=True,signed=True):
  body=b'a,b\r\n1,2\r\n';crc=zlib.crc32(body);name=b'd.csv';flags=8 if descriptor else 0
  head=struct.pack('<4s5H3I2H',b'PK\x03\x04',20,flags,0,0,33,0 if descriptor else crc,0 if descriptor else len(body),0 if descriptor else len(body),len(name),0)
  tail=(b'PK\x07\x08' if signed else b'')+struct.pack('<III',crc,len(body),len(body)) if descriptor else b''
  rec={'header_offset':0,'required_version':20,'flags':flags,'compression':0,'dos_time':0,'dos_date':33,'crc':crc,'compressed_size':len(body),'uncompressed_size':len(body),'raw_filename_hex':name.hex()}
  return head+name+body+tail,rec
 def test_bit3_signed_unsigned_nonbit3(self):
  for descriptor,signed in [(True,True),(True,False),(False,False)]:
   raw,r=self.fixture(descriptor,signed);f=io.BytesIO(raw);loc=a.local(f,r,len(raw));self.assertEqual(loc['descriptor_bytes'],(16 if signed else 12) if descriptor else 0)
   with tempfile.TemporaryDirectory() as d:self.assertEqual(a.acquire_member(f,r,loc,Path(d)/'member')['bytes'],r['uncompressed_size'])
 def test_header_descriptor_body_bounds(self):
  raw,r=self.fixture()
  for offset in [4,6,8,14,len(raw)-1]:
   b=bytearray(raw);b[offset]^=1
   with self.assertRaises(ValueError):a.local(io.BytesIO(b),r,len(b))
  with self.assertRaises(ValueError):a.local(io.BytesIO(raw),r,len(raw)-1)
 def test_crc_before_decode(self):
  raw,r=self.fixture();f=io.BytesIO(raw);loc=a.local(f,r,len(raw));bad=bytearray(raw);bad[loc['start']]^=1
  with tempfile.TemporaryDirectory() as d,mock.patch.object(a,'text',side_effect=AssertionError('decoder')) as spy:
   with self.assertRaises(ValueError):a.acquire_member(io.BytesIO(bad),r,loc,Path(d)/'out')
   spy.assert_not_called()
 def test_literal_csv(self):
  x=a.text(b'\xef\xbb\xbfA,"B,C"\r\n1,2\n\n');self.assertTrue(x['bom']);self.assertEqual(x['records'][0],['\ufeffA','B,C']);self.assertEqual(x['crlf'],1);self.assertTrue(x['final_newline'])
  for raw in [b'\xff',b'"unclosed',b'a'*16385,(','.join(['x']*65)).encode()]:
   with self.assertRaises((ValueError,UnicodeError,a.csv.Error)):a.text(raw)


class Additional(unittest.TestCase):
 def test_identity_zero_analysis(self):
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'source';src.write_bytes(b'opaque')
   with mock.patch.object(a.scanner,'directory',side_effect=AssertionError('parser')) as spy:
    with self.assertRaises(ValueError):a.run(src,Path(d)/'out',{'archive_bytes':6,'archive_sha256':'bad'})
    spy.assert_not_called()
   self.assertEqual([p.name for p in Path(d).iterdir()],['source'])
 def test_local_name_flags_crc_placeholders(self):
  raw,r=Tests().fixture()
  for offset in [30,14,18,22]:
   b=bytearray(raw);b[offset]^=1
   with self.assertRaises(ValueError):a.local(io.BytesIO(b),r,len(b))
  b=bytearray(raw)
  for offset,value in [(14,r['crc']),(18,r['compressed_size']),(22,r['uncompressed_size'])]:struct.pack_into('<I',b,offset,value)
  a.local(io.BytesIO(b),r,len(b))
 def test_no_zip_extract_execute(self):
  import zipfile,subprocess
  raw,r=Tests().fixture()
  with mock.patch.object(zipfile.ZipFile,'open',side_effect=AssertionError('unselected')),mock.patch.object(zipfile.ZipFile,'extract',side_effect=AssertionError('extract')),mock.patch.object(subprocess,'run',side_effect=AssertionError('exec')):
   a.local(io.BytesIO(raw),r,len(raw))
 def test_literal_unicode_separator(self):
  x=a.text('a\u2028b,c\r\n'.encode());self.assertEqual(len(x['literal_lines']),2)
if __name__=='__main__':unittest.main()
