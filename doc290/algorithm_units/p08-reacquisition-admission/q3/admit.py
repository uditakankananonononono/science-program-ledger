"""Q3 fixed full PDF local admission. All outputs private pending pixel review."""
import hashlib,json,math,os,re,resource,shutil,signal,struct,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
TOOLS=['/usr/bin/pdfinfo','/usr/bin/pdftotext','/usr/bin/pdftoppm']
def hash_handle(f):
    f.seek(0);h=hashlib.sha256();n=0
    while True:
        b=f.read(65536)
        if not b:break
        h.update(b);n+=len(b)
    return n,h.hexdigest()
def hashpath(p):
    with Path(p).open('rb') as f:return hash_handle(f)[1]
def pins():
    files={str(Path(sys.executable).resolve()),*TOOLS}
    for tool in TOOLS:
        text=subprocess.check_output(['/usr/bin/ldd',tool],text=True,timeout=20)
        if 'not found' in text:raise ValueError('missing dependency')
        for line in text.splitlines():
            match=re.search(r'(/[^\s]+)\s+\(',line)
            if match:files.add(str(Path(match.group(1)).resolve()))
    import _hashlib,_posixsubprocess
    modules=[hashlib,json,math,os,re,resource,shutil,signal,struct,subprocess,tempfile,_hashlib,_posixsubprocess]
    return {'python':sys.version,'files':{p:hashpath(p) for p in sorted(files)},'modules':{m.__name__:({'path':m.__file__,'sha256':hashpath(m.__file__)} if getattr(m,'__file__',None) else {'builtin_origin':m.__spec__.origin,'executable_covered':True}) for m in modules}}
def limits(cap):
    resource.setrlimit(resource.RLIMIT_AS,(2147483648,2147483648));resource.setrlimit(resource.RLIMIT_CPU,(20,20));resource.setrlimit(resource.RLIMIT_FSIZE,(cap,cap));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    if hasattr(os,'sched_getaffinity'):
        cpus=sorted(os.sched_getaffinity(0));os.sched_setaffinity(0,cpus[:2])
def command(args,stage,label,cap=1048576):
    stdout=stage/(label+'.stdout');stderr=stage/(label+'.stderr')
    with stdout.open('xb') as out,stderr.open('xb') as err:
        p=subprocess.Popen(args,stdout=out,stderr=err,stdin=subprocess.DEVNULL,env={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C'},preexec_fn=lambda:limits(cap),start_new_session=True)
        try:p.wait(timeout=30)
        except BaseException:
            os.killpg(p.pid,signal.SIGKILL);p.wait();raise
    if p.returncode!=0 or stdout.stat().st_size>cap or stderr.stat().st_size>cap:raise ValueError('native parser failure '+label)
    return stdout.read_bytes()
def info_pages(raw):
    text=raw.decode('utf-8',errors='strict')
    enc=re.findall(r'^Encrypted:\s*(.+)$',text,re.M);counts=re.findall(r'^Pages:\s*([0-9]+)\s*$',text,re.M)
    if len(enc)!=1 or enc[0]!='no' or len(counts)!=1:raise ValueError('encrypted/ambiguous pdfinfo')
    n=int(counts[0])
    if not 1<=n<=32:raise ValueError('page cap')
    return n
NUM=r'(?:0|[1-9][0-9]*)(?:\.[0-9]+)?'
def dimensions(raw,page):
    text=raw.decode('utf-8',errors='strict')
    sizes=re.findall(r'^Page\s+'+str(page)+r'\s+size:\s*('+NUM+r')\s+x\s+('+NUM+r')\s+pts(?:\s+\([^\n]*\))?\s*$',text,re.M)
    rotations=re.findall(r'^Page\s+'+str(page)+r'\s+rot:\s*([0-9]+)\s*$',text,re.M)
    if len(sizes)!=1 or len(rotations)!=1 or int(rotations[0]) not in (0,90,180,270):raise ValueError('page dimension ambiguity')
    w,h=map(float,sizes[0]);pw,ph=math.ceil(w*150/72),math.ceil(h*150/72)
    if w<=0 or h<=0 or (pw+1)*(ph+1)>20000000:raise ValueError('pixel preflight cap')
    if int(rotations[0]) in (90,270):pw,ph=ph,pw
    return pw,ph

def text_pages(raw,n):
    if len(raw)>1048576:raise ValueError('text cap')
    text=raw.decode('utf-8',errors='strict')
    # Poppler default final formfeed: exactly N separators, trailing empty segment retained.
    parts=text.split('\f')
    if len(parts)!=n+1 or parts[-1]!='':raise ValueError('text/page final formfeed grammar')
    records=[];total=0
    for page,segment in enumerate(parts[:-1],1):
        lines=segment.split('\n');total+=len(lines)
        if total>10000 or any(len(x)>16384 for x in lines):raise ValueError('literal line cap')
        records.append({'page':page,'lines':lines,'line_count_including_final_empty':len(lines),'blank_or_nontext':not segment.strip(),'ends_newline':segment.endswith('\n'),'separator_formfeed':True})
    return records

def png_shape(path):
    with path.open('rb') as f:head=f.read(24)
    if head[:8]!=b'\x89PNG\r\n\x1a\n' or head[12:16]!=b'IHDR' or len(head)!=24:raise ValueError('PNG header')
    w,h=struct.unpack('>II',head[16:24])
    if not w or not h or w*h>20000000:raise ValueError('PNG pixel cap')
    return w,h

def verify_freeze():
    for line in (HERE/'freeze-hashes.sha256').read_text().splitlines():
        h,p=line.split('  ',1)
        if hashpath(HERE/p)!=h:raise ValueError('freeze '+p)
    if pins()!=json.loads((HERE/'environment.json').read_text()):raise ValueError('environment changed')

def run(source,dest,sel=None):
    sel=sel or json.loads((HERE/'selection.json').read_text());dest=Path(dest)
    if dest.exists() or dest.is_symlink():raise ValueError('destination exists')
    dest.parent.mkdir(parents=True,exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='.q3-incomplete-',dir=dest.parent))
    try:
        with Path(source).open('rb') as original:
            original_stat=os.fstat(original.fileno());expected=(sel['bytes'],sel['sha256'])
            if hash_handle(original)!=expected:raise ValueError('original identity')
            scratch=stage/'held-source.pdf'
            original.seek(0)
            with scratch.open('xb') as out:shutil.copyfileobj(original,out,65536)
            with scratch.open('rb') as held:
                held_stat=os.fstat(held.fileno())
                def identities():
                    if hash_handle(original)!=expected or hash_handle(held)!=expected:raise ValueError('held identity changed')
                    if os.fstat(original.fileno())!=original_stat or os.fstat(held.fileno())!=held_stat:raise ValueError('held stat changed')
                    if os.stat(scratch)!=held_stat:raise ValueError('scratch path binding')
                identities();n=info_pages(command([TOOLS[0],'-box',str(scratch)],stage,'info'))
                shapes=[]
                for page in range(1,n+1):
                    identities()
                    raw=command([TOOLS[0],'-f',str(page),'-l',str(page),'-box',str(scratch)],stage,f'dim-{page}')
                    shapes.append(dimensions(raw,page))
                identities()
                raw=command([TOOLS[1],'-layout','-enc','UTF-8',str(scratch),'-'],stage,'text')
                pages=text_pages(raw,n)
                render_total=0;renders=[]
                for page,(pw,ph) in enumerate(shapes,1):
                    identities();remaining=sel['max_render_bytes']-render_total
                    # PNG cannot exceed conservative uncompressed RGBA scanlines plus overhead.
                    bound=((pw+1)*4+1)*(ph+1)+1048576
                    if bound>remaining:raise ValueError('render preflight byte budget')
                    prefix=stage/f'page-{page}'
                    command([TOOLS[2],'-f',str(page),'-l',str(page),'-singlefile','-r','150','-png',str(scratch),str(prefix)],stage,f'render-{page}',cap=remaining)
                    image=prefix.with_suffix('.png');size=image.stat().st_size;actual=png_shape(image)
                    if abs(actual[0]-pw)>1 or abs(actual[1]-ph)>1 or size>remaining:raise ValueError('render association/budget')
                    render_total+=size;renders.append({'page':page,'file':image.name,'width':actual[0],'height':actual[1],'preflight_width':pw,'preflight_height':ph,'bytes':size,'sha256':hashpath(image)})
                identities()
                # Private-only complete text retained including blank/final/separator evidence.
                (stage/'private-text-pages.json').write_text(json.dumps(pages,indent=2,ensure_ascii=True)+'\n')
                manifest={'status':'complete_parser_outputs_PENDING_ALL_PAGE_PIXEL_REVIEW','source_bytes':sel['bytes'],'source_sha256':sel['sha256'],'pages':n,'text_bytes':len(raw),'text_sha256':hashlib.sha256(raw).hexdigest(),'text_page_association':'exact N formfeeds plus trailing empty split; LF lines retain blank/final empty','text_counts':[{'page':p['page'],'lines':len(p['lines']),'blank_or_nontext':p['blank_or_nontext']} for p in pages],'renders':renders,'render_bytes':render_total,'visual_coverage_complete':False,'endpoint_classification':False}
                (stage/'parser-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
                os.rename(stage,dest);return manifest
    finally:
        if stage.exists():shutil.rmtree(stage)

def interrupt(s,f):raise InterruptedError('signal '+str(s))
if __name__=='__main__':
    signal.signal(signal.SIGTERM,interrupt);signal.signal(signal.SIGINT,interrupt)
    verify_freeze();print(json.dumps(run(sys.argv[1],sys.argv[2]),indent=2))
