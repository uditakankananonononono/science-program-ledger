"""FOVEA reviewed common-endpoint diagnostic, not a routing invention."""
import json,hashlib,zipfile,sys,importlib.metadata
from pathlib import Path
from itertools import combinations
import numpy as np
from scipy.ndimage import label
ROOT=Path(__file__).resolve().parents[2]

def endpoints(a,b,limit=16):
    points=np.argwhere(a & b);m=len(points);k=min(limit,m)
    return m,[tuple(map(int,points[(j*(m-1))//(k-1)])) for j in range(k)] if k>=2 else []

def diagnostic(a,b):
    m,pts=endpoints(a,b);la,ca=label(a,np.ones((3,3),int));lb,cb=label(b,np.ones((3,3),int))
    queries=[];counts=dict.fromkeys(['both_reachable','A1_only','A2_only','neither'],0)
    for s,t in combinations(pts,2):
        x=bool(la[s]==la[t]);y=bool(lb[s]==lb[t]);kind='both_reachable' if x and y else 'A1_only' if x else 'A2_only' if y else 'neither'
        counts[kind]+=1;queries.append({'source':s,'target':t,'components_A1':[int(la[s]),int(la[t])],'components_A2':[int(lb[s]),int(lb[t])],'classification':kind})
    n1=int(a.sum());n2=int(b.sum())
    return {'shared_skeleton_pixels':m,'skeleton_pixels_A1':n1,'skeleton_pixels_A2':n2,'shared_coverage_A1':{'numerator':m,'denominator':n1},'shared_coverage_A2':{'numerator':m,'denominator':n2},'endpoint_count':len(pts),'status':'measured' if len(pts)>=2 else 'insufficient_shared_endpoints','query_count':len(queries),'counts':counts,'components_A1':int(ca),'components_A2':int(cb),'queries':queries}

def admit(archive,p):
    if p['max_endpoints']!=16 or p['connectivity']!=8:raise ValueError('protocol rule')
    if hashlib.sha256(Path(archive).read_bytes()).hexdigest()!=p['archive_sha256']:raise ValueError('archive hash')
    for name,sha in p['pipeline_sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('pipeline hash')
    for name,v in p['versions'].items():
        if importlib.metadata.version(name)!=v:raise ValueError('version')
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:raise ValueError('CRC')
        names={Path(n).name:n for n in z.namelist() if not n.endswith('/')}
        if len(names)!=160 or set(names)!={r['path'] for r in p['masks']}:raise ValueError('membership')
        for r in p['masks']:
            raw=z.read(names[r['path']])
            if len(raw)!=r['size_bytes'] or hashlib.sha256(raw).hexdigest()!=r['sha256']:raise ValueError('mask hash')
    return names

def run(archive,p):
    names=admit(archive,p) # before loading extractor or extraction
    sys.path.insert(0,str(ROOT))
    from hrf_extract import extract_member
    records=[]
    for patient in range(1,41):
        for phase in ('p','i'):
            stems=[f'FOVEA{patient:03d}_{phase}_ve_{a}.png' for a in (1,2)]
            qa,a=extract_member(archive,names[stems[0]]);qb,b=extract_member(archive,names[stems[1]])
            if a.shape!=b.shape:raise ValueError('paired shape')
            records.append({'patient':f'FOVEA{patient:03d}','phase':phase,'image_sha256_A1':qa['image_sha256'],'image_sha256_A2':qb['image_sha256'],'skeleton_sha256_A1':qa['skeleton_sha256'],'skeleton_sha256_A2':qb['skeleton_sha256'],**diagnostic(a,b)})
    return records
if __name__=='__main__':
    p=json.loads(Path(__file__).with_name('protocol.json').read_text())
    print(json.dumps(run(sys.argv[1],p),indent=2))
