#!/usr/bin/env python3
import json, time
import numpy as np, pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.stats import wilcoxon
t0=time.time(); rng=np.random.default_rng(20260923)
df=pd.read_csv('data/GSE72857_umitab.txt.gz',sep='\t',index_col=0)
print('umitab:',df.shape,flush=True)
X=df.values.T.astype(np.float32)  # cells x genes
genes=np.array(df.index)
lib=X.sum(1); lib[lib==0]=1
Xn=np.log1p(X*(1e4/lib[:,None]))
mu=Xn.mean(0); var=Xn.var(0)
top=np.argsort(var)[-1000:]
Xs=Xn[:,top]
pc=PCA(n_components=20,random_state=1).fit_transform(Xs)
km=KMeans(n_clusters=12,random_state=1,n_init=10).fit(pc)
lab=km.labels_
# stemness root (pre-registered markers, frozen)
markers=[g for g in genes if g.lower() in ('cd34','kit','flt3','gata2')]
midx=[i for i,g in enumerate(genes) if g.lower() in ('cd34','kit','flt3','gata2')]
stem=Xn[:,midx].mean(1)
root=int(np.argmax([stem[lab==k].mean() for k in range(12)]))
print('root cluster:',root,flush=True)
# diffusion pseudotime on PCA kNN graph
from sklearn.neighbors import NearestNeighbors
import scipy.sparse as sp
nn=NearestNeighbors(n_neighbors=15).fit(pc)
A=nn.kneighbors_graph(pc,mode='distance')
sig=np.median(A.data)+1e-9
A.data=np.exp(-A.data**2/(2*sig**2))
A=(A+A.T).tocsr(); A.data[:]=np.maximum(A.data,1e-12)
d=np.asarray(A.sum(1)).ravel()
P=sp.diags(1/d)@A
# diffusion map: eigenvectors of P (top 10, power iterate via dense small eigh on normalized)
import scipy.sparse.linalg as sla
vals,vecs=sla.eigs(P.T.astype(np.float64),k=6,which='LM')
vecs=np.real(vecs); vals=np.real(vals)
order=np.argsort(-vals)
dpt=vecs[:,order[1]]  # first nontrivial component
# orient: root cluster should be LOW pseudotime
if dpt[lab==root].mean()>dpt.mean(): dpt=-dpt
pt=(dpt-dpt.min())/(dpt.max()-dpt.min())
# train/test split stratified
idx=np.arange(X.shape[0])
test_mask=np.zeros(X.shape[0],bool)
for k in range(12):
    ki=idx[lab==k]; test_mask[rng.choice(ki,len(ki)//2,replace=False)]=True
train=idx[~test_mask]; test=idx[test_mask]
# transitions: for each train cell, its nearest train neighbor at HIGHER pseudotime
pt_t=pt[train]; pc_t=pc[train]; lab_t=lab[train]
order_pt=np.argsort(pt_t)
T=np.ones((12,12))  # Laplace
for i in range(len(train)):
    higher=order_pt[np.searchsorted(pt_t[order_pt],pt_t[i],'right'):]
    if len(higher)==0: continue
    j=higher[np.argmin(((pc_t[higher]-pc_t[i])**2).sum(1))]
    T[lab_t[i],lab_t[j]]+=1
T=T/T.sum(1,keepdims=True)
stat=T.mean(0)  # climatology ~ mean outgoing dist
# evaluation: for each test cell, true next-state = state of its nearest TRAIN neighbor at higher pt
nn2=NearestNeighbors(n_neighbors=1).fit(pc_t)
nll_m=[]; nll_b=[]; top1_m=0; top1_b=0
for i in test:
    higher=np.where(pt_t>pt[i])[0]
    if len(higher)==0: continue
    j=higher[np.argmin(((pc_t[higher]-pc[i])**2).sum(1))]
    true_state=lab_t[j]
    s=lab[i]
    pm=T[s]+1e-9; pb=stat+1e-9
    nll_m.append(-np.log(pm[true_state])); nll_b.append(-np.log(pb[true_state]))
    top1_m+=int(np.argmax(pm)==true_state); top1_b+=int(np.argmax(pb)==true_state)
nll_m=np.array(nll_m); nll_b=np.array(nll_b)
w=wilcoxon(nll_m,nll_b,alternative='less')
acc_m=top1_m/len(nll_m); acc_b=top1_b/len(nll_b)
g1=bool(w.pvalue<=0.01 and acc_m>=1.5*acc_b)
# G2: horizon curve 2-step, 3-step
T2=T@T; T3=T2@T
def step_nll(Tm):
    out=[]
    for i in test:
        higher=np.where(pt_t>pt[i])[0]
        if len(higher)==0: continue
        j=higher[np.argmin(((pc_t[higher]-pc[i])**2).sum(1))]
        out.append(-np.log(Tm[lab[i]][lab_t[j]]+1e-9))
    return np.array(out)
n2=step_nll(T2); n3=step_nll(T3)
nb=nll_b[:len(n2)] if len(nll_b)!=len(n2) else nll_b
g2=bool(n2.mean()<nb.mean() and n3.mean()<nb.mean())
pd.DataFrame(T).to_csv('results/transition_matrix.csv')
pd.DataFrame(dict(step=['1-step','2-step','3-step'],model_nll=[nll_m.mean(),n2.mean(),n3.mean()],baseline_nll=[nb.mean()]*3)).to_csv('results/horizon_curve.csv',index=False)
np.save('results/pseudotime.npy',pt)
summary=dict(n_cells=int(X.shape[0]),n_eval=int(len(nll_m)),
  G1=dict(model_nll=float(nll_m.mean()),baseline_nll=float(nll_b.mean()),wilcoxon_p=float(w.pvalue),top1_model=float(acc_m),top1_baseline=float(acc_b),PASS=g1),
  G2=dict(step2_nll=float(n2.mean()),step3_nll=float(n3.mean()),baseline=float(nb.mean()),PASS=g2),
  runtime_min=(time.time()-t0)/60)
json.dump(summary,open('results/gate_summary.json','w'),indent=2)
print(json.dumps(summary,indent=2),flush=True)
