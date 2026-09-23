#!/usr/bin/env python3
"""DOC-1-003 tool: Moran's I + technical-covariate audit for any 10x Visium filtered matrix.
Usage: visium_spatial_tool.py --h5 <filtered_feature_bc_matrix.h5> --positions <tissue_positions_list.csv> [--out out.csv]
Outputs per-gene Moran's I, mean, dropout, and the ridge R^2 of covariates->Moran's I
(train/test split) so users can see how much of their 'spatial pattern' is technical."""
import argparse, numpy as np, pandas as pd, h5py, scipy.sparse as sp
from sklearn.linear_model import Ridge
p=argparse.ArgumentParser(); p.add_argument('--h5',required=True); p.add_argument('--positions',required=True); p.add_argument('--out',default='morans_audit.csv'); a=p.parse_args()
f=h5py.File(a.h5,'r'); m=f['matrix']
barcodes=[b.decode() for b in m['barcodes'][:]]
feat=[g.decode() for g in m['features']['name'][:]]
M=sp.csc_matrix((m['data'][:],m['indices'][:],m['indptr'][:]),shape=(len(feat),len(barcodes))).T.tocsr()
pos=pd.read_csv(a.positions,header=None,names=['barcode','in_tissue','row','col','px','py'])
pos=pos[pos.in_tissue==1].set_index('barcode')
keep=[i for i,b in enumerate(barcodes) if b in pos.index]; bcs=[barcodes[i] for i in keep]
M=M[keep]; lib=np.asarray(M.sum(1)).ravel(); lib[lib==0]=1
N=M.multiply(1e4/lib[:,None]).tocsr().log1p()
mu=np.asarray(N.mean(0)).ravel(); m2=np.asarray(N.multiply(N).mean(0)).ravel(); var=m2-mu**2
top=np.argsort(var)[-1000:]
X=N[:,top].toarray().astype(np.float32); genes=np.array(feat)[top]
n=X.shape[0]
rc=pos.loc[bcs][['row','col']].values; pm={(r,c):i for i,(r,c) in enumerate(rc)}
W=sp.lil_matrix((n,n),dtype=np.float32)
for i,(r,c) in enumerate(rc):
    for dr,dc in ((0,2),(0,-2),(1,1),(1,-1),(-1,1),(-1,-1)):
        j=pm.get((r+dr,c+dc))
        if j is not None: W[i,j]=1
W=(W+W.T).tocsr(); W.data[:]=1
Xc=X-X.mean(0); den=(Xc**2).sum(0); den[den==0]=1e-9
I=(n/W.sum())*(Xc*(W@Xc)).sum(0)/den
F=np.c_[X.mean(0),(X==0).mean(0)]
rng=np.random.default_rng(1); s=rng.permutation(len(genes)); tr,te=s[:500],s[500:]
r_=Ridge(alpha=1.0).fit(F[tr],I[tr]); pred=r_.predict(F[te])
from scipy.stats import pearsonr
r=pearsonr(pred,I[te])[0]
pd.DataFrame(dict(gene=genes,morans_i=I,mean=F[:,0],dropout=F[:,1])).to_csv(a.out,index=False)
print(f'wrote {a.out}; covariates->MoransI held-out r = {r:.3f} (>=0.5: spatial calls need technical-covariate control)')
