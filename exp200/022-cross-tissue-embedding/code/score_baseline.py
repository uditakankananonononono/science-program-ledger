import numpy as np, json, sys, pandas as pd
sys.path.insert(0,'code')
from common import DEV, FROZEN, load, transfer_acc, dev_mean_acc
import harmonypy as hm
from sklearn.decomposition import TruncatedSVD

split=json.load(open('results/split.json'))
dev=split['dev']
genes=np.load('results/local/genes.npy', allow_pickle=True)

def lognorm_inplace(X):
    lib=X.sum(1, keepdims=True); lib[lib==0]=1
    X/=lib; X*=1e4; np.log1p(X, out=X)
    return X

# streaming mean/var for HVG on dev pooled
s=np.zeros(len(genes), np.float64); s2=np.zeros(len(genes), np.float64); n=0
for t in dev:
    X=np.load(f'results/local/{t}_X.npy')
    X=lognorm_inplace(X)
    s+=X.sum(0); s2+=(X.astype(np.float64)**2).sum(0); n+=len(X)
    np.save(f'results/local/{t}_log.npy', X); del X
var=s2/n-(s/n)**2
hv=np.sort(np.argsort(-var)[:2000])
# standardization stats on hv
mu=s[hv]/n; sd=np.sqrt(np.maximum(var[hv],1e-12))
Zdev={}
for t in dev:
    X=np.load(f'results/local/{t}_log.npy')
    Z=((X[:,hv]-mu)/sd).astype(np.float32)
    Zdev[t]=Z; np.save(f'results/local/{t}_Z.npy', Z); del X, Z
Zall=np.vstack([Zdev[t] for t in dev])
svd=TruncatedSVD(n_components=50, random_state=7).fit(Zall)
del Zall
Pdev={t: svd.transform(Zdev[t]).astype(np.float32) for t in dev}
y={t: np.load(f'results/local/{t}_y.npy', allow_pickle=True) for t in dev}
classes=json.load(open('results/class_list.json'))
acc_pca, per_pca = dev_mean_acc(Pdev, y, classes, dev)
Xall=np.vstack([Pdev[t] for t in dev])
meta=pd.DataFrame({'tissue': np.concatenate([[t]*len(Pdev[t]) for t in dev])})
ho=hm.run_harmony(Xall, meta, ['tissue'], random_state=7, verbose=False)
Z=ho.Z_corr; H=Z.T if Z.shape[0]==Xall.shape[1] else Z
i=0; Hdev={}
for t in dev:
    Hdev[t]=H[i:i+len(Pdev[t])].astype(np.float32); i+=len(Pdev[t])
acc_h, per_h = dev_mean_acc(Hdev, y, classes, dev)
out={'n_pcs':50,'pca_only':{'mean':acc_pca,'per_tissue':per_pca},'harmony':{'mean':acc_h,'per_tissue':per_h}}
json.dump(out, open('results/baseline_scores.json','w'), indent=1)
np.savez('results/local/dev_fit.npz', hv=hv, mu=mu, sd=sd)
import pickle; pickle.dump(svd, open('results/local/svd.pkl','wb'))
np.save('results/local/harmony_dev.npy', H)
print('PCA-only dev mean', round(acc_pca,4), per_pca)
print('Harmony  dev mean', round(acc_h,4), per_h)
