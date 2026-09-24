import numpy as np, json, pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import KNeighborsClassifier

DEV=['Marrow','Lung','Heart']; FROZEN=['Spleen']
class D(dict):
    def __getitem__(self,k):
        if k=='genes': return np.load('results/local/genes.npy', allow_pickle=True)
        return np.load(f'results/local/{k}.npy', allow_pickle=True)
def load():
    return D(), json.load(open('results/class_list.json'))
def lognorm(X):
    lib=X.sum(1, keepdims=True); lib[lib==0]=1
    return np.log1p(X/lib*1e4).astype(np.float32)
def hvg(Xgenes_log, genes, k=2000):
    v=Xgenes_log.var(0); idx=np.argsort(-v)[:k]
    return np.sort(idx)
def standardize_fit(Xtr):
    mu=Xtr.mean(0); sd=Xtr.std(0); sd[sd==0]=1
    return mu, sd
def transfer_acc(emb_by_tissue, y_by_tissue, classes, held):
    tr_t=[t for t in emb_by_tissue if t!=held]
    Xtr=np.vstack([emb_by_tissue[t] for t in tr_t]); ytr=np.concatenate([y_by_tissue[t] for t in tr_t])
    m=np.isin(ytr, classes); Xtr,ytr=Xtr[m],ytr[m]
    # Addendum A: score only classes with >=30 cells in the training pool
    import collections
    cnt=collections.Counter(ytr.tolist())
    ok={k for k,v in cnt.items() if v>=30}
    m2=np.array([l in ok for l in ytr]); Xtr,ytr=Xtr[m2],ytr[m2]
    Xte=emb_by_tissue[held]; yte=y_by_tissue[held]
    m=np.isin(yte, classes) & np.array([l in ok for l in yte]); Xte,yte=Xte[m],yte[m]
    if len(Xte)==0: return None,0
    knn=KNeighborsClassifier(n_neighbors=5, metric='cosine').fit(Xtr,ytr)
    acc=(knn.predict(Xte)==yte).mean()
    return float(acc), len(yte)
def dev_mean_acc(emb_by_tissue, y_by_tissue, classes, tissues):
    accs={}
    for t in tissues:
        a,n=transfer_acc(emb_by_tissue, y_by_tissue, classes, t)
        accs[t]={'acc':a,'n_test':n}
    vals=[v['acc'] for v in accs.values() if v['acc'] is not None]
    return float(np.mean(vals)), accs
