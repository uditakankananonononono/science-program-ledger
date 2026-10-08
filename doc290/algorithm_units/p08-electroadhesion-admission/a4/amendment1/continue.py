"""A4-1 bounded member checkpoint continuation, imports original freeze unchanged."""
import gzip,hashlib,hmac,json,os,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import admit as old,scanner
TYPE='A4-1-checkpoint-v1'
def codepins():
 here=Path(__file__).parent
 return {str(p.relative_to(here.parent)):scanner.sha(p.read_bytes()) for p in [here/'continue.py',here.parent/'admit.py',here.parent/'scanner.py',here.parent/'selection.json',here.parent/'freeze-hashes.sha256',here.parent/'environment.json']}
def validate_archive(archive,sel,caps):
 with Path(archive).open('rb') as f:
  old.identity(f,sel);state=os.fstat(f.fileno());inv=scanner.directory(f,caps);rule=sel['selection_rule']
  matches=[e for e in inv['entries'] if e['filename'].startswith(rule['exact_prefix']) and e['filename'].endswith(rule['exact_suffix'])]
  if matches!=sel['files'] or len(matches)!=sel['max_members']:raise ValueError('recomputed central selection')
  old.identity(f,sel)
  if state!=os.fstat(f.fileno()):raise ValueError('archive mutated')
def seal(payload,key):return hmac.new(key,json.dumps(payload,sort_keys=True,separators=(',',':')).encode(),hashlib.sha256).hexdigest()
def load(stage,keypath):
 doc=json.loads((stage/'state.json').read_text());payload=doc['payload'];key=keypath.read_bytes()
 if not hmac.compare_digest(doc['seal'],seal(payload,key)) or payload['type']!=TYPE:raise ValueError('checkpoint state type/seal')
 expected={'state.json'}|{r['inventory_filename'] for r in payload['members']}
 if {p.name for p in stage.iterdir()}!=expected:raise ValueError('unmanifested/temp/foreign stage files')
 if payload['pins']!=codepins():raise ValueError('checkpoint code/selection changed')
 if len({r['ordinal_1based'] for r in payload['members']})!=len(payload['members']):raise ValueError('duplicate ordinal')
 return payload,key
def save(stage,payload,key):
 tmp=stage/'state.tmp';scanner.dump(tmp,{'payload':payload,'seal':seal(payload,key)});tmp.replace(stage/'state.json')
def rawrecords(rawdir,sel):
 # Recompute each discovery from held raw set, tie hashes to original acquire inputs.
 inputs=json.loads((rawdir.parent/'inputs.json').read_text());expected=sel['files']
 if len(inputs)!=len(expected):raise ValueError('raw input coverage')
 rs=[]
 for e,r in zip(expected,inputs):
  if r['ordinal_1based']!=e['ordinal_1based'] or r['filename']!=e['filename'] or r['scratch_filename']!='member-'+str(e['ordinal_1based'])+'.raw' or r['raw_bytes']!=e['uncompressed_size']:raise ValueError('raw input metadata')
  with (rawdir/r['scratch_filename']).open('rb') as f:h=scanner.hashfile(f)
  if h['bytes']!=r['raw_bytes'] or h['sha256']!=r['raw_sha256_discovered']:raise ValueError('raw discovery identity')
  rs.append(r)
 if sum(r['raw_bytes'] for r in rs)>sel['max_total_decompressed_bytes'] or any(r['raw_bytes']>sel['max_member_bytes'] for r in rs):raise ValueError('raw caps')
 return rs
def replay(rawpath,sel,output):
 n=0
 with output.open('xb') as f,gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as gz:
  for line in old.line_records(rawpath,sel):
   n+=1
   if n>sel['max_total_lines']:raise ValueError('line cap')
   gz.write((json.dumps(line,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode())
 return n,old.file_sha(output)
def run(stage,rawdir,archive,keypath,mode,destination=None):
 stage=Path(stage);rawdir=Path(rawdir);keypath=Path(keypath);here=Path(__file__).parent.parent
 # Original freeze+actual environment gates every invocation.
 for l in (here/'freeze-hashes.sha256').read_text().splitlines():
  h,n=l.split('  ',1)
  if scanner.sha((here/n).read_bytes())!=h:raise ValueError('original freeze')
 if old.pins()!=json.loads((here/'environment.json').read_text()):raise ValueError('environment')
 sel=json.loads((here/'selection.json').read_text());caps=json.loads((here/'directory-caps.json').read_text());validate_archive(archive,sel,caps);rs=rawrecords(rawdir,sel)
 if mode=='init':
  if stage.exists() or keypath.exists():raise ValueError('fresh stage/key required')
  stage.mkdir();keypath.write_bytes(os.urandom(32));keypath.chmod(0o600);key=keypath.read_bytes()
  save(stage,{'type':TYPE,'pins':codepins(),'raw_records':rs,'members':[]},key);return {'status':'initialized_only','new_analysis':False}
 payload,key=load(stage,keypath)
 if payload['raw_records']!=rs:raise ValueError('raw receipt changed')
 valid={r['ordinal_1based']:r for r in rs}
 for c in payload['members']:
  if c['ordinal_1based'] not in valid or any(c[k]!=valid[c['ordinal_1based']][k] for k in valid[c['ordinal_1based']]):raise ValueError('foreign/mismatched checkpoint')
  if old.file_sha(stage/c['inventory_filename'])!=c['inventory_sha256']:raise ValueError('checkpoint gzip altered after replay receipt')
 if sum(c['line_count'] for c in payload['members'])>sel['max_total_lines']:raise ValueError('replay-receipted total line cap')
 if mode=='batch':
  done={c['ordinal_1based'] for c in payload['members']};todo=[r for r in rs if r['ordinal_1based'] not in done][:3]
  # Each newly made inventory is literal replay output; verify independent second replay <=3 members total.
  for r in todo:
   name='member-'+str(r['ordinal_1based'])+'.jsonl.gz';path=stage/name
   with tempfile.TemporaryDirectory(prefix='a4-1-replay-') as td:
    tmp=Path(td)/'canonical.gz';n,h=replay(rawdir/r['scratch_filename'],sel,tmp)
    second=Path(td)/'verify.gz';n2,h2=replay(rawdir/r['scratch_filename'],sel,second)
    if (n,h)!=(n2,h2):raise ValueError('literal replay mismatch')
    with (rawdir/r['scratch_filename']).open('rb') as f:rh=scanner.hashfile(f)
    if rh['sha256']!=r['raw_sha256_discovered'] or rh['bytes']!=r['raw_bytes']:raise ValueError('raw changed during replay')
    c={**r,'inventory_filename':name,'line_count':n,'inventory_sha256':h}
    if sum(x['line_count'] for x in payload['members'])+n>sel['max_total_lines']:raise ValueError('aggregate line cap')
    # A crash before signed state update leaves unmanifested file rejected on next call.
    tmp.replace(path);payload['members'].append(c);save(stage,payload,key)
  return {'status':'checkpoint_only_NOT_success','completed_members':len(payload['members']),'members_processed_this_call':len(todo)}
 if mode!='final':raise ValueError('mode')
 if [c['ordinal_1based'] for c in payload['members']]!=[r['ordinal_1based'] for r in rs]:raise ValueError('complete all45 ordinal coverage')
 # Signature binds computed replay counts and exact hashes; final fresh raw/archive/gzip checks above.
 destination=Path(destination)
 if destination.exists():raise ValueError('success destination exists')
 complete=Path(tempfile.mkdtemp(prefix='.a4-1-final-',dir=destination.parent))
 import shutil
 for c in payload['members']:shutil.copyfile(stage/c['inventory_filename'],complete/c['inventory_filename'])
 scanner.dump(complete/'summary.json',{'status':'all_selected_raw_literal_text_inventories','members':payload['members'],'total_lines':sum(c['line_count'] for c in payload['members']),'grammar':'CRLF/CR/LF only; 0based raw byte offsets; body excludes terminator, full span body+terminator; 1based lines; no fictitious trailing empty after delimiter, empty raw zero lines, VT/FF/NEL/Unicode separators literal'})
 scanner.dump(complete/'manifest.json',{'outputs':{p.name:old.file_sha(p) for p in sorted(complete.iterdir()) if p.is_file()}})
 for c in payload['members']:
  if old.file_sha(complete/c['inventory_filename'])!=c['inventory_sha256']:raise ValueError('final copied gzip mismatch')
 complete.rename(destination);return {'status':'success_all45_inventory','total_lines':sum(c['line_count'] for c in payload['members'])}
if __name__=='__main__':
 print(json.dumps(run(*sys.argv[1:]),indent=2))
