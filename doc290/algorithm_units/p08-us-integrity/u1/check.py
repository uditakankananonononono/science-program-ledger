"""Bounded descriptive source admission, no author code execution or learned model."""
import csv,hashlib,io,json,math,sys,urllib.request,urllib.error,time,re,platform
from pathlib import Path,PurePosixPath
from PIL import Image,ImageDraw
COMMIT='1a0364c7509468dde0df86b4a82a8d8546b45818'
CAP=64*1024**2;PIXELS=2400000;TIMEOUT=20
Image.MAX_IMAGE_PIXELS=PIXELS
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None

def download(url,limit,budget,opener=None):
    opener=opener or urllib.request.build_opener(NoRedirect())
    request=urllib.request.Request(url,headers={'User-Agent':'source-admission/1','Accept-Encoding':'identity'})
    data=bytearray();started=time.monotonic()
    with opener.open(request,timeout=TIMEOUT) as response:
        if response.status!=200:raise ValueError('HTTP status')
        if response.headers.get('Content-Encoding','identity')!='identity':raise ValueError('compressed transfer unsupported')
        length=response.headers.get('Content-Length')
        declared=None
        if length is not None:
            if not length.isdigit():raise ValueError('invalid content length')
            declared=int(length)
            if declared>min(limit,budget[0]):raise ValueError('declared byte cap')
        while True:
            remaining=min(limit-len(data),budget[0])
            if time.monotonic()-started>40:raise ValueError('40s transport deadline')
            if remaining<=0:
                if response.headers.get('Content-Length')==str(len(data)):break
                raise ValueError('cap boundary without EOF proof')
            chunk=response.read(min(65536,remaining))
            if not chunk:break
            budget[0]-=len(chunk)
            if len(chunk)>remaining:raise ValueError('stream byte cap')
            data.extend(chunk)
        if declared is not None and len(data)!=declared:raise ValueError('truncated content length')
    return bytes(data)

def decode(raw):
    with Image.open(io.BytesIO(raw)) as im:
        if im.format not in ('PNG','JPEG'):raise ValueError('image format')
        w,h=im.size
        if w<=0 or h<=0 or w*h>PIXELS or w>4096 or h>4096:raise ValueError('decoded dimensions cap')
        if getattr(im,'n_frames',1)!=1:raise ValueError('multi-frame unsupported')
        im.load();return im.convert('RGB')

def labels(raw,w,h):
    text=raw.decode('utf-8');lines=text.splitlines();rows=[]
    for n,line in enumerate(lines,1):
        if not line.strip():continue
        parts=line.split();row={'line':n,'raw':line,'valid':False,'issues':[],'corners_px':None}
        if len(parts)!=5:row['issues'].append('field_count')
        else:
            try:
                values=[float(a) for a in parts]
                if not all(math.isfinite(a) for a in values):row['issues'].append('nonfinite')
                else:
                    cls,x,y,bw,bh=values;row['class']=cls
                    if cls<0 or not cls.is_integer():row['issues'].append('class_nonnegative_integer')
                    if bw<=0 or bh<=0:row['issues'].append('nonpositive_wh')
                    corners=[x-bw/2,y-bh/2,x+bw/2,y+bh/2]
                    pixel=[corners[0]*w,corners[1]*h,corners[2]*w,corners[3]*h]
                    if not all(math.isfinite(c) for c in corners+pixel):row['issues'].append('derived_arithmetic_nonfinite')
                    else:row['corners_px']=pixel
                    if any(c<0 or c>1 for c in corners):row['issues'].append('out_of_frame')
            except ValueError:row['issues'].append('non_numeric')
        row['valid']=not row['issues'];rows.append(row)
    return {'status':'empty' if not rows else 'multirow' if len(rows)>1 else 'single','row_count':len(rows),'invalid_rows':sum(not a['valid'] for a in rows),'rows':rows}

def run(folder):
    root=Path(__file__).parent;environment=json.load(open(root/'environment.json'))
    if sys.version!=environment['python'] or Image.__version__!=environment['Pillow']:raise ValueError('environment pin')
    sel=json.load(open(root/'selection.json'));paths=(root/'paths.txt').read_text().splitlines()
    if sel['source_commit']!=COMMIT or hashlib.sha256((root/'paths.txt').read_bytes()).hexdigest()!=sel['inventory_paths_sha256']:raise ValueError('selection/inventory pin')
    out=Path(folder);out.mkdir(exist_ok=False);sources=out/'sources';sources.mkdir();budget=[CAP];records=[]
    yaml_paths=[f'{r}/dataset.yaml' if f'{r}/dataset.yaml' in paths else f'{r}/sample.yaml' for r in ['cube','cylinder','flagella','helical','rollingcube','sheetrobot','sphere1','sphere3']]
    source_specs=[('README.md',131072),('LICENSE',131072)]+[(a,131072) for a in yaml_paths]
    source_specs += [(s[k],2097152 if k=='image' else 65536) for s in sel['selection'] for k in ('image','label') if s[k]]
    if len(source_specs)>58 or len(set(a for a,b in source_specs))!=len(source_specs):raise ValueError('file cap/duplicate selection')
    fetched={}
    for name,limit in source_specs:
        if name.startswith('/') or '..' in PurePosixPath(name).parts:raise ValueError('path traversal')
        url='https://raw.githubusercontent.com/Kivo0/UsMicroMagSet/'+COMMIT+'/'+name
        rec={'path':name,'url':url,'status':'unavailable'}
        try:
            raw=download(url,limit,budget);target=sources/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
            rec.update(status='retrieved',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest());fetched[name]=raw
        except Exception as e:rec['error']=type(e).__name__+':'+str(e)
        records.append(rec)
        if budget[0]<=0:break
    yaml_checks=[]
    for name in yaml_paths:
        text=fetched.get(name,b'').decode('utf-8',errors='replace')
        # Static text evidence only: do not execute local paths or infer names from helper code.
        matches=re.findall(r'^nc:\s*(\d+)\s*$',text,re.M)
        nc=int(matches[0]) if len(matches)==1 else None
        yaml_checks.append({'path':name,'status':'retrieved' if name in fetched else 'unavailable','nc':nc,'class_name_lines':[a for a in text.splitlines() if 'names:' in a or re.match(r'^\s*\d+:',a)],'raw_text':text,'mapping':'unresolved until raw nc/names reviewed; no relabeling'})
    checked=[];overlay=[]
    for s in sel['selection']:
        row={**s,'status':'unavailable'};im=None
        try:
            if s['image'] not in fetched or s['label'] not in fetched:raise ValueError('missing selected source pair')
            im=decode(fetched[s['image']]);w,h=im.size;row.update(status='checked',width=w,height=h,image_sha256=hashlib.sha256(fetched[s['image']]).hexdigest(),annotation=labels(fetched[s['label']],w,h))
        except Exception as e:row['error']=type(e).__name__+':'+str(e)
        if row['status']=='checked':
            nc=next(a['nc'] for a in yaml_checks if a['path'].startswith(s['robot']+'/'))
            row['declared_nc']=nc
            row['classes_outside_declared_count']=[a['line'] for a in row['annotation']['rows'] if 'class' in a and nc is not None and a['class']>=nc]
        checked.append(row)
        if s['overlay']:
            panel=Image.new('RGB',(640,400),'#fff');d=ImageDraw.Draw(panel)
            if im is not None and row['status']=='checked' and 'annotation' in row:
                for box in row['annotation']['rows']:
                    if box['corners_px'] is not None and box['valid']:
                        ImageDraw.Draw(im).rectangle(box['corners_px'],outline='red',width=4)
                im.thumbnail((640,340));panel.paste(im,((640-im.width)//2,30))
            d.text((5,4),s['robot']+'/'+s['split']+'/'+s['frame_token'],fill='black');d.text((5,375),row['status']+' '+str(row.get('annotation',{}).get('status',row.get('error','')))+' invalid='+str(row.get('annotation',{}).get('invalid_rows','NA')),fill='black');overlay.append(panel)
    for i in range(0,len(overlay),4):
        canvas=Image.new('RGB',(1280,800),'white')
        for j,a in enumerate(overlay[i:i+4]):canvas.paste(a,((j%2)*640,(j//2)*400))
        canvas.save(out/f'overlay_{i//4+1}.png')
    inventory={};stems={};images=set();labs=set()
    for a in paths:
        parts=a.split('/')
        if len(parts)==4 and parts[1] in ('images','labels'):
            key='/'.join(parts[:3]);inventory[key]=inventory.get(key,0)+1
            normalized=(parts[0],parts[2],Path(parts[-1]).stem)
            (images if parts[1]=='images' else labs).add(normalized)
            if parts[1]=='images':stems.setdefault((parts[0],Path(parts[-1]).stem),[]).append(a)
    hashes={}
    for a in checked:
        if a['status']=='checked':hashes.setdefault(a['image_sha256'],[]).append(a['image'])
    result={'records':checked,'path_inventory':inventory,'image_without_label':sorted(images-labs),'label_without_image':sorted(labs-images),'repeated_image_stems':[v for v in stems.values() if len(v)>1],'sample_content_duplicates':[v for v in hashes.values() if len(v)>1],'source_video_mapping':'unresolved; prefix not proven video identity','source_bytes_received':CAP-budget[0],'yaml_paths':yaml_paths,'yaml_static':yaml_checks,'sample_adjacency':[{'robot':a['robot'],'prefix':a['source_prefix'],'splits':[a['split'],b['split']],'frames':[a['frame_token'],b['frame_token']]} for i,a in enumerate(checked) for b in checked[i+1:] if a.get('source_prefix') is not None and a['robot']==b['robot'] and a['source_prefix']==b['source_prefix'] and str(a['frame_token']).isdigit() and str(b['frame_token']).isdigit() and abs(int(a['frame_token'])-int(b['frame_token']))==1],'prior_exposure':'reviewer cube/test/Cube2-000008.png+label,not blind or held-out'}
    (out/'integrity.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');(out/'inputs.json').write_text(json.dumps(records,indent=2)+'\n')
    manifest={'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':sys.version,'Pillow':Image.__version__,'environment_sha256':hashlib.sha256((root/'environment.json').read_bytes()).hexdigest(),'platform':platform.platform(),'selection_sha256':hashlib.sha256((root/'selection.json').read_bytes()).hexdigest(),'outputs':{a.name:hashlib.sha256(a.read_bytes()).hexdigest() for a in sorted(out.iterdir()) if a.is_file()}}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1])
