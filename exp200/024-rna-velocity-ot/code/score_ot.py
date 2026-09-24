import numpy as np, json, sys
sys.path.insert(0,'code')
from flows import cluster_flow, score
import scanpy as sc, anndata
from sklearn.neighbors import NearestNeighbors

LAM=float(sys.argv[1]) if len(sys.argv)>1 else 1.0
TAG=sys.argv[2] if len(sys.argv)>2 else 'dev'
sfx='' if TAG=='dev' else '_frozen'
X=np.load(f'results/local/X_hvg{sfx}.npy'); V=np.load(f'results/local/velocity{sfx}.npy')
labels=np.load(f'results/local/labels{sfx}.npy', allow_pickle=True)
edges=json.load(open(f'results/canonical_edges{sfx}.json'))
# DPT pseudotime
print('stage: dpt', flush=True)
ad=anndata.AnnData(X=X)
sc.pp.pca(ad, n_comps=30, random_state=7)
sc.pp.neighbors(ad, n_neighbors=30, n_pcs=30, random_state=7)
sc.tl.diffmap(ad)
root_cluster='Ductal' if TAG=='dev' else 'Radial Glia-like'
duct=np.where(labels==root_cluster)[0]
cent=ad.obsm['X_pca'][duct].mean(0)
root=duct[np.argmin(((ad.obsm['X_pca'][duct]-cent)**2).sum(1))]
ad.uns['iroot']=root
sc.tl.dpt(ad)
dpt=ad.obs['dpt_pseudotime'].values
bins=np.minimum((dpt/ (dpt.max()+1e-9) * 50).astype(int), 49)
# sinkhorn between consecutive bins
def sinkhorn(C, eps=0.05, iters=200):
    C=(C-C.mean())/ (C.std()+1e-9)
    K=np.exp(-C/eps)
    u=np.ones(K.shape[0])/K.shape[0]; v=np.ones(K.shape[1])/K.shape[1]
    a=np.ones(K.shape[0]); b=np.ones(K.shape[1])
    for _ in range(iters):
        a=1.0/np.maximum(K@b,1e-12); b=1.0/np.maximum(K.T@a,1e-12)
    return (a[:,None]*K)*b[None,:] / K.shape[0]
n=len(X)
Fmass=np.zeros((n,n), np.float32)
Xn=X/ (np.linalg.norm(X,axis=1,keepdims=True)+1e-9)
Vn=V/ (np.linalg.norm(V,axis=1,keepdims=True)+1e-9)
for t in range(49):
    I=np.where(bins==t)[0]; J=np.where(bins==t+1)[0]
    if len(I)==0 or len(J)==0: continue
    XI=X[I]; XJ=X[J]
    dn2=(XI**2).sum(1)[:,None]+(XJ**2).sum(1)[None,:]-2*XI@XJ.T
    dn=np.sqrt(np.maximum(dn2,0)).astype(np.float32)
    num=(Vn[I]@Xn[J].T)-(Vn[I]*Xn[I]).sum(1)[:,None]
    cosv=(num/(dn+1e-9)).astype(np.float32)
    C=dn - LAM*cosv
    pi=sinkhorn(C)
    Fmass[np.ix_(I,J)]+=pi.astype(np.float32)
    del XI,XJ,dn2,dn,num,cosv,C,pi
    if t%10==0: print('stage: bin', t, flush=True)
# per-source-cell normalize, then cluster flow
rowsum=Fmass.sum(1,keepdims=True); rowsum[rowsum==0]=1
T=Fmass/rowsum
print('stage: scoring', flush=True)
F=cluster_flow(T, labels)
res=score(F, edges)
# spurious mass: outgoing fraction to non-canonical targets, per upstream cluster
canon={a:set() for a,_ in edges}
for a,b in edges: canon.setdefault(a,set()).add(b)
sp=[]
for a in canon:
    out=sum(v for (x,b),v in F.items() if x==a)
    spu=sum(v for (x,b),v in F.items() if x==a and b not in canon[a])
    sp.append(spu/out if out>0 else 0.0)
res['spurious_fraction']=float(np.mean(sp)); res['lambda']=LAM
json.dump(res, open(f'results/ot_{TAG}_lam{LAM}.json','w'), indent=1)
base=json.load(open(f'results/baseline_{TAG}.json'))
# baseline spurious
F0=cluster_flow(np.load(f'results/local/velocity_graph_T{sfx}.npy'), labels)
sp0=[]
for a in canon:
    out=sum(v for (x,b),v in F0.items() if x==a)
    spu=sum(v for (x,b),v in F0.items() if x==a and b not in canon[a])
    sp0.append(spu/out if out>0 else 0.0)
print('baseline spurious', round(float(np.mean(sp0)),4))
print(f'OT lam={LAM} {TAG}:', res['recovered'],'/',res['total'],'wrong',res['wrong'],'spurious',round(res['spurious_fraction'],4))
