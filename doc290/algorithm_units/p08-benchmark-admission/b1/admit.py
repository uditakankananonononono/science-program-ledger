"""Internal-document readiness inventory only; no authenticated science or benchmark."""
import ast, hashlib, json, platform, sys, time, urllib.request
from pathlib import Path, PurePosixPath
PIN="6db62c4f7d4a811da63c79c6a886c4762ad495e3"
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

def download(url, limit, budget, opener=None):
    opener = opener or urllib.request.build_opener(NoRedirect())
    req = urllib.request.Request(url, headers={'Accept-Encoding': 'identity', 'User-Agent': 'source-admission/2'})
    data = bytearray(); start = time.monotonic()
    with opener.open(req, timeout=20) as r:
        if r.status != 200 or r.geturl() != url:
            raise ValueError('status or redirected URL')
        if r.headers.get('Content-Encoding', 'identity').lower() != 'identity':
            raise ValueError('nonidentity transport')
        length = r.headers.get('Content-Length'); declared = None
        if length is not None:
            if not length.isdigit(): raise ValueError('invalid content length')
            declared = int(length)
            if declared > min(limit, budget[0]): raise ValueError('declared byte cap')
        while True:
            if time.monotonic() - start > 40: raise ValueError('transport deadline')
            remaining = min(limit-len(data), budget[0])
            if remaining <= 0:
                if declared == len(data): break
                raise ValueError('cap boundary without EOF proof')
            chunk = r.read(min(65536, remaining))
            if not chunk: break
            budget[0] -= len(chunk)
            if len(chunk) > remaining: raise ValueError('stream byte cap')
            data.extend(chunk)
        if declared is not None and len(data) != declared: raise ValueError('truncated content length')
    return bytes(data)

def verify(raw, spec):
    if len(raw) != spec['metadata_blob_size']: raise ValueError('pinned size mismatch')
    oid = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if oid != spec['git_blob_oid']: raise ValueError('pinned Git blob mismatch')
    return oid

def structural(raw, python_source=False):
    text=raw.decode('utf-8',errors='strict')
    result={'numbering':'Python str.splitlines 1-based, blank-inclusive; VT/FF boundaries',
      'lines':[{'line':i,'text':t} for i,t in enumerate(text.splitlines(),1)],
      'VT_count':text.count('\x0b'),'FF_count':text.count('\x0c')}
    if python_source:
        try:
            tree=ast.parse(text)
            result['ast_status']='parsed'
            result['definitions']=[{'type':type(n).__name__,'name':n.name,'start':n.lineno,'end':n.end_lineno} for n in ast.walk(tree) if isinstance(n,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef))]
            result['imports']=[{'line':n.lineno,'text':ast.get_source_segment(text,n)} for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]
            result['string_literals']=[{'line':n.lineno,'text':n.value} for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
        except (SyntaxError,ValueError,MemoryError,RecursionError) as e:
            result['ast_status']='error_retained';result['ast_error']=type(e).__name__+': '+str(e)
    return result

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def run(folder,retained=None):
    root=Path(__file__).parent
    for line in (root/'freeze-hashes.sha256').read_text().splitlines():
        h,name=line.split('  ',1)
        if sha(root/name)!=h:raise ValueError('freeze hash mismatch '+name)
    env=json.loads((root/'environment.json').read_text())
    if env['python']!=sys.version:raise ValueError('Python pin')
    sel=json.loads((root/'selection.json').read_text())
    if sel['source_commit']!=PIN or len(sel['files'])!=10 or len({r['path'] for r in sel['files']})!=10:raise ValueError('selection pin/count')
    out=Path(folder);out.mkdir(exist_ok=False);sources=out/'sources';sources.mkdir()
    budget=[sel['max_total_source_bytes']];records=[];verified={}
    # No AST, decode, text split or semantic analysis until all 11 verified.
    for spec in sel['files']:
        p=spec['path']
        if p.startswith('/') or '..' in PurePosixPath(p).parts:raise ValueError('unsafe path')
        url='https://raw.githubusercontent.com/uditakankananonononono/science-program-ledger/'+PIN+'/'+p
        rec={**spec,'url':url,'status':'unavailable'}
        try:
            if retained is None:raw=download(url,sel['max_file_bytes'],budget)
            else:
                with (Path(retained)/p).open('rb') as f:raw=f.read(min(sel['max_file_bytes'],budget[0])+1)
                budget[0]-=len(raw)
                if len(raw)>sel['max_file_bytes'] or budget[0]<0:raise ValueError('retained byte cap')
            target=sources/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
            rec.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
            rec['verified_git_blob_oid']=verify(raw,spec);rec['status']='verified';verified[p]=raw
        except Exception as e:rec['error']=type(e).__name__+': '+str(e)
        records.append(rec)
    dump(out/'inputs.json',records)
    if len(verified)!=10:
        dump(out/'structural.json',{'outcome':'REJECT source admission: not all10 identities verified','analysis_performed':False})
    else:
        inventory={}
        for p,raw in verified.items():
            try:inventory[p]=structural(raw,False)
            except UnicodeError as e:inventory[p]={'status':'invalid_utf8','error':str(e)}
        dump(out/'structural.json',{'outcome':'manual readiness inventory required; document reports are not authenticated external evidence','files':inventory,
            'scope':'fixed10 internal documents only; not proof of all code/data/protocols or published chronology',
            'claims':'No benchmark or numerical validation; no clinical/external rights clearance; document-reported reproduction is not authenticated'})
    dump(out/'manifest.json',{'code_sha256':sha(root/'admit.py'),'selection_sha256':sha(root/'selection.json'),'environment':env,
         'outputs':{p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file()}})
if __name__=='__main__':run(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None)
