"""Q5 whole central-directory metadata only, identity before all parser calls."""
import hashlib,json,os,shutil,sys,tempfile,zipfile,struct,stat,re
from pathlib import Path
import scanner
HERE=Path(__file__).resolve().parent

def sha(p):
    with Path(p).open('rb') as f:return hashf(f)[1]
def hashf(f):
    f.seek(0);h=hashlib.sha256();n=0
    while True:
        b=f.read(65536)
        if not b:break
        n+=len(b);h.update(b)
    return n,h.hexdigest()
def pins():
    import _hashlib,zlib
    ms=[hashlib,json,os,shutil,tempfile,zipfile,struct,stat,re,_hashlib,zlib]
    return {'python':sys.version,'executable_sha256':sha(sys.executable),'modules':{m.__name__:({'path':m.__file__,'sha256':sha(m.__file__)} if getattr(m,'__file__',None) else {'builtin':m.__spec__.origin,'executable_covered':True}) for m in ms}}
def verify():
    for line in (HERE/'freeze-hashes.sha256').read_text().splitlines():
        h,p=line.split('  ',1)
        if sha(HERE/p)!=h:raise ValueError('freeze '+p)
    if pins()!=json.loads((HERE/'environment.json').read_text()):raise ValueError('environment changed')

def run(source,dest,sel=None):
    sel=sel or json.loads((HERE/'selection.json').read_text());dest=Path(dest)
    if dest.exists() or dest.is_symlink():raise ValueError('output exists')
    stage=Path(tempfile.mkdtemp(prefix='.q5-incomplete-',dir=dest.parent))
    try:
        with Path(source).open('rb') as f:
            state=os.fstat(f.fileno());expected=(sel['bytes'],sel['sha256'])
            if sel['bytes']>sel['max_archive_bytes'] or hashf(f)!=expected:raise ValueError('entire source identity before parse')
            inv=scanner.directory(f,sel)
            if hashf(f)!=expected or os.fstat(f.fileno())!=state:raise ValueError('source mutation')
            # Stream serialization to bounded file, not whole-output RAM assembly.
            encoder=json.JSONEncoder(indent=2,sort_keys=True,ensure_ascii=True,allow_nan=False)
            count=0
            with (stage/'inventory.json').open('xb') as out:
                for piece in encoder.iterencode(inv):
                    b=piece.encode('utf-8');count+=len(b)
                    if count+1>67108864:raise ValueError('output cap')
                    out.write(b)
                out.write(b'\n')
            manifest={'source_bytes':sel['bytes'],'source_sha256':sel['sha256'],'entry_count':inv['entry_count'],'inventory_bytes':count+1,'inventory_sha256':sha(stage/'inventory.json'),'member_reads':False,'local_header_reads':False,'scope':'central metadata and conservative declared local spans only'}
            (stage/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
            os.rename(stage,dest);return manifest
    finally:
        if stage.exists():shutil.rmtree(stage)
if __name__=='__main__':verify();print(json.dumps(run(sys.argv[1],sys.argv[2]),indent=2))
