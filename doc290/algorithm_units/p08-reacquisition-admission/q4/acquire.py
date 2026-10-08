"""Q4 fixed expiring ranged route. Opaque storage only; checkpoint interruption fails closed."""
import hashlib,json,os,re,shutil,signal,sys,tempfile,time,urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent
DISK_CAP=3221225472
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None

def hashfile(p):
    n=0;h=hashlib.sha256()
    with p.open('rb') as f:
        while True:
            b=f.read(65536)
            if not b:break
            n+=len(b);h.update(b)
    return n,h.hexdigest()

def binding(sel):
    return {'selection_sha256':hashlib.sha256(json.dumps(sel,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'code_sha256':hashfile(Path(__file__))[1]}

def pins():
    import http.client,ssl,socket,_ssl,_hashlib,urllib.error,urllib.parse,email.message,email.parser
    ms=[hashlib,json,os,re,shutil,signal,tempfile,time,urllib.request,http.client,ssl,socket,_ssl,_hashlib,urllib.error,urllib.parse,email.message,email.parser]
    return {'python':sys.version,'executable_sha256':hashfile(Path(sys.executable))[1],'modules':{m.__name__:({'path':m.__file__,'sha256':hashfile(Path(m.__file__))[1]} if getattr(m,'__file__',None) else {'builtin':m.__spec__.origin,'executable_covered':True}) for m in ms}}

def fsyncdir(p):
    fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)

def atomic(p,value):
    temp=p.parent/(p.name+'.tmp')
    with temp.open('x') as f:
        json.dump(value,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(temp,p);fsyncdir(p.parent)

def nodups(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise ValueError('duplicate JSON key')
        d[k]=v
    return d

def load(p):
    if p.stat().st_size>1048576:raise ValueError('checkpoint metadata cap')
    return json.loads(p.read_text(),object_pairs_hook=nodups,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('JSON constant')))
def exact_int(x):return type(x) is int

def spans(sel):
    n=sel['metadata_bytes'];r=sel['range_bytes']
    return [(start,min(start+r,n)-1) for start in range(0,n,r)]
def schedule(sel):return [(pas,i,lo,hi) for pas in [1,2] for i,(lo,hi) in enumerate(spans(sel))]
def name(pas,index):return f'pass{pas}-chunk{index:04d}.bin'

def disk(root,extra=0):
    total=0
    for p in root.iterdir():
        if p.is_symlink() or not p.is_file():raise ValueError('foreign nonregular path')
        total+=p.stat().st_size
    if total+extra>DISK_CAP:raise ValueError('global disk budget')
    return total

def terminal(root,reason):
    # O_EXCL + fsync durable terminal marker, independent of possibly corrupt checkpoint.
    p=root/'TERMINAL-FAILED.json'
    if p.exists():return
    with p.open('x') as f:
        json.dump({'status':'TERMINAL_FAILED','reason':reason[:1200]},f,sort_keys=True);f.flush();os.fsync(f.fileno())
    fsyncdir(root)

def verify(root,sel):
    if (root/'TERMINAL-FAILED.json').exists():raise ValueError('terminal failed: no retry')
    p=root/'checkpoint.json';c=load(p)
    if set(c)!={'version','binding','status','receipts','inflight'} or type(c['version']) is not int or c['version']!=1 or c['binding']!=binding(sel):raise ValueError('checkpoint schema/binding')
    if c['status'] not in ('ACTIVE','COMPLETE') or c['inflight'] is not None:raise ValueError('interrupted/inflight state cannot resume')
    if type(c['receipts']) is not list:raise ValueError('receipt type')
    sch=schedule(sel)
    if len(c['receipts'])>len(sch):raise ValueError('receipt coverage')
    expected={'checkpoint.json'}
    for rec,(pas,i,lo,hi) in zip(c['receipts'],sch):
        if type(rec) is not dict or set(rec)!={'pass','index','start','end','bytes','sha256','file'}:raise ValueError('receipt schema')
        if any(not exact_int(rec[k]) for k in ['pass','index','start','end','bytes']):raise ValueError('integer types')
        if (rec['pass'],rec['index'],rec['start'],rec['end'],rec['bytes'],rec['file'])!=(pas,i,lo,hi,hi-lo+1,name(pas,i)):raise ValueError('receipt frozen span')
        if type(rec['sha256']) is not str or not re.fullmatch('[0-9a-f]{64}',rec['sha256']):raise ValueError('receipt hash')
        expected.add(rec['file'])
        chunk=root/rec['file']
        if not chunk.is_file() or chunk.is_symlink() or hashfile(chunk)!=(hi-lo+1,rec['sha256']):raise ValueError('completed chunk identity')
    if c['status']=='COMPLETE':
        if len(c['receipts'])!=len(sch):raise ValueError('complete coverage')
        expected|={'opaque-pass1.bin','opaque-pass2.bin','manifest.json'}
        manifest=load(root/'manifest.json')
        if manifest.get('status')!='COMPLETE_OPAQUE_TWO_PASS_BINDING_DISCOVERED' or manifest.get('binding')!=binding(sel) or manifest.get('url')!=sel['url'] or manifest.get('full_stream_compare') is not True:raise ValueError('completed manifest binding')
        acquisitions=manifest.get('acquisitions')
        if type(acquisitions) is not list or len(acquisitions)!=2:raise ValueError('complete acquisition schema')
        for pas,rec in zip([1,2],acquisitions):
            if type(rec) is not dict or set(rec)!={'pass','bytes','discovered_sha256'} or type(rec['pass']) is not int or rec['pass']!=pas or type(rec['bytes']) is not int or rec['bytes']!=sel['metadata_bytes'] or not re.fullmatch('[0-9a-f]{64}',rec['discovered_sha256']):raise ValueError('complete acquisition identity')
            if hashfile(root/f'opaque-pass{pas}.bin')!=(sel['metadata_bytes'],rec['discovered_sha256']):raise ValueError('completed archive mutation')
        compare(root/'opaque-pass1.bin',root/'opaque-pass2.bin')
    if set(p.name for p in root.iterdir())!=expected:raise ValueError('foreign/orphan/missing fileset')
    disk(root)
    return c

def singleton(h,key,required=True):
    values=h.get_all(key,[])
    if not values:
        if required:raise ValueError('missing '+key)
        return None
    if len(values)!=1 or any(x in values[0] for x in [',','\r','\n']):raise ValueError('ambiguous '+key)
    return values[0]

def fetch(sel,lo,hi,path,root,opener=None,clock=time.monotonic):
    opener=opener or urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    req=urllib.request.Request(sel['url'],headers={'Range':f'bytes={lo}-{hi}','Accept-Encoding':'identity','User-Agent':'opaque-range-binding/1'})
    count=0;h=hashlib.sha256();start=clock();span=hi-lo+1
    with opener.open(req,timeout=20) as r:
        if r.status!=206 or r.geturl()!=sel['url']:raise ValueError('206 exact route required')
        if singleton(r.headers,'Content-Range')!=f'bytes {lo}-{hi}/{sel["metadata_bytes"]}':raise ValueError('exact canonical range')
        if singleton(r.headers,'Content-Length')!=str(span):raise ValueError('exact canonical length')
        if singleton(r.headers,'Content-Type').split(';',1)[0].strip().lower() not in ('application/octet-stream','application/zip'):raise ValueError('frozen MIME allowlist')
        enc=singleton(r.headers,'Content-Encoding',False)
        if enc is not None and enc.lower()!='identity':raise ValueError('encoding')
        if singleton(r.headers,'Transfer-Encoding',False) is not None:raise ValueError('transfer encoding')
        with path.open('xb') as out:
            while True:
                if clock()-start>90:raise TimeoutError('between-read deadline')
                b=r.read(min(sel['stream_chunk_bytes'],span-count+1))
                if not b:break
                if count+len(b)>span:raise ValueError('range cap before write')
                disk(root,len(b));out.write(b);out.flush();count+=len(b);h.update(b)
            if count!=span:raise ValueError('range exact EOF')
            out.flush();os.fsync(out.fileno())
    return count,h.hexdigest()

def compare(a,b):
    with a.open('rb') as x,b.open('rb') as y:
        while True:
            ax=x.read(65536);by=y.read(65536)
            if ax!=by:raise ValueError('two pass full stream mismatch')
            if not ax:return

def finish(root,sel,c):
    c['inflight']={'finalization':True};atomic(root/'checkpoint.json',c)
    results=[]
    for pas in [1,2]:
        tmp=root/f'opaque-pass{pas}.tmp';final=root/f'opaque-pass{pas}.bin'
        with tmp.open('xb') as out:
            for rec in c['receipts']:
                if rec['pass']!=pas:continue
                with (root/rec['file']).open('rb') as f:
                    while True:
                        b=f.read(65536)
                        if not b:break
                        disk(root,len(b));out.write(b);out.flush()
            out.flush();os.fsync(out.fileno())
        n,h=hashfile(tmp)
        if n!=sel['metadata_bytes']:raise ValueError('archive metadata size')
        os.rename(tmp,final);fsyncdir(root);results.append({'pass':pas,'bytes':n,'discovered_sha256':h})
    compare(root/'opaque-pass1.bin',root/'opaque-pass2.bin')
    if results[0]['discovered_sha256']!=results[1]['discovered_sha256']:raise ValueError('aggregate hash mismatch')
    for pas,rec in zip([1,2],results):
        if hashfile(root/f'opaque-pass{pas}.bin')!=(rec['bytes'],rec['discovered_sha256']):raise ValueError('post compare mutation')
    for rec in c['receipts']:
        if hashfile(root/rec['file'])!=(rec['end']-rec['start']+1,rec['sha256']):raise ValueError('final chunk rehash')
    manifest={'status':'COMPLETE_OPAQUE_TWO_PASS_BINDING_DISCOVERED','binding':binding(sel),'url':sel['url'],'acquisitions':results,'ranges_each':len(spans(sel)),'full_stream_compare':True,'source_strong_validator':None,'source_body_parse':False,'unscanned_risk':True,'origin_immutability':False,'authorship_proven':False,'global_disk_bytes':disk(root)}
    atomic(root/'manifest.json',manifest);c['inflight']=None;c['status']='COMPLETE';atomic(root/'checkpoint.json',c)
    verify(root,sel);return manifest

def batch(root,sel,opener=None,clock=time.monotonic):
    root=Path(root)
    if type(sel['metadata_bytes']) is not int or not 0<sel['metadata_bytes']<=sel['max_archive_bytes'] or type(sel['ranges_per_invocation']) is not int or not 1<=sel['ranges_per_invocation']<=3:raise ValueError('frozen operational selection caps')
    if root.is_symlink():raise ValueError('checkpoint root symlink')
    if not root.exists():
        root.mkdir();atomic(root/'checkpoint.json',{'version':1,'binding':binding(sel),'status':'ACTIVE','receipts':[],'inflight':None})
    try:
        c=verify(root,sel)
        if c['status']=='COMPLETE':return load(root/'manifest.json')
        sch=schedule(sel)
        if len(c['receipts'])==len(sch):return finish(root,sel,c)
        count=0
        while count<sel['ranges_per_invocation'] and len(c['receipts'])<len(sch):
            pas,i,lo,hi=sch[len(c['receipts'])]
            c['inflight']={'pass':pas,'index':i};atomic(root/'checkpoint.json',c)
            tmp=root/(name(pas,i)+'.tmp')
            n,h=fetch(sel,lo,hi,tmp,root,opener,clock)
            if hashfile(tmp)!=(hi-lo+1,h):raise ValueError('chunk postread identity')
            os.rename(tmp,root/name(pas,i));fsyncdir(root)
            c['receipts'].append({'pass':pas,'index':i,'start':lo,'end':hi,'bytes':n,'sha256':h,'file':name(pas,i)})
            c['inflight']=None;atomic(root/'checkpoint.json',c);count+=1
        verify(root,sel)
        return {'status':'VERIFIED_PREFIX_PENDING','completed_ranges':len(c['receipts']),'total_ranges':len(sch),'new_ranges':count}
    except BaseException as ex:
        terminal(root,type(ex).__name__+': '+str(ex));raise

def verify_freeze():
    for line in (HERE/'freeze-hashes.sha256').read_text().splitlines():
        h,n=line.split('  ',1)
        if hashfile(HERE/n)[1]!=h:raise ValueError('freeze '+n)
    if pins()!=load(HERE/'environment.json'):raise ValueError('environment')
def interrupt(s,f):raise InterruptedError('signal '+str(s))
if __name__=='__main__':
    signal.signal(signal.SIGTERM,interrupt);signal.signal(signal.SIGINT,interrupt)
    verify_freeze();print(json.dumps(batch(sys.argv[1],load(HERE/'selection.json')),indent=2))
