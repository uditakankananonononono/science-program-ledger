"""T3 static literal XML inventory only; no tracking/pixel/physical calibration."""
import hashlib,json,re,sys,time,urllib.request
from pathlib import Path
import defusedxml,defusedxml.ElementTree as DX,defusedxml.common,xml.etree.ElementTree as ET
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

def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=True,indent=2,allow_nan=False)+'\n')
def verify(raw,s):
    gitsha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if len(raw)!=s['metadata_size'] or gitsha!=s['git_blob_sha1']:raise ValueError('pinned size/Git blob SHA1')
def inventory(raw,caps):
    try:
        text=raw.decode('utf-8',errors='strict')
        declaration=re.match(r'^\ufeff?<\?xml\s+([^?]*)\?>',text)
        if declaration:
            encoding=re.search(r'encoding\s*=\s*([\'"])(.*?)\1',declaration.group(1))
            if encoding and encoding.group(2).lower() not in ('utf-8','utf8'):raise ValueError('non-UTF8 declaration excluded')
        root=DX.fromstring(text,forbid_dtd=True,forbid_entities=True,forbid_external=True)
        records=[];stack=[(root,[],1,1)];textchars=attrchars=0
        while stack:
            node,parent,tagordinal,childordinal=stack.pop()
            path=parent+[{'expanded_name':node.tag,'same_expanded_name_sibling_ordinal_1based':tagordinal,'element_child_ordinal_1based':childordinal}]
            if len(path)>caps['depth'] or len(records)>=caps['nodes']:raise ValueError('depth/node cap')
            textchars+=len(node.text or '')+len(node.tail or '')
            attrchars+=sum(len(k)+len(v) for k,v in node.attrib.items())
            if textchars>caps['text_characters'] or attrchars>caps['attribute_characters']:raise ValueError('literal character cap')
            records.append({'document_element_preorder_ordinal_1based':len(records)+1,'path_segments':path,'attributes':dict(sorted(node.attrib.items())),'text':node.text,'tail':node.tail})
            children=[];counts={}
            for i,ch in enumerate(node,1):
                counts[ch.tag]=counts.get(ch.tag,0)+1;children.append((ch,path,counts[ch.tag],i))
            stack.extend(reversed(children))
        return {'status':'static_complete_element_inventory','elements':records,'element_count':len(records),'literal_text_tail_characters':textchars,'attribute_characters':attrchars,'original_sha256':sha(raw),'partial_inventory_exposed':False}
    except Exception as ex:
        return {'status':'unresolved_syntax_unsafe_encoding_or_cap','error':type(ex).__name__+': '+str(ex),'partial_inventory_exposed':False,'original_sha256':sha(raw)}
def analyze(raws,selection,caps):
    if len(raws)!=len(selection['files']):return {'analysis_performed':False,'outcome':'identity incomplete'}
    try:
        for raw,s in zip(raws,selection['files']):verify(raw,s)
    except Exception as ex:return {'analysis_performed':False,'outcome':'identity failed','error':str(ex)}
    return {'analysis_performed':True,'outcome':'mandatory manual annotation/provenance ledger required','inventory':[inventory(r,caps) for r in raws]}
def pins():
    modules=(defusedxml,DX,defusedxml.common,ET)
    return {'python':sys.version,'python_executable_path':sys.executable,'python_executable_sha256':sha(Path(sys.executable).read_bytes()),'modules':{m.__name__:{'path':m.__file__,'sha256':sha(Path(m.__file__).read_bytes())} for m in modules}}
def run(folder,retained=None):
    here=Path(__file__).parent
    for line in (here/'freeze-hashes.sha256').read_text().splitlines():
        h,n=line.split('  ',1)
        if sha((here/n).read_bytes())!=h:raise ValueError('freeze hash '+n)
    env=json.loads((here/'environment.json').read_text())
    if pins()!=env['pins']:raise ValueError('Python/module bytes changed')
    sel=json.loads((here/'selection.json').read_text())
    for n,h in sel['metadata_sha256'].items():
        if sha((here/n).read_bytes())!=h:raise ValueError('metadata pin '+n)
    if len(sel['files'])!=2:raise ValueError('selection count')
    out=Path(folder);out.mkdir(exist_ok=False);(out/'sources').mkdir()
    inputs=[];raws=[];budget=[sel['max_total_source_bytes']]
    for i,s in enumerate(sel['files']):
        record={**s,'status':'unavailable'}
        try:
            if retained is None:raw=download(s['url'],sel['max_file_bytes'],budget)
            else:
                with (Path(retained)/('source-'+str(i)+'.xml')).open('rb') as f:raw=f.read(sel['max_file_bytes']+1)
                if len(raw)>sel['max_file_bytes'] or len(raw)>budget[0]:raise ValueError('retained caps')
                budget[0]-=len(raw)
            (out/'sources'/('source-'+str(i)+'.xml')).write_bytes(raw)
            record.update(bytes=len(raw),sha256=sha(raw));verify(raw,s);record['status']='verified';raws.append(raw)
        except Exception as ex:record['error']=type(ex).__name__+': '+str(ex)
        inputs.append(record)
    dump(out/'inputs.json',inputs)
    inv=analyze(raws,sel,env['caps']) if all(r['status']=='verified' for r in inputs) else {'analysis_performed':False,'outcome':'scoped unavailable: both identities required'}
    dump(out/'inventory.json',inv)
    dump(out/'manifest.json',{'environment':env,'outputs':{p.name:sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()}})
if __name__=='__main__':run(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None)
