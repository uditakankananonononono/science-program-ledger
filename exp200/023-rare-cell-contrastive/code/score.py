import numpy as np, json, sys, torch, igraph as ig, leidenalg, collections
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors
torch.set_num_threads(2)

def leiden_labels(E, y, target, k=15, res=1.0, seed=7):
    nn=NearestNeighbors(n_neighbors=k+1).fit(E)
    D,I=nn.kneighbors(E)
    n=len(E); edges=[(i,j) for i in range(n) for j in I[i,1:]]
    g=ig.Graph(n=n, edges=edges).simplify()
    part=leidenalg.find_partition(g, leidenalg.RBConfigurationVertexPartition, resolution_parameter=res, seed=seed)
    cl=np.array(part.membership)
    pred=np.empty(n, dtype=object)
    for c in set(cl):
        m=cl==c
        pred[m]=collections.Counter(y[m].tolist()).most_common(1)[0][0]
    yt=(y==target); pt=(pred==target)
    tp=int((yt&pt).sum()); fp=int((~yt&pt).sum()); fn=int((yt&~pt).sum())
    f1=2*tp/max(2*tp+fp+fn,1); rec=tp/max(int(yt.sum()),1)
    return f1, rec, int(len(set(cl)))

def hvg_standardize(Xl, k=2000):
    v=Xl.var(0); hv=np.sort(np.argsort(-v)[:k])
    Z=Xl[:,hv]; mu=Z.mean(0); sd=Z.std(0); sd[sd==0]=1
    return ((Z-mu)/sd).astype(np.float32)

import os
EPOCHS=int(os.environ.get('CL_EPOCHS','30')); PROJ=int(os.environ.get('CL_PROJ','64'))
def contrastive_embed(Z, epochs=None, proj=None, bs=128, seed=7):
    epochs=epochs or EPOCHS; proj=proj or PROJ
    torch.manual_seed(seed); np.random.seed(seed)
    enc=torch.nn.Sequential(torch.nn.Linear(Z.shape[1],256), torch.nn.ReLU(), torch.nn.Linear(256,proj))
    opt=torch.optim.Adam(enc.parameters(), lr=1e-3)
    Xt=torch.from_numpy(Z); n=len(Xt)
    def aug(x):
        mask=(torch.rand_like(x)>0.1).float()
        return x*mask + 0.1*torch.randn_like(x)
    for ep in range(epochs):
        perm=torch.randperm(n)
        for i in range(0,n,bs):
            xb=Xt[perm[i:i+bs]]
            z1=torch.nn.functional.normalize(enc(aug(xb)),dim=1)
            z2=torch.nn.functional.normalize(enc(aug(xb)),dim=1)
            logits=z1@z2.T/0.5
            labels=torch.arange(len(xb))
            loss=(torch.nn.functional.cross_entropy(logits,labels)+torch.nn.functional.cross_entropy(logits.T,labels))/2
            opt.zero_grad(); loss.backward(); opt.step()
    with torch.no_grad():
        return enc(Xt).numpy().astype(np.float32)

def run_cohort(X_raw, y, grid, bg_idx, target, lognorm, out_path):
    res={'baseline':{}, 'contrastive':{}}
    for r, pp_idx in grid.items():
        idx=np.array(sorted(bg_idx.tolist()+pp_idx))
        X=X_raw[idx].astype(np.float32); yy=y[idx]
        if lognorm:
            lib=X.sum(1,keepdims=True); lib[lib==0]=1
            X/=lib; X*=1e4; np.log1p(X,out=X)
        Z=hvg_standardize(X)
        P=TruncatedSVD(n_components=50, random_state=7).fit_transform(Z)
        f1b,reb,ncb=leiden_labels(P, yy, target)
        E=contrastive_embed(Z) if os.environ.get('P1')!='1' else contrastive_embed(Z, epochs=60, proj=128)
        f1c,rec,ncc=leiden_labels(E, yy, target)
        res['baseline'][r]={'f1':f1b,'recall':reb,'n_clusters':ncb}
        res['contrastive'][r]={'f1':f1c,'recall':rec,'n_clusters':ncc,'p1':os.environ.get('P1')=='1'}
        print(f'r={r} baseline F1 {f1b:.3f} rec {reb:.3f} ({ncb} cl) | contrastive F1 {f1c:.3f} rec {rec:.3f} ({ncc} cl)', flush=True)
    mb=float(np.mean([v['f1'] for v in res['baseline'].values()]))
    mc=float(np.mean([v['f1'] for v in res['contrastive'].values()]))
    res['mean_f1']={'baseline':mb,'contrastive':mc}
    json.dump(res, open(out_path,'w'), indent=1)
    print('MEAN F1 baseline', round(mb,4), 'contrastive', round(mc,4), flush=True)

if __name__=='__main__':
    tag=sys.argv[1]
    if tag=='dev':
        X=np.load('results/local/dev_X.npy'); y=np.load('results/local/dev_y.npy', allow_pickle=True)
        g=json.load(open('results/rarity_grid.json'))
        bg=np.array([i for i in range(len(y)) if y[i]!='pancreatic PP cell'])
        run_cohort(X, y, g['grid'], bg, 'pancreatic PP cell', True, 'results/dev_scores.json')
    else:
        X=np.load('results/local/frozen_X.npy'); y=np.load('results/local/frozen_y.npy', allow_pickle=True)
        g=json.load(open('results/rarity_grid_frozen.json'))
        bg=np.array([i for i in range(len(y)) if y[i]!='gamma'])
        run_cohort(X, y, g['grid'], bg, 'gamma', False, 'results/frozen_scores.json')
