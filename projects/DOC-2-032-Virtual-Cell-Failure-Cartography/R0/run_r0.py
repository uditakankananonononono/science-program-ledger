#!/usr/bin/env python3
import h5py, numpy as np, pandas as pd, scipy.sparse as sp, json, hashlib, math
from pathlib import Path
FN='AdamsonWeissman2016_GSM2406675_10X001.h5ad'; SEED=32032
with h5py.File(FN,'r') as f:
 shape=tuple(map(int,f['X'].attrs['shape']))
 X=sp.csc_matrix((f['X/data'][:],f['X/indices'][:],f['X/indptr'][:]),shape=shape).tocsr().astype(float)
 cats=np.array([x.decode() for x in f['obs/perturbation/categories'][:]])
 labels=cats[f['obs/perturbation/codes'][:]]
 genes=np.array([x.decode() for x in f['var/gene_symbol'][:]])
# CPM-ish log normalization
s=np.asarray(X.sum(1)).ravel(); sf=np.divide(1e4,s,out=np.zeros_like(s),where=s>0)
X=sp.diags(sf)@X; X.data=np.log1p(X.data)
uniq,counts=np.unique(labels,return_counts=True); countmap=dict(zip(uniq,counts))
control='*'; perts=[p for p in uniq if p!=control and countmap[p]>=50]
ctrl=np.where(labels==control)[0]
# eligible genes by overall detection >=20; select 2000 by control variance only
eligible=np.asarray((X>0).sum(0)).ravel()>=20
m1=np.asarray(X[ctrl].mean(0)).ravel(); m2=np.asarray(X[ctrl].power(2).mean(0)).ravel(); var=m2-m1*m1
idx=np.where(eligible)[0]; idx=idx[np.argsort(var[idx],kind='stable')[-min(2000,len(idx)):]]
# fixed within-condition random split
rng=np.random.default_rng(SEED); halves=[]
for h in [0,1]:
 d={}
 for p in uniq:
  z=np.where(labels==p)[0].copy(); rng2=np.random.default_rng(SEED+int(hashlib.sha256(p.encode()).hexdigest()[:8],16)); rng2.shuffle(z); d[p]=z[h::2]
 halves.append(d)
def corr(a,b):
 a=a-a.mean(); b=b-b.mean(); den=np.linalg.norm(a)*np.linalg.norm(b); return float(a@b/den) if den else float('nan')
rows=[]
for h,d in enumerate(halves,1):
 c=np.asarray(X[d[control]][:,idx].mean(0)).ravel()
 for p in perts:
  y=np.asarray(X[d[p]][:,idx].mean(0)).ravel(); resp=y-c; pred=c
  r=corr(pred,y); top=np.argsort(np.abs(resp))[-min(50,len(resp)):]
  sign=float(np.mean((np.sign(np.zeros(len(top)))==np.sign(resp[top])) & (np.sign(resp[top])!=0)))
  rel=0.0
  if r>=.90 and sign<=.55: lab='metric_mirage'
  elif r<.90 and rel<=.25: lab='transparent_collapse'
  elif sign<=.55: lab='other_directional_failure'
  else: lab='directionally_adequate'
  # centered correlation: predicted response all zero => undefined
  rows.append(dict(half=h,perturbation=p,n_cells=len(d[p]),r_abs=r,response_capture=0.0,top50_sign=sign,relative_response_norm=rel,taxonomy=lab))
df=pd.DataFrame(rows); df.to_csv('pilot_metrics.csv',index=False)
wide=df.pivot(index='perturbation',columns='half',values=['r_abs','taxonomy'])
agree=float(np.mean(wide[('taxonomy',1)]==wide[('taxonomy',2)])); meddiff=float(np.median(np.abs(wide[('r_abs',1)].astype(float)-wide[('r_abs',2)].astype(float))))
prev=[float(np.mean(df[df.half==h].taxonomy=='metric_mirage')) for h in [1,2]]
k=int(np.sum(df.taxonomy=='metric_mirage')); n=len(df)
z=1.95996398454; ph=k/n; wilson=(ph+z*z/(2*n)-z*math.sqrt(ph*(1-ph)/n+z*z/(4*n*n)))/(1+z*z/n)
classes=sorted(df.taxonomy.unique())
f0=len(perts)>=8 and len(ctrl)>=200 and len(idx)>=1000
s1=all(x>=.25 for x in prev) and wilson>.10
s2=agree>=.8 and meddiff<=.03
s3=len(classes)>=2
res=dict(dataset_sha256=hashlib.sha256(Path(FN).read_bytes()).hexdigest(),cells=int(X.shape[0]),genes=int(X.shape[1]),control_cells=int(len(ctrl)),eligible_perturbations=len(perts),analysis_genes=len(idx),counts={k:int(v) for k,v in countmap.items()},metric_mirage_prevalence_by_half=prev,pooled_metric_mirage_k=k,pooled_n=n,wilson95_lower=wilson,label_agreement=agree,median_abs_r_change=meddiff,occupied_classes=classes,gates={'F0':f0,'S1':s1,'S2':s2,'S3':s3,'overall':f0 and s1 and s2 and s3})
Path('pilot_summary.json').write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2)); print(df.to_string(index=False))
