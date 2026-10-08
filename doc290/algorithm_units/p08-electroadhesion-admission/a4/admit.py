"""A4 fixed member raw text only, transactional success directory."""
import codecs,gzip,hashlib,json,os,sys,tempfile,zipfile
from pathlib import Path
import scanner as a
def identity(f,sel):
 h=a.hashfile(f)
 if h!={'bytes':sel['archive_bytes'],'md5':sel['archive_md5'],'sha256':sel['archive_sha256']}:raise ValueError('original identity')
 return h
def acquire(f,sel,caps,scratch):
 h=identity(f,sel);state=os.fstat(f.fileno());inv=a.directory(f,caps);rule=sel['selection_rule']
 matches=[e for e in inv['entries'] if e['filename'].startswith(rule['exact_prefix']) and e['filename'].endswith(rule['exact_suffix'])]
 if matches!=sel['files'] or len(matches)!=sel['max_members']:raise ValueError('complete selected metadata/ordinal agreement')
 total=0;records=[]
 with zipfile.ZipFile(f,'r') as z:
  infos=z.infolist()
  for selected in matches:
   info=infos[selected['ordinal_1based']-1]
   if info.filename!=selected['filename']:raise ValueError('ordinal')
   path=scratch/('member-'+str(selected['ordinal_1based'])+'.raw');size=0;sh=hashlib.sha256()
   with z.open(info,'r') as member,path.open('xb') as out:
    while True:
     chunk=member.read(min(65536,sel['max_member_bytes']-size+1,sel['max_total_decompressed_bytes']-total+1))
     if not chunk:break
     size+=len(chunk);total+=len(chunk)
     if size>sel['max_member_bytes'] or total>sel['max_total_decompressed_bytes']:raise ValueError('member/total stream cap')
     out.write(chunk);sh.update(chunk)
    out.flush();os.fsync(out.fileno())
   if size!=selected['uncompressed_size']:raise ValueError('exact EOF member size')
   records.append({'ordinal_1based':selected['ordinal_1based'],'filename':selected['filename'],'scratch_filename':path.name,'raw_bytes':size,'raw_sha256_discovered':sh.hexdigest()})
 if identity(f,sel)!=h or os.fstat(f.fileno())!=state:raise ValueError('original mutated')
 return records

def line_records(path,sel):
 # Incremental UTF8 validation independently of byte-line delimiter grammar.
 decoder=codecs.getincrementaldecoder('utf-8')('strict');buf=bytearray();start=0;ordinal=0
 def emit(body,term):
  nonlocal ordinal,start
  if len(body)>sel['max_line_bytes']:raise ValueError('line byte cap')
  ordinal+=1
  record={'line_ordinal_1based':ordinal,'byte_offset_0based':start,'body_byte_count':len(body),'terminator':{b'':'NONE',b'\r':'CR',b'\n':'LF',b'\r\n':'CRLF'}[term],'terminator_byte_count':len(term),'text':body.decode('utf-8','strict'),'literal_delimiter_counts':{k:body.count(v) for k,v in [('comma',b','),('semicolon',b';'),('tab',b'\t')]},'literal_quote_present':b'"' in body or b"'" in body}
  start+=len(body)+len(term);return record
 with path.open('rb') as f:
  while True:
   chunk=f.read(65536);final=not chunk;decoder.decode(chunk,final=final);buf.extend(chunk)
   pos=0;begin=0
   while pos<len(buf):
    ch=buf[pos]
    if ch in (10,13):
     if ch==13 and pos+1==len(buf) and not final:break
     n=2 if ch==13 and pos+1<len(buf) and buf[pos+1]==10 else 1
     yield emit(bytes(buf[begin:pos]),bytes(buf[pos:pos+n]));pos+=n;begin=pos
    else:pos+=1
    if pos-begin>sel['max_line_bytes']:raise ValueError('line byte cap')
   if begin:del buf[:begin]
   if final:
    if buf:yield emit(bytes(buf),b'')
    break

def file_sha(path):
 with path.open('rb') as f:return a.hashfile(f)['sha256']

def analyze_transaction(records,sel,scratch,destination):
 if destination.exists():raise ValueError('success destination exists')
 # ALL scratch hashes BEFORE ANY analysis.
 for r in records:
  with (scratch/r['scratch_filename']).open('rb') as f:h=a.hashfile(f)
  if h['bytes']!=r['raw_bytes'] or h['sha256']!=r['raw_sha256_discovered']:raise ValueError('scratch identity before analysis')
 # Hidden sibling stage, renamed once only after ALL inventory/manifest writes succeed.
 stage=Path(tempfile.mkdtemp(prefix='.a4-stage-',dir=destination.parent));total_lines=0;summary=[]
 for r in records:
  path=scratch/r['scratch_filename'];name='member-'+str(r['ordinal_1based'])+'.jsonl.gz';n=0
  with (stage/name).open('xb') as f,gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as gz:
   for line in line_records(path,sel):
    n+=1;total_lines+=1
    if total_lines>sel['max_total_lines']:raise ValueError('total line count cap')
    gz.write((json.dumps(line,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode())
  with path.open('rb') as f:h=a.hashfile(f)
  if h['bytes']!=r['raw_bytes'] or h['sha256']!=r['raw_sha256_discovered']:raise ValueError('scratch mutation during analysis')
  summary.append({**r,'inventory_filename':name,'line_count':n,'inventory_sha256':file_sha(stage/name)})
 a.dump(stage/'summary.json',{'status':'all_selected_raw_literal_text_inventories','members':summary,'total_lines':total_lines,'grammar':'CRLF/CR/LF only; 0based raw byte offsets; body excludes terminator, full span body+terminator; 1based lines; no fictitious trailing empty after delimiter, empty raw zero lines, VT/FF/NEL/Unicode separators literal'})
 a.dump(stage/'manifest.json',{'outputs':{p.name:file_sha(p) for p in sorted(stage.iterdir()) if p.is_file()}})
 stage.rename(destination)
 return summary

def pins():return {**a.pins(),'scanner_sha256':a.sha(Path(a.__file__).read_bytes())}
def run(folder,archive):
 here=Path(__file__).parent
 for l in (here/'freeze-hashes.sha256').read_text().splitlines():
  h,n=l.split('  ',1)
  if a.sha((here/n).read_bytes())!=h:raise ValueError('freeze '+n)
 if pins()!=json.loads((here/'environment.json').read_text()):raise ValueError('environment')
 sel=json.loads((here/'selection.json').read_text());caps=json.loads((here/'directory-caps.json').read_text());out=Path(folder);out.mkdir(exist_ok=False);scratch=out/'raw';scratch.mkdir()
 status={'status':'unavailable','analysis_performed':False,'partial_inventory_exposed':False}
 try:
  with Path(archive).open('rb') as f:records=acquire(f,sel,caps,scratch)
  # A failed transaction never has a success/inventory directory; raw retained intact.
  a.dump(out/'inputs.json',records)
  analyze_transaction(records,sel,scratch,out/'inventory');status={'status':'success_all_literal_inventories','analysis_performed':True,'partial_inventory_exposed':False}
 except Exception as ex:status['error']=type(ex).__name__+': '+str(ex)
 a.dump(out/'status.json',status)
if __name__=='__main__':run(sys.argv[1],sys.argv[2])
