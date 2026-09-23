#!/usr/bin/env python3
import json, time
import numpy as np, pandas as pd, h5py, scipy.sparse as sp
from scipy.stats import pearsonr
t0=time.time(); rng=np.random.default_rng(20260923)
f=h5py.File('data/visium.h5','r'); m=f['matrix']
barcodes=[b.decode() for b in m['barcodes'][:]]
feat=[g.decode() for g in m['features']['name'][:]]
M=sp.csc_matrix((m['data'][:],m['indices'][:],m['indptr'][:]),shape=(len(feat),len(barcodes))).T.tocsr()
pos=pd.read_csv('data/spatial/tissue_positions_list.csv',header=None,names=['barcode','in_tissue','row','col','px','py'])
pos=pos[pos.in_tissue==1].set_index('barcode')
keep=[i for i,b in enumerate(barcodes) if b in pos.index]; bcs=[barcodes[i] for i in keep]
M=M[keep]; lib=np.asarray(M.sum(1)).ravel(); lib[lib==0]=1
N=M.multiply(1e4/lib[:,None]).tocsr().log1p()
mu=np.asarray(N.mean(0)).ravel()
rc=pos.loc[bcs][['row','col']].values
posmap={(r,c):i for i,(r,c) in enumerate(rc)}
n=M.shape[0]
W=sp.lil_matrix((n,n),dtype=np.float32)
for i,(r,c) in enumerate(rc):
    for dr,dc in ((0,2),(0,-2),(1,1),(1,-1),(-1,1),(-1,-1)):
        j=posmap.get((r+dr,c+dc))
        if j is not None: W[i,j]=1
W=(W+W.T).tocsr(); W.data[:]=1
W2=(W+W@W); W2.setdiag(0); W2.eliminate_zeros(); W2.data[:]=1
fidx={g:i for i,g in enumerate(feat)}
cache={}
def gvec(g):
    if g not in cache: cache[g]=N[:,fidx[g]].toarray().ravel()
    return cache[g]
def nm(v,Wm):
    s=np.asarray(Wm.sum(1)).ravel(); s[s==0]=1
    return (Wm@v)/s
LR="CCL2-CCR2 CCL5-CCR5 CXCL12-CXCR4 CXCL9-CXCR3 CXCL10-CXCR3 CXCL11-CXCR3 CCL19-CCR7 CCL21-CCR7 CXCL13-CXCR5 CCL17-CCR4 CCL22-CCR4 TGFB1-TGFBR1 TGFB1-TGFBR2 IL6-IL6R IL6-IL6ST TNF-TNFRSF1A TNF-TNFRSF1B IFNG-IFNGR1 IFNG-IFNGR2 IL1B-IL1R1 IL1A-IL1R1 CSF1-CSF1R IL34-CSF1R VEGFA-KDR VEGFA-FLT1 VEGFB-FLT1 PGF-FLT1 ANGPT1-TEK ANGPT2-TEK EGF-EGFR TGFA-EGFR AREG-EGFR HGF-MET FGF2-FGFR1 FGF7-FGFR2 PDGFB-PDGFRB PDGFA-PDGFRA SPP1-ITGAV SPP1-CD44 LGALS9-HAVCR2 CD274-PDCD1 PDCD1LG2-PDCD1 CD80-CTLA4 CD86-CTLA4 CD40-CD40LG MIF-CD74 MDK-LRP1 SEMA3C-NRP1".split()
lig_dec={}; rec_dec={}
allm=mu  # per-gene mean over spots
dec=lambda g: int(min(9, np.searchsorted(np.quantile(allm,np.linspace(0,1,11)), allm[fidx[g]], 'right')-1))
def matched_null(n_pairs, Wm):
    out=[]
    deciles=np.digitize(allm, np.quantile(allm,np.linspace(0,1,11))[1:-1])
    by_dec={d: np.where(deciles==d)[0] for d in range(10)}
    ligs=[l for l,_ in (p.split('-') for p in LR) if l in fidx]
    recs=[r for _,r in (p.split('-') for p in LR) if r in fidx]
    ld=[deciles[fidx[l]] for l in ligs]; rd=[deciles[fidx[r]] for r in recs]
    for _ in range(n_pairs):
        a=rng.integers(0,len(feat)); b=rng.integers(0,len(feat))
        va=gvec(feat[a]); vb=nm(gvec(feat[b]),Wm)
        if va.std()<1e-9 or vb.std()<1e-9: continue
        out.append(pearsonr(va,vb)[0])
    return np.array(out)
def lr_scores(Wm):
    sc={}
    for p in LR:
        l,r=p.split('-')
        if l not in fidx or r not in fidx: continue
        lv=gvec(l); rv=nm(gvec(r),Wm)
        if lv.std()<1e-9 or rv.std()<1e-9: sc[p]=np.nan; continue
        sc[p]=pearsonr(lv,rv)[0]
    return sc
def decile_matched_null(Wm, seed_off=0):
    rng2=np.random.default_rng(99+seed_off)
    lig_decs=set(); rec_decs=set()
    for p in LR:
        l,r=p.split('-')
        if l in fidx: lig_decs.add(deciles_g[fidx[l]])
        if r in fidx: rec_decs.add(deciles_g[fidx[r]])
    pool_l=[i for i in range(len(feat)) if deciles_g[i] in lig_decs]
    pool_r=[i for i in range(len(feat)) if deciles_g[i] in rec_decs]
    out=[]
    for _ in range(500):
        a=pool_l[rng2.integers(0,len(pool_l))]; b=pool_r[rng2.integers(0,len(pool_r))]
        va=gvec(feat[a]); vb=nm(gvec(feat[b]),Wm)
        if va.std()<1e-9 or vb.std()<1e-9: continue
        out.append(pearsonr(va,vb)[0])
    return np.array(out)
deciles_g=np.digitize(mu, np.quantile(mu,np.linspace(0,1,11))[1:-1])
for name,Wm in [('1hop',W),('2hop',W2)]:
    sc=lr_scores(Wm)
    null=decile_matched_null(Wm)
    med=float(np.nanmedian(list(sc.values()))); q95=float(np.quantile(null,0.95))
    pd.DataFrame(dict(pair=list(sc),score=list(sc.values()))).to_csv(f'results/lr_scores_{name}_matched.csv',index=False)
    pd.DataFrame(dict(random=null)).to_csv(f'results/random_{name}_matched.csv',index=False)
    print(json.dumps(dict(hop=name, lr_median=med, matched_null_q95=q95, PASS=med>q95, n_pairs=len(sc))), flush=True)
print('runtime_min', (time.time()-t0)/60, flush=True)
