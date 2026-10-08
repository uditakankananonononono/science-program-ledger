"""Bounded source admission only. Never auto-admit mapping or coordinates."""
import hashlib, io, json, math, re, sys, time, urllib.request
from fractions import Fraction
from pathlib import Path, PurePosixPath
from PIL import Image, ImageDraw
PIN = '1a0364c7509468dde0df86b4a82a8d8546b45818'
DIMENSION = 4096
PIXELS = 2400000
WORK_BYTES = 32 * 1024**2
CANVAS_BYTES = 800 * 620 * 3
Image.MAX_IMAGE_PIXELS = PIXELS
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

def decode(raw):
    with Image.open(io.BytesIO(raw)) as im:
        w, h = im.size
        if im.format not in ('JPEG', 'PNG'): raise ValueError('unsupported image format')
        if w <= 0 or h <= 0 or w > DIMENSION or h > DIMENSION or w*h > PIXELS:
            raise ValueError('header dimensions cap')
        if getattr(im, 'n_frames', 1) != 1: raise ValueError('single-frame only')
        if im.mode not in ('L', 'RGB', 'RGBA'): raise ValueError('unsupported source pixel mode')
        # Conservatively budget simultaneous source+RGB working pixels at 8 B/pixel,
        # plus FOUR 800x620 RGB display buffers; transport bytes budgeted separately.
        if w*h*8 + CANVAS_BYTES*4 > WORK_BYTES: raise ValueError('working pixel memory cap')
        im.load()
        return im.convert('RGB')

NUMBER = re.compile(r'^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$')
def number(s):
    if len(s) > 128 or not NUMBER.fullmatch(s): raise ValueError('malformed/nonfinite numeric token')
    if 'e' in s.lower() and abs(int(s.lower().split('e')[1])) > 308:
        raise ValueError('numeric exponent cap')
    f = Fraction(s)
    if not math.isfinite(float(f)): raise ValueError('numeric output conversion nonfinite')
    return f

def safe_corners(values):
    x, y, w, h = values
    c = [x, y, x+w, y+h]
    floats = [float(v) for v in c]
    if not all(math.isfinite(v) for v in floats): raise ValueError('derived output conversion nonfinite')
    return {'exact': [str(v) for v in c], 'finite_preview': floats}

def rows(raw, dimensions, max_rows=None):
    text = raw.decode('utf-8', errors='strict'); output=[]
    for n, line in enumerate(text.splitlines(), 1):
        if max_rows is not None and n > max_rows: break
        rec = {'raw_row_ordinal':n, 'raw':line, 'status':'unresolved', 'issues':[],
               'mapping':'UNRESOLVED', 'coordinates':'UNRESOLVED', 'candidate_corners':None}
        if not line.strip(): rec['issues'].append('blank_row')
        else:
            tokens = line.split(','); rec['field_count']=len(tokens)
            if len(tokens) != 4: rec['issues'].append('field_count')
            else:
                try:
                    v = [number(t.strip()) for t in tokens]
                    rec['candidate_corners'] = safe_corners(v)
                    if v[2] <= 0 or v[3] <= 0: rec['issues'].append('candidate_nonpositive_wh')
                    if n in dimensions:
                        w,h=dimensions[n]
                        if any(a<0 for a in (v[0],v[1])) or v[0]+v[2]>w or v[1]+v[3]>h:
                            rec['issues'].append('candidate_out_of_frame')
                    rec['candidate_geometry_only']='HYPOTHETICAL pixel/top-left x,y,w,h with row-n/frame-n alignment; not annotation validity'
                except (ValueError, OverflowError, ZeroDivisionError) as e:
                    rec['issues'].append(str(e)); rec['candidate_corners']=None
        output.append(rec)
    if not output: return [{'raw_row_ordinal':1,'raw':None,'status':'missing','issues':['empty_file'], 'mapping':'UNRESOLVED','coordinates':'UNRESOLVED','candidate_corners':None}]
    return output

def static(raw):
    text=raw.decode('utf-8', errors='strict')
    return {'line_count':len(text.splitlines()), 'comma_token_count':len(text.split(',')) if text else 0,
            'numbered_lines':[{'line':i,'text':s} for i,s in enumerate(text.splitlines(),1)],
            'semantics':'UNRESOLVED; no filename-derived meaning or polarity'}

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x): p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')

def run(folder, retained=None):
    root=Path(__file__).parent
    for line in (root/'freeze-hashes.sha256').read_text().splitlines():
        expected,name=line.split('  ',1)
        if digest(root/name)!=expected: raise ValueError('freeze hash mismatch: '+name)
    env=json.loads((root/'environment.json').read_text())
    if env['python']!=sys.version or env['Pillow']!=Image.__version__: raise ValueError('environment pin')
    sel=json.loads((root/'selection.json').read_text())
    if sel['source_commit'] != PIN or len(sel['files']) != 23 or len({a['path'] for a in sel['files']}) != 23:
        raise ValueError('selection pin/count')
    out=Path(folder);out.mkdir(exist_ok=False);source=out/'sources';source.mkdir()
    budget=[sel['max_total_source_bytes']]; metadata_total=0; verified={}; records=[]
    # ALL 23 identity checks precede any text analysis or image decoding.
    for spec in sel['files']:
        p=spec['path']
        if p.startswith('/') or '..' in PurePosixPath(p).parts: raise ValueError('unsafe path')
        limit=sel['max_image_bytes'] if spec['role']=='image' else sel['max_static_file_bytes']
        url='https://raw.githubusercontent.com/Kivo0/UsMicroMagSet/'+PIN+'/'+p
        rec={**spec,'url':url,'status':'unavailable'}
        try:
            if retained is None: raw=download(url,limit,budget)
            else:
                with (Path(retained)/p).open('rb') as f: raw=f.read(min(limit,budget[0])+1)
                budget[0]-=len(raw)
                if len(raw)>limit or budget[0]<0: raise ValueError('retained byte cap')
            if spec['role']=='static':
                metadata_total+=len(raw)
                if metadata_total>sel['max_static_total_bytes']: raise ValueError('combined static byte cap')
            target=source/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
            rec.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
            rec['verified_git_blob_oid']=verify(raw,spec)
            rec['status']='verified';verified[p]=raw
        except Exception as e: rec['error']=type(e).__name__+': '+str(e)
        records.append(rec)
    dump(out/'inputs.json',records)
    if len(verified)!=23:
        dump(out/'admission.json',{'outcome':'REJECT tracking/dynamics use','reason':'not all 23 pinned file identities verified','records':records})
        finish(root,out,env);return
    static_audit={};all_text_ok=True
    for s in sel['files']:
        if s['role']=='static':
            try: static_audit[s['path']]=static(verified[s['path']])
            except UnicodeError as e:
                static_audit[s['path']]={'status':'invalid_utf8','error':str(e)};all_text_ok=False
    dump(out/'static_provenance.json',static_audit)
    image_checks=[];dimensions={}
    for spec in sel['files']:
        if spec['role']!='image':continue
        n=int(Path(spec['path']).stem); rec={'path':spec['path'],'image_id':n,'status':'unsupported'}
        try:
            im=decode(verified[spec['path']]);dimensions[n]=im.size
            rec.update(status='decoded',width=im.width,height=im.height);im.close()
        except Exception as e: rec['error']=type(e).__name__+': '+str(e)
        image_checks.append(rec)
    gt='USMicroMagSet_For_tracking/cube/cube-1/groundtruth.txt'
    try: parsed=rows(verified[gt],dimensions,16)
    except UnicodeError as e: parsed=[{'raw_row_ordinal':1,'raw':None,'status':'invalid_utf8','issues':[str(e)]}]
    sample=[]
    for n in range(1,17):
        sample.append(parsed[n-1] if n<=len(parsed) else {'raw_row_ordinal':n,'raw':None,'status':'missing','issues':['missing_row']})
    # No source consumer is promoted to authoritative binding. Exact evidence audit
    # is human-reviewed, not inferred by count/visual fit. Conservative machine gate
    # remains unresolved; any established binding needs separate reviewed amendment.
    result={'outcome':'UNRESOLVED -> REJECT tracking/dynamics use',
      'row_frame_binding':'UNRESOLVED: explicit source-specific map not admitted',
      'coordinate_binding':'UNRESOLVED: source-specific convention/origin not admitted',
      'original_frame_provenance':'UNRESOLVED','all_static_utf8':all_text_ok,
      'groundtruth_raw_row_count':len(verified[gt].decode('utf-8',errors='strict').splitlines()) if all_text_ok else None,
      'first16_blank_row_count':sum('blank_row' in r.get('issues',[]) for r in parsed),
      'first16_raw_candidate_rows':sample,'images':image_checks,
      'claims':'No mapping/coordinates/tracker/identity/time/dynamics/bottleneck/invention or rights-clearance claim'}
    dump(out/'admission.json',result)
    for p in sel['fixed_display_paths']:
        n=int(Path(p).stem); panel=Image.new('RGB',(800,620),'white');d=ImageDraw.Draw(panel)
        d.text((12,10),f'cube-1 image {n:08d} | UNRESOLVED row/frame + coordinates',fill='black')
        try:
            im=decode(verified[p]);im.thumbnail((760,460));panel.paste(im,((800-im.width)//2,45));im.close()
        except Exception as e: d.text((12,70),'IMAGE UNSUPPORTED: '+str(e)[:95],fill='black')
        r=sample[n-1];text=str(r.get('raw'))
        d.text((12,525),f'Raw candidate row ordinal {n} shown SEPARATELY (not bound):',fill='black')
        for j in range(0,min(len(text),240),95):d.text((12,550+14*(j//95)),text[j:j+95],fill='black')
        d.text((12,605),'No box drawn. No alignment/coordinate calibration or tracking claim.',fill='black')
        panel.save(out/f'source_and_candidate_{n:08d}.png');panel.close()
    finish(root,out,env)

def finish(root,out,env):
    dump(out/'manifest.json',{'environment':env,'code_sha256':digest(root/'check.py'),
          'selection_sha256':digest(root/'selection.json'),'prereg_sha256':digest(root/'PREREG.md'),
          'outputs':{p.name:digest(p) for p in sorted(out.iterdir()) if p.is_file()}})

if __name__=='__main__':
    run(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else None)
