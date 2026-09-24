import numpy as np, pandas as pd, json
from scipy.spatial import Delaunay
from collections import Counter
rng=np.random.default_rng(7)
def load(name):
    return np.load(f'results/local/{name}_Xlr.npy'), np.load(f'results/local/{name}_lrgenes.npy', allow_pickle=True), np.load(f'results/local/{name}_cl.npy')
def means(X, cl, C):
    M=np.zeros((C,X.shape[1]),np.float32)
    for c in range(C):
        m=cl==c
        if m.sum()>0: M[c]=X[m].mean(0)
    return M
X,genes,cl=load('Anterior')
gidx={g:i for i,g in enumerate(genes)}
C=cl.max()+1
lit=[('NRG1','ERBB4'),('VEGFA','KDR'),('NRXN1','NLGN1'),('BDNF','NTRK2'),('FGF1','FGFR2')]
lit=[(a,b) for a,b in lit if a in gidx and b in gidx]
prs=[(gidx[a],gidx[b]) for a,b in lit]
M=means(X,cl,C)
Li=[p[0] for p in prs]; Ri=[p[1] for p in prs]
obs=M[:,Li].T[:, :, None]*M[:,Ri].T[:, None, :]
cnt=np.zeros_like(obs)
for _ in range(100):
    clp=rng.permutation(cl)
    Mp=means(X,clp,C)
    cnt+=(Mp[:,Li].T[:, :, None]*Mp[:,Ri].T[:, None, :]>=obs)
pvals=(cnt+1)/101.0
sp=pd.read_csv('results/local/Anterior_coords.csv')
tri=Delaunay(sp[['px_row','px_col']].values)
cc=Counter()
for s in tri.simplices:
    for i in range(3):
        for j in range(i+1,3):
            ca,cb=cl[s[i]],cl[s[j]]
            if ca!=cb: cc[(min(ca,cb),max(ca,cb))]+=1
elig=np.eye(C,dtype=bool)
for (a,b),v in cc.items():
    if v>=10: elig[a,b]=elig[b,a]=True
litres={}
for k,(a,b) in enumerate(lit):
    sig_base=int((pvals[k]<=0.05).sum())
    sig_sp=int(((pvals[k]<=0.05)&elig[None,:,:]).sum())
    litres[f'{a}->{b}']={'sig_cluster_pairs_baseline':int(sig_base),'sig_cluster_pairs_spatial':int(sig_sp)}
sizes=Counter(cl.tolist())
deg={c:sum(v for (a,b),v in cc.items() if a==c or b==c) for c in range(C)}
size_arr=np.array([sizes[c] for c in range(C)]); deg_arr=np.array([deg[c] for c in range(C)])
bias_corr=float(np.corrcoef(size_arr,deg_arr)[0,1])
out={'literature_pairs':litres,'contact_degree_vs_cluster_size_corr':round(bias_corr,3),
     'n_eligible_pairs':int((elig.sum()-C)/2+C),'n_total_pairs':int(C*C)}
json.dump(out, open('results/g4_mechanism.json','w'), indent=1)
print(json.dumps(out, indent=1))
