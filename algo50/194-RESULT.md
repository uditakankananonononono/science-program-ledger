# Unit 194 result - DROPPED at DEV gate D1 (TEST sealed, never loaded into any model)
Prereg algo50/194-PREREG.md sha256 7215b45586199cb7723a3338eedc8b2b79d534e1a3f01cefebb5e2597a1242ef. Benchmark: TDC ADMET AMES, 5 seeds of scaffold train/valid split of train_val (5,821), VALID AUROC only.

D0 (baseline mean VALID AUROC >= 0.75): PASS 0.8593
D1 (candidate minus baseline >= +0.005): FAIL, candidate 0.8609, diff +0.0016
Verdict: DROPPED pre-TEST. No test AUROC exists. The 1,457-compound test split was not scored. Exposure disclosed in prereg: one test-label scalar (positive rate 0.597).

## DEV log verbatim
```
Found local copy...
generating training, validation splits...
seed 1 train 5093 valid 728 invalid dropped 0
1 B sqrt 1 valid AUROC 0.8867 8s
1 B sqrt 2 valid AUROC 0.8955 6s
1 B 0.2 1 valid AUROC 0.8746 47s
1 B 0.2 2 valid AUROC 0.8864 41s
1 C sqrt 1 valid AUROC 0.8889 20s
1 C sqrt 2 valid AUROC 0.8970 17s
1 C 0.2 1 valid AUROC 0.8866 90s
1 C 0.2 2 valid AUROC 0.8923 921s
generating training, validation splits...
seed 2 train 4553 valid 1268 invalid dropped 0
2 B sqrt 1 valid AUROC 0.7793 6s
2 B sqrt 2 valid AUROC 0.7786 5s
2 B 0.2 1 valid AUROC 0.7630 40s
2 B 0.2 2 valid AUROC 0.7721 35s
2 C sqrt 1 valid AUROC 0.7820 15s
2 C sqrt 2 valid AUROC 0.7813 15s
2 C 0.2 1 valid AUROC 0.7752 79s
2 C 0.2 2 valid AUROC 0.7796 75s
generating training, validation splits...
seed 3 train 5093 valid 728 invalid dropped 0
3 B sqrt 1 valid AUROC 0.8829 7s
3 B sqrt 2 valid AUROC 0.8813 5s
3 B 0.2 1 valid AUROC 0.8621 46s
3 B 0.2 2 valid AUROC 0.8706 40s
3 C sqrt 1 valid AUROC 0.8753 17s
3 C sqrt 2 valid AUROC 0.8821 16s
3 C 0.2 1 valid AUROC 0.8690 86s
3 C 0.2 2 valid AUROC 0.8777 83s
generating training, validation splits...
seed 4 train 5093 valid 728 invalid dropped 0
4 B sqrt 1 valid AUROC 0.8719 7s
4 B sqrt 2 valid AUROC 0.8745 5s
4 B 0.2 1 valid AUROC 0.8629 45s
4 B 0.2 2 valid AUROC 0.8702 39s
4 C sqrt 1 valid AUROC 0.8745 16s
4 C sqrt 2 valid AUROC 0.8757 16s
4 C 0.2 1 valid AUROC 0.8653 85s
4 C 0.2 2 valid AUROC 0.8697 83s
generating training, validation splits...
seed 5 train 5093 valid 728 invalid dropped 0
5 B sqrt 1 valid AUROC 0.8631 7s
5 B sqrt 2 valid AUROC 0.8645 6s
5 B 0.2 1 valid AUROC 0.8563 46s
5 B 0.2 2 valid AUROC 0.8629 39s
5 C sqrt 1 valid AUROC 0.8600 19s
5 C sqrt 2 valid AUROC 0.8677 16s
5 C 0.2 1 valid AUROC 0.8601 88s
5 C 0.2 2 valid AUROC 0.8649 85s
B mean best-valid AUROC 0.8593  C 0.8609  diff 0.0016 D0 True D1 False
```

Note: the group-bootstrap forest was no better than ordinary RF on scaffold-held-out VALID (best per-seed grid cell, mean over seeds).

## rf194.py
```python
import numpy as np, pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem import rdFingerprintGenerator
from rdkit.Chem.Scaffolds import MurckoScaffold
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from joblib import Parallel, delayed
RDLogger.DisableLog('rdApp.*')
GEN=rdFingerprintGenerator.GetMorganGenerator(radius=2,fpSize=2048)
def feat(smiles):
    X=[];ok=[];sc=[]
    for s in smiles:
        m=Chem.MolFromSmiles(s)
        if m is None: ok.append(False); continue
        X.append(GEN.GetFingerprintAsNumPy(m).astype(np.uint8)); ok.append(True)
        try: sc.append(MurckoScaffold.MurckoScaffoldSmiles(mol=m))
        except Exception: sc.append(s)
    return np.array(X),np.array(ok),np.array(sc)
def _tree(X,y,groups_idx,seed,mf,msl):
    rng=np.random.default_rng(seed); g=rng.integers(0,len(groups_idx),len(groups_idx))
    idx=np.concatenate([groups_idx[i] for i in g])
    t=DecisionTreeClassifier(max_features=mf,min_samples_leaf=msl,random_state=seed).fit(X[idx],y[idx])
    p=np.zeros(2); return t
class GroupRF:
    def __init__(s,n=500,max_features='sqrt',min_samples_leaf=1,random_state=0,n_jobs=-1): s.n=n;s.mf=max_features;s.msl=min_samples_leaf;s.rs=random_state;s.nj=n_jobs
    def fit(s,X,y,scaf):
        u,inv=np.unique(scaf,return_inverse=True); gi=[np.where(inv==k)[0] for k in range(len(u))]
        s.trees=Parallel(n_jobs=s.nj)(delayed(_tree)(X,y,gi,s.rs*10007+i,s.mf,s.msl) for i in range(s.n)); return s
    def predict_proba1(s,X):
        P=np.zeros(len(X)); 
        for t in s.trees:
            pr=t.predict_proba(X); P+=pr[:,list(t.classes_).index(1)] if 1 in t.classes_ else 0
        return P/len(s.trees)
GRID=[(mf,msl) for mf in ('sqrt',0.2) for msl in (1,2)]
```

## dev194.py
```python
import numpy as np, pandas as pd, json, sys, time
from sklearn.metrics import roc_auc_score
from tdc.benchmark_group import admet_group
from rf194 import *
g=admet_group(path='/tmp/tdcdata'); res={}
for seed in range(1,6):
    tr,va=g.get_train_valid_split(benchmark='AMES',split_type='default',seed=seed)
    Xt,okt,sct=feat(tr.Drug); yt=tr.Y.values[okt]; Xv,okv,scv=feat(va.Drug); yv=va.Y.values[okv]
    print('seed',seed,'train',len(yt),'valid',len(yv),'invalid dropped',int((~okt).sum()+(~okv).sum()),flush=True)
    for arm in ('B','C'):
        best=None
        for mf,msl in GRID:
            t0=time.time()
            if arm=='B':
                m=RandomForestClassifier(n_estimators=500,max_features=mf,min_samples_leaf=msl,random_state=seed,n_jobs=-1).fit(Xt,yt); p=m.predict_proba(Xv)[:,1]
            else:
                m=GroupRF(500,mf,msl,seed).fit(Xt,yt,sct); p=m.predict_proba1(Xv)
            a=roc_auc_score(yv,p); res[f'{seed}|{arm}|{mf}|{msl}']=a
            print(seed,arm,mf,msl,'valid AUROC %.4f'%a,'%.0fs'%(time.time()-t0),flush=True)
json.dump(res,open('dev194_result.json','w'))
def best(arm): return np.mean([max(v for k,v in res.items() if k.startswith(f'{s}|{arm}|')) for s in range(1,6)])
b,c=best('B'),best('C'); print('B mean best-valid AUROC %.4f  C %.4f  diff %.4f'%(b,c,c-b),'D0',b>=0.75,'D1',c-b>=0.005)
json.dump(dict(B=b,C=c,D0=bool(b>=0.75),D1=bool(c-b>=0.005)),open('dev194_gates.json','w'))
```
