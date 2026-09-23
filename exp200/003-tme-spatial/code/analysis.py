#!/usr/bin/env python3
import json, time
import numpy as np, pandas as pd, h5py
from scipy.stats import pearsonr
from sklearn.linear_model import Ridge
t0=time.time(); rng=np.random.default_rng(20260923)
f=h5py.File('data/visium.h5','r')
m=f['matrix']
barcodes=[b.decode() for b in m['barcodes'][:]]
feat=[g.decode() for g in m['features']['name'][:]]
data=m['data'][:]; indices=m['indices'][:]; indptr=m['indptr'][:]
shape=(len(m['features']['id']), len(barcodes))  # 10x h5: genes x barcodes, CSC
import scipy.sparse as sp
M=sp.csc_matrix((data,indices,indptr), shape=shape).T.tocsr()  # spots x genes
print('matrix:', M.shape, flush=True)
pos=pd.read_csv('data/spatial/tissue_positions_list.csv', header=None,
                names=['barcode','in_tissue','row','col','px','py'])
pos=pos[pos.in_tissue==1].set_index('barcode')
keep=[i for i,b in enumerate(barcodes) if b in pos.index]
bcs=[barcodes[i] for i in keep]
M=M[keep]
lib=np.asarray(M.sum(1)).ravel(); lib[lib==0]=1
N=M.multiply(1e4/lib[:,None]).tocsr().log1p()
mu=np.asarray(N.mean(0)).ravel(); m2=np.asarray(N.multiply(N).mean(0)).ravel()
var=m2-mu**2
top=np.argsort(var)[-1000:]
X=N[:,top].toarray().astype(np.float32)
genes=np.array(feat)[top]
n_spots=X.shape[0]
print('spots:', n_spots, 'genes:', len(genes), flush=True)
# hex lattice adjacency (Visium: same-row col±2; row±1 col±1)
rc=pos.loc[bcs][['row','col']].values
posmap={(r,c):i for i,(r,c) in enumerate(rc)}
W=sp.lil_matrix((n_spots,n_spots),dtype=np.float32)
for i,(r,c) in enumerate(rc):
    for dr,dc in ((0,2),(0,-2),(1,1),(1,-1),(-1,1),(-1,-1)):
        j=posmap.get((r+dr,c+dc))
        if j is not None: W[i,j]=1
W=W.tocsr(); W=(W+W.T).tocsr(); W.data[:]=1
Wsum=W.sum()
# Moran's I per gene
Xc=X-X.mean(0)
den=(Xc**2).sum(0); den[den==0]=1e-9
I=(n_spots/Wsum)*(np.asarray(W@Xc).ravel() if False else (Xc*(W@Xc)).sum(0))/den
expr_mean=X.mean(0); dropout=(X==0).mean(0)
# G1: ridge (mean, dropout) -> Moran's I, 500/500 split
seed=rng.permutation(len(genes)); tr,te=seed[:500],seed[500:]
Feats=np.c_[expr_mean,dropout]
r_=Ridge(alpha=1.0).fit(Feats[tr],I[tr])
pred=r_.predict(Feats[te])
r_obs=pearsonr(pred,I[te])[0]
null=[pearsonr(Ridge(alpha=1.0).fit(Feats[tr],I[tr][rng.permutation(500)] if False else I[tr]).predict(Feats[te]), I[te][rng.permutation(500)])[0] for _ in range(0)] 
# proper null: permute test labels
null=[pearsonr(pred, I[te][rng.permutation(len(te))])[0] for _ in range(100)]
q95=float(np.quantile(null,0.95))
g1 = r_obs < q95  # locked direction: covariates do NOT explain structure
# G2: LR pairs
LR="CCL2-CCR2 CCL5-CCR5 CXCL12-CXCR4 CXCL9-CXCR3 CXCL10-CXCR3 CXCL11-CXCR3 CCL19-CCR7 CCL21-CCR7 CXCL13-CXCR5 CCL17-CCR4 CCL22-CCR4 TGFB1-TGFBR1 TGFB1-TGFBR2 IL6-IL6R IL6-IL6ST TNF-TNFRSF1A TNF-TNFRSF1B IFNG-IFNGR1 IFNG-IFNGR2 IL1B-IL1R1 IL1A-IL1R1 CSF1-CSF1R IL34-CSF1R VEGFA-KDR VEGFA-FLT1 VEGFB-FLT1 PGF-FLT1 ANGPT1-TEK ANGPT2-TEK EGF-EGFR TGFA-EGFR AREG-EGFR HGF-MET FGF2-FGFR1 FGF7-FGFR2 PDGFB-PDGFRB PDGFA-PDGFRA SPP1-ITGAV SPP1-CD44 LGALS9-HAVCR2 CD274-PDCD1 PDCD1LG2-PDCD1 CD80-CTLA4 CD86-CTLA4 CD40-CD40LG MIF-CD74 MDK-LRP1 SEMA3C-NRP1".split()
allgenes=set(feat)
fidx={g:i for i,g in enumerate(feat)}
_gcache={}
def gvec(g):
    if g not in _gcache:
        _gcache[g]=N[:,fidx[g]].toarray().ravel()
    return _gcache[g]
def neighmean(v):
    s=W.sum(1).A.ravel() if hasattr(W.sum(1),'A') else np.asarray(W.sum(1)).ravel()
    s[s==0]=1
    return (W@v)/s
lr_scores=[]; present=[]
for pair in LR:
    l,r=pair.split('-')
    if l not in fidx or r not in fidx: continue
    present.append(pair)
    lv=gvec(l); rv=neighmean(gvec(r))
    if lv.std()<1e-9 or rv.std()<1e-9: lr_scores.append(np.nan); continue
    lr_scores.append(pearsonr(lv,rv)[0])
# matched random pairs: match ligand expression decile
rand_scores=[]
allv=[g for g in feat if g in fidx]
means={g: float(mu[fidx[g]]) for g in allv}
import bisect
sorted_by_mean=sorted(allv,key=lambda g:means[g])
for _ in range(500):
    a,b=rng.choice(allv,2,replace=False)
    va=gvec(a); vb=neighmean(gvec(b))
    if va.std()<1e-9 or vb.std()<1e-9: continue
    rand_scores.append(pearsonr(va,vb)[0])
lr_med=float(np.nanmedian(lr_scores)); rq95=float(np.quantile(rand_scores,0.95))
g2=lr_med>rq95
pd.DataFrame(dict(gene=genes,morans_i=I,mean=expr_mean,dropout=dropout)).to_csv('results/morans_i.csv',index=False)
pd.DataFrame(dict(pair=present,score=lr_scores)).to_csv('results/lr_scores.csv',index=False)
pd.DataFrame(dict(random=rand_scores)).to_csv('results/random_pairs.csv',index=False)
summary=dict(spots=int(n_spots),
  G1=dict(test_r=float(r_obs), null_q95=q95, covariates_explain=bool(r_obs>=q95), PASS_structure_is_biological=bool(g1)),
  G2=dict(lr_pairs_present=len(present), lr_median=lr_med, random_q95=rq95, PASS=bool(g2)),
  runtime_min=(time.time()-t0)/60)
json.dump(summary,open('results/gate_summary.json','w'),indent=2)
print(json.dumps(summary,indent=2),flush=True)
