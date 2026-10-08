"""Q6 selected stored-member identities before any UTF8/CSV analysis."""
import csv,hashlib,io,json,os,re,shutil,struct,sys,tempfile,zlib
from pathlib import Path
import scanner
HERE=Path(__file__).resolve().parent
CAPS={'max_central_directory_bytes':16777216,'max_entries':100000,'max_member_name_characters':4096}
def hashf(f):
 f.seek(0);h=hashlib.sha256();n=0
 while True:
  b=f.read(65536)
  if not b:break
  n+=len(b);h.update(b)
 return n,h.hexdigest()
def sha(p):
 with Path(p).open('rb') as f:return hashf(f)[1]
def pins():
 import zipfile,_csv,_hashlib
 ms=[csv,hashlib,io,json,os,re,shutil,struct,tempfile,zlib,zipfile,_csv,_hashlib]
 return {'python':sys.version,'executable_sha256':sha(sys.executable),'modules':{m.__name__:({'path':m.__file__,'sha256':sha(m.__file__)} if getattr(m,'__file__',None) else {'builtin':m.__spec__.origin,'executable_covered':True}) for m in ms}}
def local(f,rec,bound):
 off=rec['header_offset'];f.seek(off);b=f.read(30)
 if len(b)!=30:raise ValueError('short localheader')
 sig,ver,flags,method,tm,dt,crc,cs,us,nl,el=struct.unpack('<4s5H3I2H',b)
 if sig!=b'PK\x03\x04' or (ver,flags,method,tm,dt)!=(rec['required_version'],rec['flags'],rec['compression'],rec['dos_time'],rec['dos_date']) or method!=0:raise ValueError('local literal fields')
 if nl>16384 or el>4096 or off+30+nl+el>bound:raise ValueError('local variable bounds')
 name=f.read(nl);extra=f.read(el)
 if name.hex()!=rec['raw_filename_hex']:raise ValueError('local raw name')
 scanner.extras(extra)
 expected=(rec['crc'],rec['compressed_size'],rec['uncompressed_size'])
 if flags&8:
  if any(a not in (0,b) for a,b in zip((crc,cs,us),expected)):raise ValueError('bit3 permitted zero-or-exact fields')
 else:
  if (crc,cs,us)!=expected:raise ValueError('nonbit3 equality')
 start=off+30+nl+el;end=start+rec['compressed_size'];descriptor=0
 if end>bound:raise ValueError('body bounds')
 if flags&8:
  f.seek(end);first=f.read(4)
  if len(first)!=4:raise ValueError('descriptor truncated')
  if first==b'PK\x07\x08':
   if rec['crc']==0x08074b50:raise ValueError('descriptor signature/CRC ambiguity')
   if end+16>bound:raise ValueError('signed descriptor bounds')
   raw=f.read(12);descriptor=16
  else:
   if end+12>bound:raise ValueError('unsigned descriptor bounds')
   raw=first+f.read(8);descriptor=12
  if len(raw)!=12 or struct.unpack('<III',raw)!=expected:raise ValueError('descriptor central agreement')
 return {'start':start,'end':end,'descriptor_bytes':descriptor,'local_extra_bytes':el}
def acquire_member(f,rec,loc,path):
 f.seek(loc['start']);remaining=rec['uncompressed_size'];count=0;crc=0;h=hashlib.sha256()
 with path.open('xb') as out:
  while remaining:
   b=f.read(min(65536,remaining))
   if not b:raise ValueError('member truncated')
   if count+len(b)>rec['uncompressed_size']:raise ValueError('member cap')
   out.write(b);h.update(b);crc=zlib.crc32(b,crc);count+=len(b);remaining-=len(b)
 if f.tell()!=loc['end'] or count!=rec['uncompressed_size'] or crc&0xffffffff!=rec['crc']:raise ValueError('EOF/CRC')
 return {'bytes':count,'crc':crc&0xffffffff,'sha256':h.hexdigest()}
def text(raw):
 s=raw.decode('utf-8',errors='strict');lines=re.findall(r'[^\r\n]*(?:\r\n|\r|\n|$)',s)
 # Regex finalempty match retained exactly; Unicode separators are ordinary characters.
 if len(lines)>20000 or any(len(x)>16384 for x in lines):raise ValueError('line caps')
 csv.field_size_limit(16384);records=[]
 for row in csv.reader(io.StringIO(s,newline=''),delimiter=',',quotechar='"',doublequote=True,escapechar=None,strict=True):
  if len(row)>64 or len(records)>=20000 or any(len(v)>16384 for v in row):raise ValueError('CSV caps')
  records.append(row)
 return {'literal_lines':lines,'records':records,'bom':s.startswith('\ufeff'),'crlf':s.count('\r\n'),'cr_only':s.count('\r')-s.count('\r\n'),'lf_only':s.count('\n')-s.count('\r\n'),'final_newline':s.endswith(('\r','\n'))}
def bounded_json(path,x):
 total=0
 with path.open('xb') as f:
  for p in json.JSONEncoder(indent=2,ensure_ascii=True,sort_keys=True,allow_nan=False).iterencode(x):
   b=p.encode();total+=len(b)
   if total+1>16777216:raise ValueError('output cap')
   f.write(b)
  f.write(b'\n')
def run(source,dest,sel=None):
 sel=sel or json.loads((HERE/'selection.json').read_text());dest=Path(dest)
 if dest.exists() or dest.is_symlink():raise ValueError('destination exists')
 stage=Path(tempfile.mkdtemp(prefix='.q6-incomplete-',dir=dest.parent))
 try:
  with Path(source).open('rb') as f:
   state=os.fstat(f.fileno());expected=(sel['archive_bytes'],sel['archive_sha256'])
   if hashf(f)!=expected:raise ValueError('wholeidentity before parser')
   inv=scanner.directory(f,CAPS)
   serialized=(json.dumps(inv,indent=2,sort_keys=True,ensure_ascii=True,allow_nan=False)+'\n').encode()
   if hashlib.sha256(serialized).hexdigest()!=sel['inventory_sha256']:raise ValueError('whole directory binding')
   matches=[r for r in inv['entries'] if r['filename'].endswith('.csv')]
   if matches!=sel['members'] or len(matches)!=2:raise ValueError('ALL2selection')
   inputs=[]
   for i,rec in enumerate(matches):
    later=[e['header_offset'] for e in inv['entries'] if e['header_offset']>rec['header_offset']];bound=min(later+[inv['central_directory_offset']])
    loc=local(f,rec,bound);h=acquire_member(f,rec,loc,stage/f'private-member-{i}.bin');inputs.append({'name':rec['filename'],'ordinal':rec['ordinal_1based'],**h,'local':loc})
   # Both complete EOF/CRC/hash gates before first decoder.
   pages=[]
   for i,rec in enumerate(matches):pages.append(text((stage/f'private-member-{i}.bin').read_bytes()))
   if hashf(f)!=expected or os.fstat(f.fileno())!=state:raise ValueError('source mutation')
   bounded_json(stage/'private-literal-cells.json',pages)
   manifest={'status':'COMPLETE_ALL2_LITERAL_SCHEMA_PENDING_MANUAL_LEDGER','source_sha256':expected[1],'inputs':inputs,'files':[{'name':r['filename'],'literal_lines':len(x['literal_lines']),'logical_records':len(x['records']),'width_counts':{str(w):sum(len(row)==w for row in x['records']) for w in sorted({len(row) for row in x['records']})},'first_logical_record_strings':x['records'][0] if x['records'] else [],'bom':x['bom'],'crlf':x['crlf'],'cr_only':x['cr_only'],'lf_only':x['lf_only'],'final_newline':x['final_newline']} for r,x in zip(matches,pages)],'numeric_conversion':False,'endpoint_classification':False}
   bounded_json(stage/'manifest.json',manifest);os.rename(stage,dest);return manifest
 finally:
  if stage.exists():shutil.rmtree(stage)
def verify():
 for line in (HERE/'freeze-hashes.sha256').read_text().splitlines():
  h,p=line.split('  ',1)
  if sha(HERE/p)!=h:raise ValueError('freeze '+p)
 if pins()!=json.loads((HERE/'environment.json').read_text()):raise ValueError('environment')
if __name__=='__main__':verify();print(json.dumps(run(sys.argv[1],sys.argv[2]),indent=2))
