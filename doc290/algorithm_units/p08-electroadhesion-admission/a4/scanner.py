"""A2 archive identity and bounded directory only; never read members."""
import hashlib,json,os,re,stat,struct,sys,time,urllib.request,zipfile
from pathlib import Path
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):return None
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=True,allow_nan=False)+'\n')
def hashfile(f):
 f.seek(0);md=hashlib.md5();sh=hashlib.sha256();size=0
 while True:
  b=f.read(65536)
  if not b:break
  size+=len(b);md.update(b);sh.update(b)
 return {'bytes':size,'md5':md.hexdigest(),'sha256':sh.hexdigest()}
def verify(f,s):
 h=hashfile(f)
 if h['bytes']!=s['metadata_size'] or h['md5']!=s['metadata_md5']:raise ValueError('original size/MD5 identity')
 return h
def download(url,path,limit,expected,opener=None):
 opener=opener or urllib.request.build_opener(NoRedirect());start=time.monotonic();size=0
 req=urllib.request.Request(url,headers={'Accept-Encoding':'identity','User-Agent':'source-admission/3'})
 with opener.open(req,timeout=20) as r,path.open('xb') as out:
  if r.status!=200 or r.geturl()!=url or r.headers.get('Content-Encoding','identity').lower()!='identity':raise ValueError('transport route/status/encoding')
  length=r.headers.get('Content-Length')
  if length is None or not length.isdigit() or int(length)!=expected or expected>limit:raise ValueError('required exact declared length/cap')
  while True:
   if time.monotonic()-start>1200:raise ValueError('between-read deadline')
   b=r.read(min(65536,limit-size+1))
   if not b:break
   size+=len(b)
   if size>limit:raise ValueError('stream cap')
   out.write(b)
  out.flush();os.fsync(out.fileno())
  if size!=expected:raise ValueError('EOF size mismatch')
def extras(raw):
 pos=0
 while pos<len(raw):
  if pos+4>len(raw):raise ValueError('malformed extra header')
  typ,n=struct.unpack_from('<HH',raw,pos);pos+=4
  if pos+n>len(raw) or typ==1:raise ValueError('malformed/ZIP64 extra')
  pos+=n
def unsafe(name,flag,creator,attr):
 if '\x00' in name or flag&1 or flag&64:raise ValueError('NUL/encrypted entry')
 normalized=name.replace('\\','/')
 if normalized.startswith('/') or re.match('^[A-Za-z]:',normalized) or '..' in normalized.split('/'):raise ValueError('unsafe absolute/drive/traversal name')
 if creator>>8==3 and stat.S_ISLNK(attr>>16):raise ValueError('symlink entry')
def directory(f,sel):
 f.seek(0,2);size=f.tell();f.seek(max(0,size-65557));tail=f.read(65557);start=size-len(tail);candidates=[]
 for i in range(len(tail)-21):
  if tail[i:i+4]==b'PK\x05\x06':
   fields=struct.unpack_from('<4s4H2IH',tail,i)
   if i+22+fields[-1]==len(tail):candidates.append((start+i,fields))
 if len(candidates)!=1:raise ValueError('missing/conflicting exact EOF EOCD')
 offset,(_,disk,cdisk,n_disk,n,cdsize,cdoffset,clen)=candidates[0]
 if disk or cdisk or n_disk!=n:raise ValueError('multipart/count mismatch')
 if n in (65535,) or cdsize==4294967295 or cdoffset==4294967295:raise ValueError('ZIP64 sentinel')
 if offset>=20:
  f.seek(offset-20)
  if f.read(4)==b'PK\x06\x07':raise ValueError('ZIP64 locator')
 if n>sel['max_entries'] or cdsize>sel['max_central_directory_bytes'] or cdoffset+cdsize!=offset or cdoffset>size:raise ValueError('directory caps/range/end alignment')
 f.seek(cdoffset);cd=f.read(cdsize)
 if len(cd)!=cdsize:raise ValueError('truncated central directory')
 pos=0;records=[]
 while pos<len(cd):
  if len(records)>=n or pos+46>len(cd):raise ValueError('central count/header bounds')
  v=struct.unpack_from('<4s6H3I5H2I',cd,pos)
  sig,creator,need,flag,comp,tm,dt,crc,csize,usize,nlen,elen,mlen,dstart,iattr,eattr,hoff=v
  if sig!=b'PK\x01\x02' or dstart or need>=45 or 4294967295 in (csize,usize,hoff):raise ValueError('central malformed/ZIP64/multipart')
  end=pos+46+nlen+elen+mlen
  if end>len(cd) or hoff>=cdoffset:raise ValueError('central record/name/local range')
  namebytes=cd[pos+46:pos+46+nlen];extra=cd[pos+46+nlen:pos+46+nlen+elen];comment=cd[pos+46+nlen+elen:end]
  name=namebytes.decode('utf-8' if flag&2048 else 'cp437',errors='strict');extras(extra);unsafe(name,flag,creator,eattr)
  if len(name)>sel['max_member_name_characters']:raise ValueError('member name cap')
  records.append({'filename':name,'raw_filename_hex':namebytes.hex(),'flags':flag,'compression':comp,'crc':crc,'compressed_size':csize,'uncompressed_size':usize,'header_offset':hoff,'create_version':creator,'external_attr':eattr,'extra_hex':extra.hex(),'comment_hex':comment.hex()});pos=end
 if len(records)!=n or pos!=cdsize:raise ValueError('central actual count/bytes mismatch')
 if len({r['filename'] for r in records})!=len(records):raise ValueError('duplicate name')
 # Allocation now bounded by fully scanned central bytes and entry count, not EOCD alone.
 with zipfile.ZipFile(f,'r') as z:
  infos=z.infolist()
  if len(infos)!=n or z.start_dir!=cdoffset:raise ValueError('ZipFile count/start mismatch')
  for ordinal,(a,b) in enumerate(zip(records,infos),1):
   for key,other in [('filename',b.filename),('flags',b.flag_bits),('compression',b.compress_type),('crc',b.CRC),('compressed_size',b.compress_size),('uncompressed_size',b.file_size),('header_offset',b.header_offset),('external_attr',b.external_attr),('extra_hex',b.extra.hex()),('comment_hex',b.comment.hex())]:
    if a[key]!=other:raise ValueError('parser disagreement '+key)
   if a['create_version']!=b.create_system*256+b.create_version:raise ValueError('creator disagreement')
   a.update(ordinal_1based=ordinal,filename_repr=repr(a['filename']),datetime=list(b.date_time))
 return {'status':'complete_bounded_directory_metadata','entries':records,'entry_count':n,'central_directory_bytes':cdsize,'central_directory_offset':cdoffset,'EOCD_offset':offset,'comment_hex':tail[-clen:].hex() if clen else '', 'claims':'directory metadata only; no member CRC/content/extraction validation'}
def inspect(f,s,sel):
 identity=verify(f,s);state=os.fstat(f.fileno())
 try:
  inv=directory(f,sel)
  if hashfile(f)!=identity or os.fstat(f.fileno())!=state:raise ValueError('archive mutated during parse')
  return identity,inv
 except Exception as ex:
  return identity,{'status':'unresolved_directory_unsafe_or_cap','error':type(ex).__name__+': '+str(ex),'partial_inventory_exposed':False}
def pins():return {'python':sys.version,'python_executable_sha256':sha(Path(sys.executable).read_bytes()),'zipfile_path':zipfile.__file__,'zipfile_sha256':sha(Path(zipfile.__file__).read_bytes())}
def run(folder,retained=None):
 here=Path(__file__).parent
 for line in (here/'freeze-hashes.sha256').read_text().splitlines():
  h,n=line.split('  ',1)
  if sha((here/n).read_bytes())!=h:raise ValueError('freeze '+n)
 env=json.loads((here/'environment.json').read_text())
 if pins()!=env:raise ValueError('environment bytes changed')
 sel=json.loads((here/'selection.json').read_text());s=sel['files'][0]
 if len(sel['files'])!=1 or sha((here/'record-metadata.json').read_bytes())!=sel['metadata_sha256']:raise ValueError('selection')
 out=Path(folder);out.mkdir(exist_ok=False);record={**s,'status':'unavailable'};inv={'analysis_performed':False,'outcome':'scoped unavailable identity required'}
 archive=Path(retained) if retained else out/'Data.zip'
 try:
  if retained is None:download(s['url'],archive,sel['max_archive_bytes'],s['metadata_size'])
  with archive.open('rb') as f:
   identity,inv=inspect(f,s,sel);record.update(identity,status='verified')
 except Exception as ex:record['error']=type(ex).__name__+': '+str(ex)
 dump(out/'inputs.json',record);dump(out/'inventory.json',inv)
 dump(out/'manifest.json',{'environment':env,'outputs':{p.name:sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file() and p.name!='Data.zip'}})
if __name__=='__main__':run(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None)
