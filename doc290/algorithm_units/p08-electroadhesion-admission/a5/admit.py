"""A5 exact Git source identity and literal evidence inventory; no scoring."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
def sha(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def strict(raw):
 def pairs(items):
  d={}
  for k,v in items:
   if k in d:raise ValueError('duplicate key')
   d[k]=v
  return d
 def constant(x):raise ValueError('nonstandard constant')
 return json.loads(raw.decode('utf-8','strict'),object_pairs_hook=pairs,parse_constant=constant)
def lines(raw):
 text=raw.decode('utf-8','strict');rs=[];start=0;byte=0
 for m in re.finditer(r'\r\n|\r|\n',text):
  body=text[start:m.start()];term=m.group();rs.append({'line_ordinal_1based':len(rs)+1,'byte_offset_0based':byte,'text':body,'terminator':{'\r\n':'CRLF','\r':'CR','\n':'LF'}[term]});byte+=len((body+term).encode());start=m.end()
 if start<len(text):rs.append({'line_ordinal_1based':len(rs)+1,'byte_offset_0based':byte,'text':text[start:],'terminator':'NONE'})
 return rs
def gate(raws,s):
 if len(raws)!=5 or len(s['files'])!=5:raise ValueError('all5')
 total=0
 for raw,f in zip(raws,s['files']):
  total+=len(raw)
  if len(raw)>s['max_file_bytes'] or total>s['max_total_bytes'] or len(raw)!=f['bytes'] or sha(raw)!=f['sha256'] or blob(raw)!=f['git_blob_sha1']:raise ValueError('identity/caps')
def consistency(summary,hashes):
 ms=summary['members']
 if type(summary['total_lines']) is not int or len(ms)!=45 or len(hashes)!=47 or summary['status']!='all_selected_raw_literal_text_inventories':raise ValueError('metadata counts/types')
 if [m['ordinal_1based'] for m in ms]!=list(range(628,673)):raise ValueError('ordinal coverage')
 if any(type(m[k]) is not int for m in ms for k in ('ordinal_1based','raw_bytes','line_count')):raise ValueError('boolean/type')
 if sum(m['line_count'] for m in ms)!=summary['total_lines'] or sum(m['raw_bytes'] for m in ms)!=389460137:raise ValueError('aggregate')
 expected={'summary.json','manifest.json'}|{m['inventory_filename'] for m in ms}
 if set(hashes)!=expected:raise ValueError('47 output coverage')
 for m in ms:
  if hashes[m['inventory_filename']]['sha256']!=m['inventory_sha256'] or type(hashes[m['inventory_filename']]['bytes']) is not int:raise ValueError('hash correlation')
 for h in hashes.values():
  if not re.fullmatch('[0-9a-f]{64}',h['sha256']) or type(h['bytes']) is not int or h['bytes']<0:raise ValueError('hash structure')
def inspect(raws,s):
 try:
  gate(raws,s);js={f['path']:strict(r) for f,r in zip(s['files'],raws) if f['path'].endswith('.json')}
  consistency(next(v for k,v in js.items() if k.endswith('/summary.json')),next(v for k,v in js.items() if k.endswith('/full-output-hashes.json')))
  return {'status':'all5_identity_literal_inventory','files':{f['path']:lines(r) for f,r in zip(s['files'],raws)},'metadata':'structural consistency only, NOT measurements/units/trial proof'}
 except Exception as ex:return {'status':'unavailable_or_unresolved','error':type(ex).__name__+': '+str(ex),'partial_inventory_exposed':False}
def run(folder):
 here=Path(__file__).parent
 for l in (here/'freeze-hashes.sha256').read_text().splitlines():
  h,n=l.split('  ',1)
  if sha((here/n).read_bytes())!=h:raise ValueError('freeze '+n)
 if strict((here/'environment.json').read_bytes())!={'python':sys.version,'python_bytes':sha(Path(sys.executable).read_bytes())}:raise ValueError('environment')
 s=strict((here/'selection.json').read_bytes());repo=subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=here,text=True).strip();raws=[]
 for f in s['files']:
  # local Git exact object, check metadata size BEFORE read.
  if subprocess.check_output(['git','rev-parse',s['source_commit']+':'+f['path']],cwd=repo,text=True).strip()!=f['git_blob_sha1']:raise ValueError('commit path binding')
  n=int(subprocess.check_output(['git','cat-file','-s',f['git_blob_sha1']],cwd=repo,text=True))
  if n!=f['bytes'] or n>s['max_file_bytes']:raise ValueError('pre-read caps')
  raws.append(subprocess.check_output(['git','cat-file','blob',f['git_blob_sha1']],cwd=repo))
 result=inspect(raws,s);out=Path(folder);out.mkdir(exist_ok=False)
 for name,x in [('inventory.json',result),('manifest.json',{'code_sha256':sha((here/'admit.py').read_bytes()),'selection_sha256':sha((here/'selection.json').read_bytes()),'source_commit':s['source_commit']})]:out.joinpath(name).write_text(json.dumps(x,indent=2,ensure_ascii=True,allow_nan=False)+'\n')
if __name__=='__main__':run(sys.argv[1])
