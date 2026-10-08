"""D4 static serialization token inventory; never unpickle or reconstruct."""
import hashlib,json,pickletools,sys,time,urllib.request
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

def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def verify(raw,s):
    if len(raw)!=s['metadata_size'] or hashlib.md5(raw).hexdigest()!=s['metadata_md5']:raise ValueError('pinned size/MD5')
def disassemble(raw,caps):
    records=[];stop=None
    try:
        for ordinal,(opcode,arg,offset) in enumerate(pickletools.genops(raw),1):
            if ordinal>caps['opcodes']:raise ValueError('opcode cap')
            literal=repr(arg)
            if len(literal)>caps['argument_repr_characters']:raise ValueError('argument repr cap')
            records.append({'opcode_ordinal':ordinal,'byte_offset_0based':offset,'opcode':opcode.name,'argument_literal_repr':literal,'argument_status':'serialization token only,not reconstructed object/numeric calibration'})
            if opcode.name=='STOP':stop=offset
        if stop is None:raise ValueError('missing STOP')
    except Exception as e:
        return {'status':'unresolved_syntax_or_cap','error':type(e).__name__+': '+str(e),'partial_inventory_exposed':False,'original_bytes':len(raw),'original_sha256':sha(raw)}
    trailing=raw[stop+1:]
    return {'status':'static_prefix_with_trailing_bytes' if trailing else 'static_complete_opcode_stream',
      'opcodes':records,'STOP_byte_offset_0based':stop,'prefix_bytes':stop+1,'original_bytes':len(raw),
      'trailing_byte_count':len(trailing),'trailing_sha256':sha(trailing),'original_sha256':sha(raw),
      'claims':'genops syntax only; no memo reconstruction/object schema/safety/calibration proof',
      'trailing_status':'uninterpreted trailing bytes retained in original,NOT whole-stream pickle syntax admission' if trailing else 'none'}
def run(folder,retained=None):
    root=Path(__file__).parent
    for line in (root/'freeze-hashes.sha256').read_text().splitlines():
        h,n=line.split('  ',1)
        if sha((root/n).read_bytes())!=h:raise ValueError('freeze hash '+n)
    e=json.loads((root/'environment.json').read_text())
    if e['python']!=sys.version or sha(Path(pickletools.__file__).read_bytes())!=e['pickletools_sha256']:raise ValueError('environment/module pin')
    sel=json.loads((root/'selection.json').read_text());s=sel['files'][0]
    if len(sel['files'])!=1 or sel['record_id']!=1306230 or sha((root/'record-metadata.json').read_bytes())!=sel['metadata_sha256']:raise ValueError('selection pin')
    out=Path(folder);out.mkdir(exist_ok=False);(out/'sources').mkdir();r={**s,'status':'unavailable'}
    try:
        if retained is None:raw=download(s['url'],sel['max_file_bytes'],[sel['max_total_source_bytes']])
        else:
            with (Path(retained)/s['path']).open('rb') as f:raw=f.read(sel['max_file_bytes']+1)
            if len(raw)>sel['max_file_bytes']:raise ValueError('retained cap')
        (out/'sources'/s['path']).write_bytes(raw);r.update(bytes=len(raw),sha256=sha(raw),md5=hashlib.md5(raw).hexdigest());verify(raw,s);r['status']='verified'
    except Exception as ex:r['error']=type(ex).__name__+': '+str(ex)
    dump(out/'inputs.json',[r])
    if r['status']!='verified':inv={'outcome':'scoped unavailable: original identity not verified','analysis_performed':False}
    else:inv={'outcome':'mandatory manual serialization/provenance ledger required','inventory':disassemble(raw,e['caps'])}
    dump(out/'inventory.json',inv)
    dump(out/'manifest.json',{'code_sha256':sha((root/'admit.py').read_bytes()),'environment':e,'outputs':{p.name:sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()}})
if __name__=='__main__':run(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None)
