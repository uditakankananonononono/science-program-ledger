#!/usr/bin/env python3
"""score_spage.py - SpaGE kNN baseline (Abdelaal 2020): 30 PVs from reference, kNN k=50 cosine, weighted mean. Leave-one-gene-out over 32 shared genes."""
import json, numpy as np
from scipy.stats import spearmanr
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
S=np.load('results/local/spatial.npz',allow_pickle=True)
R=np.load('results/local/reference.npz',allow_pickle=True)
sgenes=list(S['genes']); rgenes=list(R['genes'])
shared=list(R['genes'])
Sidx=[sgenes.index(g) for g in shared]
SM=S['M'][Sidx,:].T  # cells x 32
RM=R['R']            # ref cells x 32
pca=PCA(n_components=30,random_state=7).fit(RM)
Zr=normalize(pca.transform(RM)); Zs=normalize(pca.transform(SM))
def knn_impute(target_ref):
    # cosine sim (normalized) -> k=50 nearest, distance-weighted
    sim=Zs@Zr.T
    out=np.zeros(Zs.shape[0],dtype=np.float32)
    k=50
    idx=np.argpartition(-sim,k-1,axis=1)[:,:k]
    for i in range(Zs.shape[0]):
        w=sim[i,idx[i]]; w=(w-w.min())+1e-6
        out[i]=(w*target_ref[idx[i]]).sum()/w.sum()
    return out
res={}
split=json.load(open('results/gene_split.json'))
for gene in shared:
    ti=rgenes.index(gene); si=sgenes.index(gene)
    imp=knn_impute(RM[:,ti])
    meas=SM[:,shared.index(gene)]
    rho=float(spearmanr(meas,imp).statistic)
    res[gene]=rho
    print(gene,round(rho,3),flush=True)
out={s:float(np.mean([res[g] for g in split[s]])) for s in ['dev','frozen']}
out['per_gene']=res
json.dump(out,open('results/spage_scores.json','w'),indent=1)
print('SPAGE dev',round(out['dev'],4),'frozen',round(out['frozen'],4))
