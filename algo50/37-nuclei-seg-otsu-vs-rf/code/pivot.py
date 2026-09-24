import numpy as np,json,skimage.io as io
from skimage.measure import label
from skimage.filters import gaussian,threshold_otsu
from skimage.segmentation import watershed,find_boundaries
from skimage.feature import peak_local_max,multiscale_basic_features
from skimage.morphology import remove_small_objects
from scipy import ndimage as ndi
from sklearn.ensemble import RandomForestClassifier
R='../data/'; L=lambda f:[x.strip() for x in open(R+'metadata/'+f) if x.strip()]
TR,VA,TE=L('training.txt'),L('validation.txt'),L('test.txt')
def img(f):
    x=io.imread(R+'images/'+f.replace('.png','.tif')).astype(np.float32); lo,hi=np.percentile(x,[1,99.8]); return np.clip((x-lo)/(hi-lo+1e-9),0,1)
def gt(f): return label(io.imread(R+'masks/'+f)[...,0],background=0,connectivity=1)
def f1(g,p,thr):
    ng,np_=g.max(),p.max()
    if ng==0 or np_==0: return 0.0
    m=(g>0)&(p>0); pairs,cnt=np.unique(g[m].astype(np.int64)*(np_+1)+p[m],return_counts=True)
    gi,pi=pairs//(np_+1),pairs%(np_+1); ag=np.bincount(g.ravel(),minlength=ng+1); ap=np.bincount(p.ravel(),minlength=np_+1)
    iou=cnt/(ag[gi]+ap[pi]-cnt); tp=(iou>thr).sum(); return 2*tp/(ng+np_)
def otsu(x,s,md):
    y=gaussian(x,s); fg=ndi.binary_fill_holes(y>threshold_otsu(y)); fg=remove_small_objects(fg,30)
    if md is None: return label(fg)
    dt=ndi.distance_transform_edt(fg); pk=peak_local_max(dt,min_distance=md,labels=label(fg),exclude_border=False)
    mk=np.zeros_like(fg,int); mk[tuple(pk.T)]=np.arange(1,len(pk)+1); lab=watershed(-dt,mk,mask=fg)
    return label(remove_small_objects(lab,30)>0) if False else remove_small_objects(lab,30)
FE=lambda x:multiscale_basic_features(x,sigma_min=1,sigma_max=8).astype(np.float32)
rng=np.random.default_rng(37); Xs=[];ys=[]
for f in TR:
    g=gt(f); b=find_boundaries(g,mode='inner'); cls=np.where(g>0,1,0); cls[b]=2; F=FE(img(f))
    for c in (0,1,2):
        idx=np.flatnonzero(cls.ravel()==c); idx=rng.choice(idx,min(len(idx),1667),replace=False); Xs.append(F.reshape(-1,F.shape[-1])[idx]); ys.append(np.full(len(idx),c))
rf=RandomForestClassifier(100,max_depth=20,n_jobs=-1,random_state=37).fit(np.vstack(Xs),np.concatenate(ys)); del Xs; print('rf trained',flush=True)
def prob(x): F=FE(x); return rf.predict_proba(F.reshape(-1,F.shape[-1])).reshape(x.shape+(3,))
def rseg(P,t):
    fg=(P[...,1]+P[...,2])>0.5; sd=label(P[...,1]>t); lab=watershed(-P[...,1],sd,mask=fg); return remove_small_objects(lab,30)
cache={}
def get(f):
    if f not in cache: x=img(f); cache[f]=(x,prob(x),gt(f))
    return cache[f]
BG=[(s,md) for s in (1,2) for md in (10,13,16,20)]; TG=[0.6,0.7,0.8]
val={'B':{str(k):float(np.mean([f1(get(f)[2],otsu(get(f)[0],*k),0.5) for f in VA])) for k in BG},
     'R':{str(t):float(np.mean([f1(get(f)[2],rseg(get(f)[1],t),0.5) for f in VA])) for t in TG}}
kb=max(BG,key=lambda k:val['B'][str(k)]); kt=max(TG,key=lambda t:val['R'][str(t)]); print('val',val,kb,kt,flush=True)
cache.clear(); rows=[]
for f in TE:
    x,P,g=get(f); pb=otsu(x,*kb); pr=rseg(P,kt)
    rows.append([f1(g,pb,0.5),f1(g,pr,0.5),f1(g,pb,0.75),f1(g,pr,0.75),int(g.max())]); cache.clear()
A=np.array(rows); np.savetxt('../results/per_image_test_pivot.tsv',A,delimiter='\t',header='B_f1_50\tR_f1_50\tB_f1_75\tR_f1_75\tn_gt',comments='')
B=[];ii_=np.arange(len(A))
for _ in range(2000):
    ii=rng.integers(0,len(A),len(A)); m=A[ii].mean(0); B.append([m[1]-m[0],m[3]-m[2]])
B=np.array(B); ci=lambda v:[float(x) for x in np.percentile(v,[2.5,97.5])]; m=A.mean(0)
res={'val':val,'chosen_B':str(kb),'chosen_t':kt,'test_mean':{'B_f1_50':m[0],'R_f1_50':m[1],'B_f1_75':m[2],'R_f1_75':m[3]},
 'd1':m[1]-m[0],'ci1':ci(B[:,0]),'d2':m[3]-m[2],'ci2':ci(B[:,1]),'frac_R_ge_B':float((A[:,1]>=A[:,0]).mean())}
res['gates']={'P1':bool(res['d1']>=0.03 and res['ci1'][0]>0),'P2':bool(res['ci2'][0]>0)}
json.dump(res,open('../results/pivot_metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
