import numpy as np, pandas as pd, json
from scipy.spatial import Delaunay
from sklearn.decomposition import TruncatedSVD
rng=np.random.default_rng(7)

def load(name):
    X=np.load(f'results/local/{name}_Xlr.npy')
    genes=np.load(f'results/local/{name}_lrgenes.npy', allow_pickle=True)
    cl=np.load(f'results/local/{name}_cl.npy')
    return X, genes, cl

def means(X, cl, C):
    M=np.zeros((C, X.shape[1]), np.float32)
    for c in range(C):
        m=cl==c
        if m.sum()>0: M[c]=X[m].mean(0)
    return M

def transfer_labels(fit_name, val_name):
    Xf,gf,clf=load(fit_name); Xv,gv,_=load(val_name)
    assert list(gf)==list(gv)
    svd=TruncatedSVD(n_components=30, random_state=7).fit(Xf)
    Pf=svd.transform(Xf); Pv=svd.transform(Xv)
    C=clf.max()+1
    cents=np.stack([Pf[clf==c].mean(0) for c in range(C)])
    cents/=np.linalg.norm(cents,axis=1,keepdims=True)+1e-9
    Pvn=Pv/np.linalg.norm(Pv,axis=1,keepdims=True)+1e-9
    sim=Pvn@cents.T
    return sim.argmax(1)

def sig(X, cl, prs_idx, C):
    M=means(X, cl, C)
    Li=[p[0] for p in prs_idx]; Ri=[p[1] for p in prs_idx]
    obs=M[:,Li].T[:, :, None]*M[:,Ri].T[:, None, :]
    cnt=np.zeros_like(obs)
    for _ in range(100):
        clp=rng.permutation(cl)
        Mp=means(X, clp, C)
        cnt+=(Mp[:,Li].T[:, :, None]*Mp[:,Ri].T[:, None, :]>=obs)
    return obs, (cnt+1)/101.0

def adjacency(name, cl):
    sp=pd.read_csv(f'results/local/{name}_coords.csv')
    tri=Delaunay(sp[['px_row','px_col']].values)
    from collections import Counter
    cnt=Counter()
    for s in tri.simplices:
        for i in range(3):
            for j in range(i+1,3):
                a,b=s[i],s[j]
                ca,cb=cl[a],cl[b]
                if ca!=cb: cnt[(min(ca,cb),max(ca,cb))]+=1
    C=cl.max()+1
    elig=np.eye(C,dtype=bool)
    for (a,b),v in cnt.items():
        if v>=10: elig[a,b]=elig[b,a]=True
    return elig

pairs=[tuple(p) for p in json.load(open('results/lr_pairs.json'))]
out={}
for fit_name,val_name,tag in [('Anterior','Posterior','A2P'),('Posterior','Anterior','P2A')]:
    Xf,gf,clf=load(fit_name); Xv,gv,_=load(val_name)
    gidx={g:i for i,g in enumerate(gf)}
    prs=[(gidx[a],gidx[b]) for a,b in pairs if a in gidx and b in gidx]
    C=clf.max()+1
    obs,pvals=sig(Xf, clf, prs, C)
    clv=transfer_labels(fit_name, val_name)
    obsv,pvalsv=sig(Xv, clv, prs, C)
    elig=adjacency(fit_name, clf)
    res={}
    for arm in ['baseline','spatial']:
        mask=np.ones((C,C),bool) if arm=='baseline' else elig
        sigf=(pvals<=0.05)&mask[None,:,:]
        cand=[]
        for pi in range(len(prs)):
            aa,bb=np.where(sigf[pi])
            for A,B in zip(aa,bb): cand.append((float(obs[pi,A,B]),pi,int(A),int(B)))
        cand.sort(reverse=True)
        top=cand[:100]
        hits=sum(1 for _,pi,A,B in top if pvalsv[pi,A,B]<=0.05)
        full_hits=sum(1 for _,pi,A,B in cand if pvalsv[pi,A,B]<=0.05)
        res[arm]={'n_sig':len(cand),'precision@100':round(hits/max(len(top),1),3),
                  'full_precision':round(full_hits/max(len(cand),1),3)}
    out[tag]=res
    print(tag, json.dumps(res), flush=True)
json.dump(out, open('results/ccc_scores.json','w'), indent=1)
b=out['A2P']['baseline']['precision@100']; s=out['A2P']['spatial']['precision@100']
print('G1 sanity (>=0.20):', b, '| G2 (spatial >= baseline+0.10):', s, 'vs', b)
