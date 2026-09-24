import numpy as np, json, sys
sys.path.insert(0,'code')
from common import *
import harmonypy as hm
d, classes = load()
split=json.load(open('results/split.json'))
# dev-only fit
Xdev={t: lognorm(d[f'{t}_X']) for t in split['dev']}
genes=d['genes']
pooled=np.vstack(list(Xdev.values()))
hv=hvg(pooled, genes, 2000)
mu,sd=standardize_fit(pooled[:,hv])
Zdev={t:(Xdev[t][:,hv]-mu)/sd for t in Xdev}
svd=TruncatedSVD(n_components=50, random_state=7).fit(np.vstack(list(Zdev.values())))
Pdev={t: svd.transform(Zdev[t]).astype(np.float32) for t in Zdev}
y={t: d[f'{t}_y'] for t in split['dev']}
# PCA-only context arm
acc_pca, per_pca = dev_mean_acc(Pdev, y, classes, split['dev'])
# Harmony named baseline
import pandas as pd
Xall=np.vstack([Pdev[t] for t in split['dev']])
meta=pd.DataFrame({'tissue': np.concatenate([[t]*len(Pdev[t]) for t in split['dev']])})
ho=hm.run_harmony(Xall, meta, ['tissue'], random_state=7, verbose=False)
Z=ho.Z_corr
H=Z.T if Z.shape[0]==Xall.shape[1] else Z
assert H.shape[0]==Xall.shape[0]
i=0; Hdev={}
for t in split['dev']:
    Hdev[t]=H[i:i+len(Pdev[t])]; i+=len(Pdev[t])
acc_h, per_h = dev_mean_acc(Hdev, y, classes, split['dev'])
out={'n_pcs':50,'pca_only':{'mean':acc_pca,'per_tissue':per_pca},
     'harmony':{'mean':acc_h,'per_tissue':per_h}}
json.dump(out, open('results/baseline_scores.json','w'), indent=1)
np.savez('results/local/dev_fit.npz', hv=hv, mu=mu, sd=sd, **{f'pca_{t}':Pdev[t] for t in split['dev']})
import pickle; pickle.dump(svd, open('results/local/svd.pkl','wb'))
print('PCA-only dev mean', round(acc_pca,4), per_pca)
print('Harmony  dev mean', round(acc_h,4), per_h)
