import numpy as np, pandas as pd, json
from scipy.spatial import Delaunay
from sklearn.decomposition import TruncatedSVD
rng=np.random.default_rng(7)

def load(name):
    X=np.load(f'results/local/{name}_Xlr.npy'); genes=np.load(f'results/local/{name}_lrgenes.npy', allow_pickle=True)
    cl=np.load(f'results/local/{name}_cl.npy')
    return X, genes, cl

def means(X, cl, C):
    M=np.zeros((C, X.shape[1]), np.float32)
    for c in range(C):
        m=cl==c
        if m.sum()>0: M[c]=X[m].mean(0)
    return M

def transfer_labels(fit_name, val_name):
    Xf,gf,clf=load(fit_name); Xv,_,_=load(val_name)
    svd=TruncatedSVD(n_components=30, random_state=7).fit(Xf)
    Pf=svd.transform(Xf); Pv=svd.transform(Xv)
    C=clf.max()+1
    cents=np.stack([Pf[clf==c].mean(0) for c in range(C)])
    cents/=np.linalg.norm(cents,axis=1,keepdims=True)+1e-9
    Pvn=Pv/np.linalg.norm(Pv,axis=1,keepdims=True)+1e-9
    return (Pvn@cents.T).argmax(1)

def contact_counts(name, cl):
    sp=pd.read_csv(f'results/local/{name}_coords.csv')
    tri=Delaunay(sp[['px_row','px_col']].values)
    from collections import Counter
    cnt=Counter()
    for s in tri.simplices:
        for i in range(3):
            for j in range(i+1,3):
                a,b=s[i],s[j]; ca,cb=cl[a],cl[b]
                if ca!=cb: cnt[(min(ca,cb),max(ca,cb))]+=1
    C=cl.max()+1
    W=np.zeros((C,C),np.float32)
    for (a,b),v in cnt.items(): W[a,b]=W[b,a]=v
    np.fill_diagonal(W, np.median(W[W>0]))
    return W

def sig_weighted(X, cl, prs, C, W):
    M=means(X, cl, C)
    Li=[p[0] for p in prs]; Ri=[p[1] for p in prs]
    obs=M[:,Li].T[:, :, None]*M[:,Ri].T[:, None, :]*W[None,:,:]
    cnt=np.zeros_like(obs)
    for _ in range(100):
        clp=rng.permutation(cl)
        Mp=means(X, clp, C)
        cnt+=(Mp[:,Li].T[:, :, None]*Mp[:,Ri].T[:, None, :]*W[None,:,:]>=obs)
    return obs, (cnt+1)/101.0

pairs=[tuple(p) for p in json.load(open('results/lr_pairs.json'))]
out={}
for fit_name,val_name,tag in [('Anterior','Posterior','A2P'),('Posterior','Anterior','P2A')]:
    Xf,gf,clf=load(fit_name); Xv,_,_=load(val_name)
    gidx={g:i for i,g in enumerate(gf)}
    prs=[(gidx[a],gidx[b]) for a,b in pairs if a in gidx and b in gidx]
    C=clf.max()+1
    W=contact_counts(fit_name, clf)
    obs,pvals=sig_weighted(Xf, clf, prs, C, W)
    clv=transfer_labels(fit_name, val_name)
    Wv=contact_counts(val_name, clv)
    obsv,pvalsv=sig_weighted(Xv, clv, prs, C, Wv)
    sigf=pvals<=0.05
    cand=[]
    for pi in range(len(prs)):
        aa,bb=np.where(sigf[pi])
        for A,B in zip(aa,bb): cand.append((float(obs[pi,A,B]),pi,int(A),int(B)))
    cand.sort(reverse=True)
    top=cand[:100]
    hits=sum(1 for _,pi,A,B in top if pvalsv[pi,A,B]<=0.05)
    full=sum(1 for _,pi,A,B in cand if pvalsv[pi,A,B]<=0.05)
    out[tag]={'n_sig':len(cand),'precision@100':round(hits/max(len(top),1),3),'full_precision':round(full/max(len(cand),1),3)}
    print(tag, out[tag], flush=True)
json.dump(out, open('results/ccc_scores_p1.json','w'), indent=1)
