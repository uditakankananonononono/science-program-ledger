"""Q2 opaque bytes only. No source-format analysis or parser imports."""
import hashlib, http.client, json, os, re, shutil, signal, socket, ssl, sys, tempfile, time, urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None

def sha_file(path):
    h=hashlib.sha256(); n=0
    with Path(path).open('rb') as f:
        while True:
            b=f.read(65536)
            if not b: break
            h.update(b); n+=len(b)
    return n,h.hexdigest()

def pins():
    import _hashlib, _ssl, _socket, urllib.error, urllib.parse, email.message, email.parser
    modules=[hashlib,http.client,urllib.request,urllib.error,urllib.parse,socket,ssl,_hashlib,_ssl,_socket,email.message,email.parser]
    return {'python':sys.version,'executable':str(Path(sys.executable).resolve()),'executable_sha256':sha_file(sys.executable)[1],
        'modules':{m.__name__:({'path':m.__file__,'sha256':sha_file(m.__file__)[1]} if getattr(m,'__file__',None) else {'builtin_origin':m.__spec__.origin,'covered_by_executable_pin':True}) for m in modules}}

def singleton(headers,name,required=False):
    values=headers.get_all(name,[])
    if not values:
        if required: raise ValueError('missing '+name)
        return None
    if len(values)!=1 or ',' in values[0] or '\r' in values[0] or '\n' in values[0]: raise ValueError('ambiguous '+name)
    return values[0]

def fetch(sel,path,opener=None,clock=time.monotonic):
    opener=opener or urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    start=clock(); count=0; h=hashlib.sha256()
    req=urllib.request.Request(sel['url'],headers={'Accept-Encoding':'identity','If-Match':sel['opaque_etag'],'User-Agent':'opaque-binding/1'})
    with opener.open(req,timeout=20) as r:
        if r.status!=200 or r.geturl()!=sel['url']: raise ValueError('status/route')
        etag=singleton(r.headers,'ETag',True)
        if not re.fullmatch(r'"[^"\x00-\x20\x7f,]+"',etag) or etag!=sel['opaque_etag']: raise ValueError('strong opaque ETag')
        mime=singleton(r.headers,'Content-Type',True)
        if mime.split(';',1)[0].strip().lower()!='application/pdf': raise ValueError('MIME')
        encoding=singleton(r.headers,'Content-Encoding')
        if encoding is not None and encoding.lower()!='identity': raise ValueError('encoding')
        if singleton(r.headers,'Transfer-Encoding') is not None: raise ValueError('unsupported transfer encoding')
        length=singleton(r.headers,'Content-Length')
        if length is not None and (not re.fullmatch(r'0|[1-9][0-9]*',length) or len(length)>7 or int(length)>sel['max_bytes']): raise ValueError('length/cap')
        with path.open('xb') as out:
            while True:
                if clock()-start>120: raise TimeoutError('between-read deadline')
                b=r.read(min(sel['chunk_bytes'],sel['max_bytes']-count+1))
                if not b: break
                if count+len(b)>sel['max_bytes']: raise ValueError('stream cap before write')
                out.write(b);h.update(b);count+=len(b)
            if not count or (length is not None and count!=int(length)): raise ValueError('EOF size')
            out.flush();os.fsync(out.fileno())
    return {'url':sel['url'],'status':200,'opaque_etag':etag,'mime':mime,'content_encoding':encoding,'content_length':length,'bytes':count,'discovered_sha256':h.hexdigest()}

def compare(a,b):
    with a.open('rb') as x,b.open('rb') as y:
        while True:
            ax=x.read(65536);by=y.read(65536)
            if ax!=by: raise ValueError('full-stream byte mismatch')
            if not ax: return True

def acquire(sel,dest,opener=None,clock=time.monotonic):
    dest=Path(dest)
    if dest.exists() or dest.is_symlink(): raise ValueError('output exists')
    dest.parent.mkdir(parents=True,exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='.q2-incomplete-',dir=dest.parent))
    try:
        records=[]
        for n in [1,2]: records.append(fetch(sel,stage/f'opaque-{n}.bin',opener,clock))
        if records[0]['bytes']!=records[1]['bytes'] or records[0]['discovered_sha256']!=records[1]['discovered_sha256']: raise ValueError('acquisition mismatch')
        compare(stage/'opaque-1.bin',stage/'opaque-2.bin')
        # Rehash after comparison. Checks reproducibility, not immutable/authenticated origin.
        for n,record in enumerate(records,1):
            if sha_file(stage/f'opaque-{n}.bin')!=(record['bytes'],record['discovered_sha256']): raise ValueError('local mutation')
        manifest={'outcome':'same_byte_binding_discovered','acquisitions':records,'full_stream_compare':True,'body_analysis':False,'independent_origin_servers':False,'origin_immutability_proven':False}
        (stage/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
        os.rename(stage,dest)
        return manifest
    finally:
        if stage.exists(): shutil.rmtree(stage)

def verify_freeze():
    for line in (HERE/'freeze-hashes.sha256').read_text().splitlines():
        h,name=line.split('  ',1)
        if sha_file(HERE/name)[1]!=h: raise ValueError('freeze '+name)
    if pins()!=json.loads((HERE/'environment.json').read_text()): raise ValueError('environment changed')

def interrupted(signum,frame): raise InterruptedError('signal '+str(signum))
if __name__=='__main__':
    signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    verify_freeze()
    print(json.dumps(acquire(json.loads((HERE/'selection.json').read_text()),sys.argv[1]),indent=2))
