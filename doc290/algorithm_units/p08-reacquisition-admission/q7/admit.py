"""Q7 all-four published literal evidence. Admission only; manual rule separately."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def oid(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def strict(b):
 def pairs(items):
  d={}
  for k,v in items:
   if k in d:raise ValueError('duplicate JSON key')
   d[k]=v
  return d
 def constant(x):raise ValueError('nonfinite JSON constant')
 return json.loads(b.decode('utf-8','strict'),object_pairs_hook=pairs,parse_constant=constant)
def schema(x):
 if type(x) is dict:return {'kind':'dict','fields':{k:schema(v) for k,v in x.items()}}
 if type(x) is list:return {'kind':'list','items':[schema(v) for v in x]}
 return {'kind':type(x).__name__}
def validate(x,s,path='$'):
 if s['kind']=='dict':
  if type(x) is not dict or set(x)!=set(s['fields']):raise ValueError('JSON object schema '+path)
  for k,v in x.items():validate(v,s['fields'][k],path+'.'+k)
 elif s['kind']=='list':
  if type(x) is not list or len(x)!=len(s['items']):raise ValueError('JSON list schema '+path)
  for i,(v,t) in enumerate(zip(x,s['items'])):validate(v,t,path+'['+str(i)+']')
 elif type(x).__name__!=s['kind']:raise ValueError('JSON exact type '+path)
def lines(b):
 t=b.decode('utf-8','strict');out=[];start=0;offset=0
 for m in re.finditer(r'\r\n|\r|\n',t):
  text=t[start:m.start()];term=m.group();out.append({'line':len(out)+1,'byte_offset':offset,'text':text,'terminator':{'\r\n':'CRLF','\r':'CR','\n':'LF'}[term]});offset+=len((text+term).encode());start=m.end()
 if start<len(t) or t.endswith(('\r','\n')) or not t:out.append({'line':len(out)+1,'byte_offset':offset,'text':t[start:],'terminator':'NONE','final_empty':start==len(t)})
 return out
def inspect(raws,sel,schemas):
 try:
  if len(raws)!=4 or len(sel['files'])!=4:raise ValueError('ALL4')
  total=0
  for b,r in zip(raws,sel['files']):
   total+=len(b)
   if len(b)>sel['max_file_bytes'] or total>sel['max_aggregate_bytes'] or len(b)!=r['bytes'] or sha(b)!=r['sha256'] or oid(b)!=r['git_blob_oid']:raise ValueError('all4 identity/caps')
  js={r['path']:strict(b) for b,r in zip(raws,sel['files']) if r['path'].endswith('.json')}
  if set(js)!=set(schemas):raise ValueError('JSON source coverage')
  for path,x in js.items():validate(x,schemas[path])
  return {'status':'ALL4_IDENTITY_LITERAL_SCHEMA_ADMITTED_PENDING_MANUAL_LEDGER','files':{r['path']:lines(b) for b,r in zip(raws,sel['files'])},'json_coordinates':js,'classification_performed':False}
 except Exception as ex:return {'status':'UNAVAILABLE_NO_PARTIAL_LEDGER','error':type(ex).__name__+': '+str(ex),'partial_inventory':False,'classification_performed':False}
def pins():
 ms=[hashlib,json,re,subprocess]
 return {'python':sys.version,'executable_sha256':sha(Path(sys.executable).read_bytes()),'modules':{m.__name__:sha(Path(m.__file__).read_bytes()) for m in ms}}
def run(dest):
 for line in (HERE/'freeze-hashes.sha256').read_text().splitlines():
  h,n=line.split('  ',1)
  if sha((HERE/n).read_bytes())!=h:raise ValueError('freeze '+n)
 if pins()!=strict((HERE/'environment.json').read_bytes()):raise ValueError('environment')
 sel=strict((HERE/'selection.json').read_bytes());schemas=strict((HERE/'schemas.json').read_bytes());raws=[]
 for r in sel['files']:
  p=sel['source_commit']+':'+r['path']
  if subprocess.check_output(['git','rev-parse',p],cwd=HERE,text=True).strip()!=r['git_blob_oid']:raise ValueError('commit binding')
  n=int(subprocess.check_output(['git','cat-file','-s',r['git_blob_oid']],cwd=HERE,text=True))
  if n!=r['bytes'] or n>sel['max_file_bytes']:raise ValueError('pre-read cap')
  raws.append(subprocess.check_output(['git','cat-file','blob',r['git_blob_oid']],cwd=HERE))
 result=inspect(raws,sel,schemas);dest=Path(dest);dest.mkdir(exist_ok=False)
 (dest/'inventory.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 (dest/'manifest.json').write_text(json.dumps({'source_commit':sel['source_commit'],'code_sha256':sha((HERE/'admit.py').read_bytes()),'selection_sha256':sha((HERE/'selection.json').read_bytes()),'inventory_sha256':sha((dest/'inventory.json').read_bytes()),'endpoint_classification':False},indent=2,sort_keys=True)+'\n')
 return result['status']
if __name__=='__main__':print(run(sys.argv[1]))
