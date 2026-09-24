#!/usr/bin/env python3
"""impute_gene.py GENE - impute a shared panel gene's spatial map with the SpaGE kNN method
(the winning arm of DOC-1-021: SpaGE dev 0.678 / frozen 0.698 mean Spearman; tiny CPU DDPM
boundary documented in REPORT.md). Prints per-gene Spearman vs measured (leave-one-out benchmark)."""
import sys, json, numpy as np
from scipy.stats import spearmanr
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
gene=sys.argv[1]
S=np.load('results/local/spatial.npz',allow_pickle=True)
R=np.load('results/local/reference.npz',allow_pickle=True)
sgenes=list(S['genes']); shared=list(R['genes'])
assert gene in shared, f'{gene} not in shared panel ({len(shared)} genes)'
Sidx=[sgenes.index(g) for g in shared]
SM=S['M'][Sidx,:].T; RM=R['R']
pca=PCA(n_components=30,random_state=7).fit(RM)
Zr=normalize(pca.transform(RM)); Zs=normalize(pca.transform(SM))
sim=Zs@Zr.T; k=50
idx=np.argpartition(-sim,k-1,axis=1)[:,:k]
ti=shared.index(gene); out=np.zeros(Zs.shape[0])
for i in range(Zs.shape[0]):
    w=sim[i,idx[i]]; w=(w-w.min())+1e-6
    out[i]=(w*RM[idx[i],ti]).sum()/w.sum()
meas=SM[:,ti]
rho=float(spearmanr(meas,out).statistic)
print(json.dumps({'gene':gene,'spearman_vs_measured':round(rho,3),'n_cells':int(len(out)),
 'imputed_mean':round(float(out.mean()),3),'measured_mean':round(float(meas.mean()),3)},indent=1))
