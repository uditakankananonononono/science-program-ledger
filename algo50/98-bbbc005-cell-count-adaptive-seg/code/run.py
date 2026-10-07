import numpy as np, zipfile, io, re, json, warnings
from PIL import Image
from scipy import ndimage as ndi
from skimage import filters, feature, segmentation, measure
warnings.filterwarnings('ignore')
Z=zipfile.ZipFile('data/img.zip')
files=sorted(f for f in Z.namelist() if f.endswith('_w1.TIF'))
meta=[]
for f in files:
    m=re.search(r'_([A-P])(\d+)_C(\d+)_F(\d+)_s(\d+)_w1',f); meta.append((f,int(m[2]),int(m[3]),int(m[4])))
dev=[m for m in meta if m[1]<=12]; tst=[m for m in meta if m[1]>=13]
rd=np.random.RandomState(0); dev=[dev[i] for i in rd.choice(len(dev),600,replace=False)]
rt=np.random.RandomState(1); tst=[tst[i] for i in rt.choice(len(tst),1200,replace=False)]
dev=dev[:100]; tst=tst[:300]
print(len(files),len(dev),len(tst),flush=True)
def load(f): return np.array(Image.open(io.BytesIO(Z.read(f))))
def cnt_b(im,s,m):
    im=im.astype(float)
    g=ndi.gaussian_filter(im,s) if s>0 else im; t=filters.threshold_otsu(g); mask=g>t
    d=ndi.distance_transform_edt(mask); pk=feature.peak_local_max(d,min_distance=m,labels=measure.label(mask),exclude_border=False)
    return len(pk)
def blur(im):
    im=im.astype(float); return 1.0/(ndi.laplace(ndi.gaussian_filter(im,1)).var()+1e-9)
def cnt_a(im,b,bmed,k,th):
    im=im.astype(float)
    n=(im-im.min())/(im.max()-im.min()+1e-9); sc=1+k*(b/bmed-1); sig=np.linspace(2,8,7)*max(sc,0.3)
    return len(feature.blob_log(n,min_sigma=sig[0],max_sigma=sig[-1],num_sigma=7,threshold=th,overlap=0.5))
# equivalence
yy,xx=np.mgrid[:200,:300]; syn=np.zeros((200,300))
for cy,cx in ((50,50),(50,150),(50,250),(150,80),(150,200)): syn[(yy-cy)**2+(xx-cx)**2<=36]=200
assert cnt_b(syn,1,5)==5 and cnt_a(syn,1.0,1.0,0,0.04)==5
Dim=[(load(f),c) for f,_,c,_ in dev]
bl=np.array([blur(im) for im,_ in Dim]); bmed=float(np.median(bl))
best=None
for s in (0,1,2):
    for m in (3,5,7):
        e=np.mean([abs(cnt_b(im,s,m)-c) for im,c in Dim]); print('dev B',s,m,round(e,3),flush=True)
        if best is None or e<best[0]-1e-12: best=(e,s,m)
_,sB,mB=best; bestA=None
for k in (0,.5):
    for th in (.04,.08):
        e=np.mean([abs(cnt_a(im,bl[i],bmed,k,th)-c) for i,(im,c) in enumerate(Dim)]); print('dev A',k,th,round(e,3),flush=True)
        if bestA is None or e<bestA[0]-1e-12: bestA=(e,k,th)
_,kA,tA=bestA
eb=[];ea=[];e0=[];F=[]
for i,(f,_,c,fo) in enumerate(tst):
    im=load(f); b=blur(im); eb.append(cnt_b(im,sB,mB)-c); ea.append(cnt_a(im,b,bmed,kA,tA)-c); e0.append(cnt_a(im,b,bmed,0,tA)-c); F.append(fo)
eb,ea,e0,F=map(np.array,(eb,ea,e0,F)); ab,aa=np.abs(eb),np.abs(ea)
d=ab-aa; rs=np.random.RandomState(7); bs=[d[rs.randint(0,len(d),len(d))].mean() for _ in range(10000)]
lo,hi=np.percentile(bs,[2.5,97.5]); rel=d.mean()/ab.mean()
v='WIN' if rel>=.10 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
grp=lambda a,m:float(a[m].mean())
out=dict(baseline=dict(s=sB,m=mB,dev_mae=best[0]),asb=dict(k=kA,th=tA,dev_mae=bestA[0]),test=dict(mae_base=float(ab.mean()),mae_asb=float(aa.mean()),mae_k0=float(np.abs(e0).mean()),rel_reduction=float(rel),diff=float(d.mean()),ci=[float(lo),float(hi)]),
 by_focus={n:dict(base=grp(ab,m),asb=grp(aa,m)) for n,m in (('F<=10',F<=10),('11-30',(F>10)&(F<=30)),('31-48',F>30))},verdict=v)
json.dump(out,open('results.json','w'),indent=1); print(json.dumps(out))
