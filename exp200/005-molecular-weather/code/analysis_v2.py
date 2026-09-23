#!/usr/bin/env python3
import json, time
import numpy as np, pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.neural_network import MLPClassifier
from scipy.stats import wilcoxon
import scipy.sparse as sp, scipy.sparse.linalg as sla
t0=time.time(); rng=np.random.default_rng(20260923)
df=pd.read_csv('data/GSE72857_umitab.txt.gz',sep='\t',index_col=0)
print('umitab:',df.shape,flush=True)
X=df.values.T.astype(np.float32); genes=np.array(df.index)
lib=X.sum(1); lib[lib==0]=1
Xn=np.log1p(X*(1e4/lib[:,None]))
var=Xn.var(0); top=np.argsort(var)[-1000:]
Xs=Xn[:,top]
pc=PCA(n_components=20,random_state=1).fit_transform(Xs)
print('pca done',flush=True)
km=KMeans(n_clusters=12,random_state=1,n_init=10).fit(pc); lab=km.labels_
midx=[i for i,g in enumerate(genes) if g.lower() in ('cd34','kit','flt3','gata2')]
stem=Xn[:,midx].mean(1)
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
idx=np.arange(X.shape[0]); test_mask=np.zeros(X.shape[0],bool)
for k in range(12):
    ki=idx[lab==k]; test_mask[rng.choice(ki,len(ki)//2,replace=False)]=True
train=idx[~test_mask]; test=idx[test_mask]
pt_t=pt[train]; pc_t=pc[train]; lab_t=lab[train]
order_pt=np.argsort(pt_t)
def next_state_labels(src_idx, ref_pc, ref_pt, ref_lab):
    out_i=[]; out_l=[]
    for i in src_idx:
        higher=np.where(ref_pt>pt[i])[0] if src_idx is test else None
        if src_idx is not test:
            pos=np.searchsorted(ref_pt[order_pt],pt[i],'right'); higher=order_pt[pos:]
        if len(higher)==0: continue
        j=higher[np.argmin(((ref_pc[higher]-pc[i])**2).sum(1))]
        out_i.append(i); out_l.append(ref_lab[j])
    return np.array(out_i), np.array(out_l)
tr_i, tr_l = next_state_labels(train, pc_t, pt_t, lab_t)
te_i, te_l = next_state_labels(test, pc_t, pt_t, lab_t)
print('labels: train',len(tr_i),'test',len(te_i),flush=True)
# Markov baseline (v1)
T=np.ones((12,12))
tr_pos={c:r for r,c in enumerate(train)}
for i,l in zip(tr_i,tr_l): T[lab[i],l]+=1
T=T/T.sum(1,keepdims=True)
stat=T.mean(0)
# MLP (v2 arm)
mlp=MLPClassifier(hidden_layer_sizes=(64,32),max_iter=300,random_state=20260923)
mlp.fit(pc[tr_i],tr_l)
print('mlp trained, iters',mlp.n_iter_,flush=True)
proba=mlp.predict_proba(pc[te_i])
cls=list(mlp.classes_)
def proba_nll(Pm,classes,truth):
    cidx={c:k for k,c in enumerate(classes)}
    return np.array([-np.log(Pm[r,cidx[t]]+1e-9) for r,t in enumerate(truth)])
nll_mlp=proba_nll(proba,cls,te_l)
pred=cls[np.argmax(proba,1)]; acc_mlp=float(np.mean(pred==te_l))
nll_mk=np.array([-np.log(T[lab[i],t]+1e-9) for i,t in zip(te_i,te_l)])
acc_mk=float(np.mean([np.argmax(T[lab[i]])==t for i,t in zip(te_i,te_l)]))
nll_cl=np.array([-np.log(stat[t]+1e-9) for t in te_l])
acc_cl=float(np.mean(np.argmax(stat)==te_l))
w1=wilcoxon(nll_mlp,nll_cl,alternative='less')
w2=wilcoxon(nll_mk,nll_cl,alternative='less')
g1b=bool(w1.pvalue<=0.01 and acc_mlp>=1.5*acc_cl)
g1=bool(w2.pvalue<=0.01 and acc_mk>=1.5*acc_cl)
# horizon curve (v1 G2)
T2=T@T; T3=T2@T
n2=np.array([-np.log(T2[lab[i],t]+1e-9) for i,t in zip(te_i,te_l)])
n3=np.array([-np.log(T3[lab[i],t]+1e-9) for i,t in zip(te_i,te_l)])
g2=bool(n2.mean()<nll_cl.mean() and n3.mean()<nll_cl.mean())
import joblib
joblib.dump(dict(mlp=mlp,pca_genes=genes[top].tolist(),n_top=1000),'results/fate_forecast_model.joblib')
pd.DataFrame(T).to_csv('results/transition_matrix.csv')
pd.DataFrame(dict(step=['1-step','2-step','3-step'],markov_nll=[nll_mk.mean(),n2.mean(),n3.mean()],climatology_nll=[nll_cl.mean()]*3)).to_csv('results/horizon_curve.csv',index=False)
summary=dict(n_cells=int(X.shape[0]),n_train=int(len(tr_i)),n_eval=int(len(te_l)),
  G1b_MLP=dict(nll=float(nll_mlp.mean()),top1=acc_mlp,wilcoxon_p_vs_clim=float(w1.pvalue),PASS=g1b),
  G1_Markov=dict(nll=float(nll_mk.mean()),top1=acc_mk,wilcoxon_p_vs_clim=float(w2.pvalue),PASS=g1),
  G3_head2head=dict(mlp_nll=float(nll_mlp.mean()),markov_nll=float(nll_mk.mean()),mlp_top1=acc_mlp,markov_top1=acc_mk),
  climatology=dict(nll=float(nll_cl.mean()),top1=acc_cl),
  G2_horizon=dict(step2=float(n2.mean()),step3=float(n3.mean()),PASS=g2),
  runtime_min=(time.time()-t0)/60)
json.dump(summary,open('results/gate_summary.json','w'),indent=2)
print(json.dumps(summary,indent=2),flush=True)
