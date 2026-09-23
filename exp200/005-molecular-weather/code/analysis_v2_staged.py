#!/usr/bin/env python3
# Staged version of analysis_v2.py: reads pre-parsed intermediates from /tmp
# (X_norm_top1000.npy = CPM+log1p on top-1000 variable genes; lib.npy; chunks for markers).
import json, time
import numpy as np, pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.neural_network import MLPClassifier
from scipy.stats import wilcoxon
import scipy.sparse as sp, scipy.sparse.linalg as sla
t0=time.time(); rng=np.random.default_rng(20260923)
Xs=np.load('/tmp/X_norm_top1000.npy'); lib=np.load('/tmp/lib.npy'); top=np.load('/tmp/top_genes_idx.npy')
genes=pd.read_csv('/tmp/genes.txt',header=None)[0].values
print('X',Xs.shape,flush=True)
pc=PCA(n_components=20,random_state=1).fit_transform(Xs)
print('pca done',flush=True)
km=KMeans(n_clusters=12,random_state=1,n_init=10).fit(pc); lab=km.labels_
# stemness from raw chunks (markers may not be in top1000)
mset={'cd34','kit','flt3','gata2'}
midx=np.array([i for i,g in enumerate(genes) if str(g).lower() in mset])
print('marker rows:',genes[midx].tolist(),flush=True)
stem=np.zeros(Xs.shape[0],np.float32)
for c in range(3):
    A=np.load(f'/tmp/chunk{c}.npy',mmap_mode='r')
    r0=c*10000; r1=r0+A.shape[0]
    rows=midx[(midx>=r0)&(midx<r1)]-r0
    if len(rows):
        for j in range(0,10368,2000):
            stem[j:j+2000]+=np.log1p(A[rows][:,j:j+2000]*(1e4/lib[None,j:j+2000])).sum(0)
stem/=max(len(midx),1)
root=int(np.argmax([stem[lab==k].mean() for k in range(12)]))
nn=NearestNeighbors(n_neighbors=15).fit(pc)
A=nn.kneighbors_graph(pc,mode='distance')
sig=np.median(A.data)+1e-9; A.data=np.exp(-A.data**2/(2*sig**2))
A=(A+A.T).tocsr(); A.data[:]=np.maximum(A.data,1e-12)
d=np.asarray(A.sum(1)).ravel(); P=sp.diags(1/d)@A
vals,vecs=sla.eigs(P.T.astype(np.float64),k=6,which='LM')
vecs=np.real(vecs); vals=np.real(vals)
dpt=vecs[:,np.argsort(-vals)[1]]
if dpt[lab==root].mean()>dpt.mean(): dpt=-dpt
pt=(dpt-dpt.min())/(dpt.max()-dpt.min())
print('pseudotime done, root cluster',root,flush=True)
idx=np.arange(Xs.shape[0]); test_mask=np.zeros(Xs.shape[0],bool)
for k in range(12):
    ki=idx[lab==k]; test_mask[rng.choice(ki,len(ki)//2,replace=False)]=True
train=idx[~test_mask]; test=idx[test_mask]
pt_t=pt[train]; pc_t=pc[train]; lab_t=lab[train]
order_pt=np.argsort(pt_t)
def next_labels(src):
    out_i=[]; out_l=[]
    for i in src:
        if src is test: higher=np.where(pt_t>pt[i])[0]
        else:
            pos=np.searchsorted(pt_t[order_pt],pt[i],'right'); higher=order_pt[pos:]
        if len(higher)==0: continue
        j=higher[np.argmin(((pc_t[higher]-pc[i])**2).sum(1))]
        out_i.append(i); out_l.append(lab_t[j])
    return np.array(out_i),np.array(out_l)
tr_i,tr_l=next_labels(train); te_i,te_l=next_labels(test)
print('labels train',len(tr_i),'test',len(te_i),flush=True)
T=np.ones((12,12))
for i,l in zip(tr_i,tr_l): T[lab[i],l]+=1
T=T/T.sum(1,keepdims=True); stat=T.mean(0)
mlp=MLPClassifier(hidden_layer_sizes=(64,32),max_iter=300,random_state=20260923)
mlp.fit(pc[tr_i],tr_l)
print('mlp trained, iters',mlp.n_iter_,flush=True)
proba=mlp.predict_proba(pc[te_i]); cls=list(mlp.classes_)
cidx={c:k for k,c in enumerate(cls)}
nll_mlp=np.array([-np.log(proba[r,cidx[t]]+1e-9) for r,t in enumerate(te_l)])
acc_mlp=float(np.mean([cls[k] for k in np.argmax(proba,1)]==te_l))
nll_mk=np.array([-np.log(T[lab[i],t]+1e-9) for i,t in zip(te_i,te_l)])
acc_mk=float(np.mean([np.argmax(T[lab[i]])==t for i,t in zip(te_i,te_l)]))
nll_cl=np.array([-np.log(stat[t]+1e-9) for t in te_l])
acc_cl=float(np.mean(np.argmax(stat)==te_l))
w1=wilcoxon(nll_mlp,nll_cl,alternative='less'); w2=wilcoxon(nll_mk,nll_cl,alternative='less')
g1b=bool(w1.pvalue<=0.01 and acc_mlp>=1.5*acc_cl); g1=bool(w2.pvalue<=0.01 and acc_mk>=1.5*acc_cl)
T2=T@T; T3=T2@T
n2=np.array([-np.log(T2[lab[i],t]+1e-9) for i,t in zip(te_i,te_l)])
n3=np.array([-np.log(T3[lab[i],t]+1e-9) for i,t in zip(te_i,te_l)])
g2=bool(n2.mean()<nll_cl.mean() and n3.mean()<nll_cl.mean())
import joblib
joblib.dump(dict(mlp=mlp,top_gene_idx=top.tolist()),'results/fate_forecast_model.joblib')
pd.DataFrame(T).to_csv('results/transition_matrix.csv')
pd.DataFrame(dict(step=['1-step','2-step','3-step'],markov_nll=[nll_mk.mean(),n2.mean(),n3.mean()],climatology_nll=[nll_cl.mean()]*3)).to_csv('results/horizon_curve.csv',index=False)
np.save('results/pseudotime.npy',pt)
summary=dict(n_cells=int(Xs.shape[0]),n_train=int(len(tr_i)),n_eval=int(len(te_l)),
  G1b_MLP=dict(nll=float(nll_mlp.mean()),top1=acc_mlp,wilcoxon_p_vs_clim=float(w1.pvalue),PASS=g1b),
  G1_Markov=dict(nll=float(nll_mk.mean()),top1=acc_mk,wilcoxon_p_vs_clim=float(w2.pvalue),PASS=g1),
  G3_head2head=dict(mlp_nll=float(nll_mlp.mean()),markov_nll=float(nll_mk.mean()),mlp_top1=acc_mlp,markov_top1=acc_mk),
  climatology=dict(nll=float(nll_cl.mean()),top1=acc_cl),
  G2_horizon=dict(step2=float(n2.mean()),step3=float(n3.mean()),PASS=g2),
  runtime_min=(time.time()-t0)/60)
json.dump(summary,open('results/gate_summary.json','w'),indent=2)
print(json.dumps(summary,indent=2),flush=True)
