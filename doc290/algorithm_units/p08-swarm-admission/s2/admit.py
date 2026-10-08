"""Bounded all-identity-gated raw text inventory; no endpoint/data admission."""
import hashlib, json, sys, time, urllib.request
from pathlib import Path
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

def verify(raw,spec):
    if len(raw)!=spec['metadata_size']:raise ValueError('pinned size mismatch')
    if hashlib.md5(raw).hexdigest()!=spec['metadata_md5']:raise ValueError('pinned MD5 mismatch')

def parse(raw):
    text=raw.decode('utf-8',errors='strict')
    return {'raw_numbering':'Python splitlines 1-based,blank-inclusive,VT/FF boundaries; NOT Unix lines or CSV records',
      'raw_lines':[{'raw_splitlines_ordinal':i,'text':line} for i,line in enumerate(text.splitlines(),1)],
      'VT_count':text.count('\x0b'),'FF_count':text.count('\x0c'),
      'BOM_count':text.count('\ufeff'),'claims':'literal text only; no delimiter/schema/numeric/unit/endpoint inference'}

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
    if sha(root/'record-metadata.json')!=sel['metadata_sha256'] or sel['record_id']!=17453570 or len(sel['files'])!=13 or sel['max_files']!=13 or len({r['path'] for r in sel['files']})!=13:raise ValueError('selection pin/count')
    out=Path(folder);out.mkdir(exist_ok=False);sources=out/'sources';sources.mkdir()
    budget=[sel['max_total_source_bytes']];records=[];verified={}
    for spec in sel['files']:
        p=spec['path']
        if Path(p).name!=p:raise ValueError('unsafe source name')
        rec={**spec,'status':'unavailable'}
        try:
            if retained is None:raw=download(spec['url'],sel['max_file_bytes'],budget)
            else:
                with (Path(retained)/p).open('rb') as f:raw=f.read(min(sel['max_file_bytes'],budget[0])+1)
                budget[0]-=len(raw)
                if len(raw)>sel['max_file_bytes'] or budget[0]<0:raise ValueError('retained byte cap')
            (sources/p).write_bytes(raw)
            rec.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),received_md5=hashlib.md5(raw).hexdigest())
            verify(raw,spec);rec['status']='verified';verified[p]=raw
        except Exception as e:rec['error']=type(e).__name__+': '+str(e)
        records.append(rec)
    dump(out/'inputs.json',records)
    # ALL13 size+MD5 checks precede ANY text analysis.
    if len(verified)!=13:
        dump(out/'inventory.json',{'outcome':'scoped unavailable: not all13 identities verified','analysis_performed':False})
    else:
        inventory={}
        for p,raw in verified.items():
            try:inventory[p]=parse(raw)
            except UnicodeError as e:inventory[p]={'status':'invalid_utf8','error':str(e)}
        dump(out/'inventory.json',{'outcome':'manual endpoint/budget/trial binding ledger required','files':inventory,
          'claims':'No delimiter/schema/numeric/delivery/physiology/independence/rights admission from text alone'})
    dump(out/'manifest.json',{'code_sha256':sha(root/'admit.py'),'selection_sha256':sha(root/'selection.json'),'environment':env,
      'outputs':{p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file()}})
if __name__=='__main__':run(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None)
