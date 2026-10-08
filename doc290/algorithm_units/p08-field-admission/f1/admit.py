"""F1 bounded Git blob identity and static format admission; no execution."""
import base64,binascii,hashlib,json,re,sys,time,urllib.request
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

def strict_json(raw):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d:raise ValueError('duplicate JSON key')
            d[k]=v
        return d
    def constant(x):raise ValueError('nonstandard JSON constant')
    return json.loads(raw.decode('utf-8',errors='strict'),object_pairs_hook=pairs,parse_constant=constant)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def blobsha(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def envelope(raw,spec,limit):
    j=strict_json(raw)
    if not isinstance(j,dict) or type(j.get('size')) is not int or j['size']!=spec['metadata_size'] or j.get('sha')!=spec['git_blob_sha1'] or j.get('url')!=spec['url'] or j.get('encoding')!='base64':raise ValueError('envelope identity/encoding')
    content=j.get('content')
    if not isinstance(content,str) or re.fullmatch(r'[A-Za-z0-9+/=\r\n]*',content) is None:raise ValueError('base64 alphabet/wrapping')
    normalized=content.replace('\r\n','\n')
    if '\r' in normalized:raise ValueError('bare CR base64 wrapping')
    normalized=normalized.replace('\n','')
    if len(normalized)>4*((limit+2)//3):raise ValueError('encoded decoded cap')
    try:data=base64.b64decode(normalized,validate=True)
    except binascii.Error as e:raise ValueError('base64 syntax') from e
    if base64.b64encode(data).decode()!=normalized:raise ValueError('noncanonical base64')
    if len(data)>limit or len(data)!=spec['metadata_size'] or blobsha(data)!=spec['git_blob_sha1']:raise ValueError('decoded identity/cap')
    return data

def binding(sel,commit,tree):
    if commit.get('sha')!=sel['commit'] or commit.get('commit',{}).get('tree',{}).get('sha')!=sel['commit_tree'] or tree.get('sha')!=sel['commit_tree'] or tree.get('truncated') is not False:raise ValueError('pinned commit/tree binding')
    records=tree.get('tree')
    if not isinstance(records,list):raise ValueError('tree records')
    mapped={}
    for r in records:
        if not isinstance(r,dict) or not isinstance(r.get('path'),str) or r['path'] in mapped:raise ValueError('tree path duplicate/type')
        mapped[r['path']]=r
    expected={r['path'] for r in records if r.get('type')=='blob' and (r['path'].startswith('data/navion_data/data/') or r['path'] in ['README.md','notebooks/processing/split_dataset.ipynb'])}
    if len(expected)!=62 or len(sel['files'])!=62 or {r['path'] for r in sel['files']}!=expected or sel['max_files']!=62:raise ValueError('selection complete count')
    for s in sel['files']:
        r=mapped[s['path']]
        if type(s.get('metadata_size')) is not int or type(r.get('size')) is not int or r['type']!='blob' or r['size']!=s['metadata_size'] or r['sha']!=s['git_blob_sha1'] or r['url']!=s['url']:raise ValueError('tree object mismatch')
        if not re.fullmatch(r'[0-9a-f]{40}',s['git_blob_sha1']):raise ValueError('blobsha syntax')

def parse(raw,path):
    text=raw.decode('utf-8',errors='strict')
    out={'raw_numbering':'Python splitlines 1-based,blank-inclusive,Unicode separators;NOT Unix/CSV/frame coordinates',
        'raw_lines':[{'raw_splitlines_ordinal':i,'text':x} for i,x in enumerate(text.splitlines(),1)],
        'claims':'literal static source/format only; no measurement/model/rights admission'}
    # Pointer grammar is byte ASCII LF-only, NOT Unicode raw coordinates.
    pointer=re.fullmatch(rb'version https://git-lfs.github.com/spec/v1\noid sha256:([0-9a-f]{64})\nsize (0|[1-9][0-9]*)\n',raw)
    if pointer:
        out['format']='git_lfs_pointer_syntax';out['declared_payload_sha256']=pointer.group(1).decode('ascii');out['declared_payload_size']=int(pointer.group(2));out['payload_accessed']=False
    elif text.startswith('version https://git-lfs.github.com/spec/'):
        out['format']='unresolved_pointer_like';out['payload_accessed']=False
    else:out['format']='utf8_text_unclassified'
    if path.endswith('.ipynb'):
        j=strict_json(raw)
        if not isinstance(j,dict) or type(j.get('nbformat')) is not int or not isinstance(j.get('cells'),list):raise ValueError('notebook structure')
        cells=[]
        for i,c in enumerate(j['cells']):
            if not isinstance(c,dict) or c.get('cell_type') not in ['code','markdown','raw']:raise ValueError('cell structure')
            source=c.get('source')
            if isinstance(source,str):source=[source]
            if not isinstance(source,list) or not all(isinstance(x,str) for x in source):raise ValueError('malformed notebook source')
            cells.append({'cell_ordinal':i+1,'cell_type':c['cell_type'],'source':source,'executed':False})
        out['static_cells']=cells;out['format']='notebook_static_source';out['outputs_used_as_evidence']=False
    return out

def run(folder,retained=None):
    root=Path(__file__).parent
    for line in (root/'freeze-hashes.sha256').read_text().splitlines():
        h,n=line.split('  ',1)
        if sha((root/n).read_bytes())!=h:raise ValueError('freeze hash '+n)
    env=strict_json((root/'environment.json').read_bytes())
    if env['python']!=sys.version:raise ValueError('Python pin')
    sel=strict_json((root/'selection.json').read_bytes())
    for n,h in sel['metadata_sha256'].items():
        if sha((root/n).read_bytes())!=h:raise ValueError('metadata pin')
    binding(sel,strict_json((root/'commit-metadata.json').read_bytes()),strict_json((root/'pinned-tree-metadata.json').read_bytes()))
    out=Path(folder);out.mkdir(exist_ok=False);(out/'envelopes').mkdir();(out/'sources').mkdir()
    budget=[8388608];decoded=0;records=[];verified={}
    for i,s in enumerate(sel['files'],1):
        rec={**s,'status':'unavailable','envelope_file':f'{i:03}.json'}
        try:
            if retained is None:raw=download(s['url'],131072,budget)
            else:
                raw=(Path(retained)/'envelopes'/f'{i:03}.json').read_bytes()
                budget[0]-=len(raw)
                if len(raw)>131072 or budget[0]<0:raise ValueError('retained envelope cap')
            (out/'envelopes'/f'{i:03}.json').write_bytes(raw)
            data=envelope(raw,s,min(sel['max_file_bytes'],sel['max_total_source_bytes']-decoded));decoded+=len(data)
            p=out/'sources'/s['path']
            if '..' in Path(s['path']).parts or Path(s['path']).is_absolute():raise ValueError('unsafe path')
            p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
            verified[s['path']]=data;rec.update(status='verified',bytes=len(data),sha256=sha(data),envelope_sha256=sha(raw))
        except Exception as e:rec['error']=type(e).__name__+': '+str(e)
        records.append(rec)
    dump(out/'inputs.json',records)
    if len(verified)!=62:dump(out/'inventory.json',{'outcome':'scoped unavailable:not all62identities verified','analysis_performed':False})
    else:
        inventory={}
        for path,data in verified.items():
            try:inventory[path]=parse(data,path)
            except (UnicodeError,ValueError) as e:inventory[path]={'status':'unresolved_text_or_notebook','error':str(e),'partial_analysis_used':False}
        dump(out/'inventory.json',{'outcome':'mandatory manual format/provenance ledger required','files':inventory})
    dump(out/'manifest.json',{'code_sha256':sha((root/'admit.py').read_bytes()),'environment':env,'outputs':{p.name:sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()}})
if __name__=='__main__':run(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None)
