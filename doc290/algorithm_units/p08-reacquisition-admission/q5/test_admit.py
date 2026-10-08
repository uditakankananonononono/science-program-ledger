import copy,hashlib,io,json,struct,tempfile,unittest,unittest.mock as mock,zipfile
from pathlib import Path
import admit as a
import scanner as s
SEL={'max_archive_bytes':671088640,'max_central_directory_bytes':16777216,'max_entries':100000,'max_member_name_characters':4096}
def fixture():
    f=io.BytesIO()
    with zipfile.ZipFile(f,'w') as z:
        zi=zipfile.ZipInfo('folder/Raw Data.csv',(2024,1,2,3,4,6));zi.comment=b'comment';zi.extra=b'\x02\x00\x01\x00x';zi.internal_attr=1
        z.writestr(zi,b'opaque fixture');z.writestr('folder/image.txt',b'opaque2')
    return f.getvalue()
class Tests(unittest.TestCase):
    def test_correspondence(self):
        raw=fixture();inv=s.directory(io.BytesIO(raw),SEL)
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            for i,(r,b) in enumerate(zip(inv['entries'],z.infolist()),1):
                for k,v in {'ordinal_1based':i,'filename':b.filename,'flags':b.flag_bits,'compression':b.compress_type,'crc':b.CRC,'compressed_size':b.compress_size,'uncompressed_size':b.file_size,'header_offset':b.header_offset,'create_version':b.create_system*256+b.create_version,'required_version':b.extract_version,'internal_attr':b.internal_attr,'external_attr':b.external_attr,'extra_hex':b.extra.hex(),'comment_hex':b.comment.hex(),'datetime':list(b.date_time)}.items():self.assertEqual(r[k],v)
                self.assertEqual(r['dos_time'],(b.date_time[3]<<11)|(b.date_time[4]<<5)|(b.date_time[5]//2));self.assertEqual(r['dos_date'],((b.date_time[0]-1980)<<9)|(b.date_time[1]<<5)|b.date_time[2])
                self.assertEqual(r['raw_filename_hex'],b.filename.encode().hex());self.assertEqual(r['disk_start'],0)
    def test_no_member_routes(self):
        raw=fixture()
        with mock.patch.object(zipfile.ZipFile,'open',side_effect=AssertionError('member')),mock.patch.object(zipfile.ZipFile,'extract',side_effect=AssertionError('extract')),mock.patch.object(zipfile.ZipFile,'testzip',side_effect=AssertionError('testzip')):s.directory(io.BytesIO(raw),SEL)
    def test_caps(self):
        for key,val in [('max_central_directory_bytes',1),('max_entries',1),('max_member_name_characters',1)]:
            sel=copy.deepcopy(SEL);sel[key]=val
            with self.assertRaises(ValueError):s.directory(io.BytesIO(fixture()),sel)
        for off,val in [(28,16385),(30,4097),(32,4097)]:
            raw=bytearray(fixture());p=raw.index(b'PK\x01\x02');struct.pack_into('<H',raw,p+off,val)
            with self.assertRaises(ValueError):s.directory(io.BytesIO(raw),SEL)
    def test_offset_overlap_outside(self):
        raw=fixture();positions=[];start=0
        while True:
            p=raw.find(b'PK\x01\x02',start)
            if p<0:break
            positions.append(p);start=p+4
        for offset in [0,len(raw)-1]:
            b=bytearray(raw);struct.pack_into('<I',b,positions[1]+42,offset)
            with self.assertRaises(ValueError):s.directory(io.BytesIO(b),SEL)
    def test_identity_and_mutation(self):
        with tempfile.TemporaryDirectory() as d:
            src=Path(d)/'source';src.write_bytes(fixture());sel={**SEL,'bytes':src.stat().st_size,'sha256':a.sha(src)}
            with mock.patch.object(s,'directory',side_effect=AssertionError('parser')) as spy:
                bad={**sel,'sha256':'wrong'}
                with self.assertRaises(ValueError):a.run(src,Path(d)/'out',bad)
                spy.assert_not_called()
            original=s.directory
            def mutate(f,x):
                inv=original(f,x)
                with src.open('r+b') as w:w.seek(0);w.write(b'XX')
                return inv
            with mock.patch.object(s,'directory',side_effect=mutate):
                with self.assertRaises(ValueError):a.run(src,Path(d)/'out',sel)
            self.assertFalse((Path(d)/'out').exists());self.assertEqual([p.name for p in Path(d).iterdir()],['source'])
    def test_unsafe(self):
        for name in ['../bad','/bad']:
            f=io.BytesIO()
            with zipfile.ZipFile(f,'w') as z:z.writestr(name,b'x')
            with self.assertRaises(ValueError):s.directory(io.BytesIO(f.getvalue()),SEL)
    def test_record_disagreement(self):
        original=zipfile.ZipFile.infolist
        def wrong(z):
            infos=original(z);infos[0].internal_attr=3;return infos
        with mock.patch.object(zipfile.ZipFile,'infolist',wrong):
            with self.assertRaises(ValueError):s.directory(io.BytesIO(fixture()),SEL)
if __name__=='__main__':unittest.main()

class Additional(unittest.TestCase):
    def test_aggregate_cap(self):
        f=io.BytesIO()
        with zipfile.ZipFile(f,'w') as z:
            for i in range(140):
                zi=zipfile.ZipInfo(str(i)+'x'*4000);zi.comment=b'c'*4000;z.writestr(zi,b'x')
        with self.assertRaises(ValueError):s.directory(io.BytesIO(f.getvalue()),SEL)
    def test_zip64_multipart_duplicates_encryption(self):
        raw=fixture();e=raw.rindex(b'PK\x05\x06');c=raw.index(b'PK\x01\x02')
        for target,offset,fmt,val in [(e,4,'H',1),(e,10,'H',65535),(c,8,'H',1),(c,20,'I',4294967295)]:
            b=bytearray(raw);struct.pack_into('<'+fmt,b,target+offset,val)
            with self.assertRaises(ValueError):s.directory(io.BytesIO(b),SEL)
        f=io.BytesIO()
        with zipfile.ZipFile(f,'w') as z:z.writestr('same',b'x');z.writestr('same',b'x')
        with self.assertRaises(ValueError):s.directory(io.BytesIO(f.getvalue()),SEL)
