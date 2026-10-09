# Unit 195 result - DROPPED at DEV gate D1 (TEST sealed; official test never accessed)
Prereg algo50/195-PREREG.md sha256 2b5fb0a824df14d5ad785f19fc2a5faa3fb7833deb22b15bc99eb8cb6e68b93b. Note: the prereg title says no data loaded "for this unit"; AMES had been loaded for unit 194 and its test positive rate (0.597) was disclosed in the prereg.

D0 (mean E_raw - R >= 0.02): PASS, leakage gap 0.0812
D1 (E_sim DEV MAE <= 0.75 x min(E_raw, E_scaf) MAE): FAIL. DEV mean abs error over 5 salts x 6 models: E_raw 0.0812, E_scaf 0.0362, E_sim 0.0307. Threshold 0.75 x 0.0362 = 0.0272; E_sim 0.0307 is 15% below E_scaf, not 25%.
Verdict: DROPPED pre-TEST. No test statistic. Not a WIN.

## Per-model means over 5 salts (E_raw, E_scaf, E_sim, realized R) and mean abs error
```
RF {'E_raw': 0.8974, 'E_scaf': 0.84, 'E_sim': 0.8251, 'R': 0.8209} MAE {'E_raw': 0.0766, 'E_scaf': 0.0192, 'E_sim': 0.0262}
ET {'E_raw': 0.8989, 'E_scaf': 0.8376, 'E_sim': 0.828, 'R': 0.8191} MAE {'E_raw': 0.0798, 'E_scaf': 0.0205, 'E_sim': 0.0279}
LR {'E_raw': 0.8663, 'E_scaf': 0.769, 'E_sim': 0.7863, 'R': 0.7819} MAE {'E_raw': 0.0844, 'E_scaf': 0.06, 'E_sim': 0.0327}
KNN {'E_raw': 0.8794, 'E_scaf': 0.7997, 'E_sim': 0.7998, 'R': 0.7761} MAE {'E_raw': 0.1033, 'E_scaf': 0.0269, 'E_sim': 0.0368}
SVM {'E_raw': 0.8636, 'E_scaf': 0.7578, 'E_sim': 0.781, 'R': 0.7779} MAE {'E_raw': 0.0857, 'E_scaf': 0.0618, 'E_sim': 0.0322}
HGB {'E_raw': 0.8675, 'E_scaf': 0.8061, 'E_sim': 0.8017, 'R': 0.8103} MAE {'E_raw': 0.0573, 'E_scaf': 0.0289, 'E_sim': 0.0284}
```

Observation (descriptive, not a claim): random-CV AUROC overstated pseudo-test AUROC by 0.081 on average, confirming the leakage gap on this benchmark; the similarity reweighting removed most of it and beat the scaffold-validation proxy on the linear models (LR, SVM), while scaffold validation was better on RF/ET/KNN. Neither cleared the preregistered 0.75x bar.

## DEV log verbatim
```
Found local copy...
train_val 5821 invalid dropped 0
salt 1 pool 4656 pseudo-test 1165 scaf train/val 4074 582
  RF {'E_raw': 0.8995, 'E_sim': 0.8344, 'E_scaf': 0.8673, 'R': 0.8292}
  ET {'E_raw': 0.9008, 'E_sim': 0.8381, 'E_scaf': 0.8643, 'R': 0.828}
  LR {'E_raw': 0.8729, 'E_sim': 0.8015, 'E_scaf': 0.8364, 'R': 0.7521}
  KNN {'E_raw': 0.8808, 'E_sim': 0.8127, 'E_scaf': 0.8121, 'R': 0.7941}
  SVM {'E_raw': 0.8707, 'E_sim': 0.797, 'E_scaf': 0.8272, 'R': 0.7496}
  HGB {'E_raw': 0.8731, 'E_sim': 0.8109, 'E_scaf': 0.8369, 'R': 0.8098}
salt 2 pool 4655 pseudo-test 1166 scaf train/val 4074 581
  RF {'E_raw': 0.8952, 'E_sim': 0.8223, 'E_scaf': 0.8691, 'R': 0.8546}
  ET {'E_raw': 0.8963, 'E_sim': 0.8245, 'E_scaf': 0.8598, 'R': 0.8506}
  LR {'E_raw': 0.8596, 'E_sim': 0.7864, 'E_scaf': 0.7274, 'R': 0.7903}
  KNN {'E_raw': 0.875, 'E_sim': 0.7877, 'E_scaf': 0.8066, 'R': 0.8097}
  SVM {'E_raw': 0.8571, 'E_sim': 0.7819, 'E_scaf': 0.7161, 'R': 0.7844}
  HGB {'E_raw': 0.8629, 'E_sim': 0.7955, 'E_scaf': 0.8306, 'R': 0.8431}
salt 3 pool 3556 pseudo-test 2265 scaf train/val 3112 444
  RF {'E_raw': 0.891, 'E_sim': 0.7922, 'E_scaf': 0.8153, 'R': 0.8148}
  ET {'E_raw': 0.894, 'E_sim': 0.7988, 'E_scaf': 0.8152, 'R': 0.8202}
  LR {'E_raw': 0.8641, 'E_sim': 0.7544, 'E_scaf': 0.7607, 'R': 0.7974}
  KNN {'E_raw': 0.8779, 'E_sim': 0.7796, 'E_scaf': 0.7849, 'R': 0.7902}
  SVM {'E_raw': 0.8611, 'E_sim': 0.7466, 'E_scaf': 0.7458, 'R': 0.7928}
  HGB {'E_raw': 0.8584, 'E_sim': 0.77, 'E_scaf': 0.7669, 'R': 0.8147}
salt 4 pool 4583 pseudo-test 1238 scaf train/val 4011 572
  RF {'E_raw': 0.9017, 'E_sim': 0.826, 'E_scaf': 0.8075, 'R': 0.8024}
  ET {'E_raw': 0.9027, 'E_sim': 0.8287, 'E_scaf': 0.803, 'R': 0.802}
  LR {'E_raw': 0.8642, 'E_sim': 0.7774, 'E_scaf': 0.7184, 'R': 0.8011}
  KNN {'E_raw': 0.8845, 'E_sim': 0.7997, 'E_scaf': 0.7634, 'R': 0.725}
  SVM {'E_raw': 0.8613, 'E_sim': 0.772, 'E_scaf': 0.7068, 'R': 0.796}
  HGB {'E_raw': 0.8728, 'E_sim': 0.8084, 'E_scaf': 0.7742, 'R': 0.7966}
salt 5 pool 4656 pseudo-test 1165 scaf train/val 4074 582
  RF {'E_raw': 0.8999, 'E_sim': 0.8506, 'E_scaf': 0.8409, 'R': 0.8033}
  ET {'E_raw': 0.9004, 'E_sim': 0.8501, 'E_scaf': 0.8459, 'R': 0.7947}
  LR {'E_raw': 0.8707, 'E_sim': 0.8117, 'E_scaf': 0.8019, 'R': 0.7685}
  KNN {'E_raw': 0.8786, 'E_sim': 0.8194, 'E_scaf': 0.8314, 'R': 0.7616}
  SVM {'E_raw': 0.8678, 'E_sim': 0.8074, 'E_scaf': 0.7933, 'R': 0.7666}
  HGB {'E_raw': 0.8706, 'E_sim': 0.8239, 'E_scaf': 0.8218, 'R': 0.7871}
mean E_raw - R (leakage gap) 0.0812
DEV MAE {'E_raw': 0.0812, 'E_scaf': 0.0362, 'E_sim': 0.0307}
D0 True D1 False
```

## est195.py
```python
import numpy as np, pandas as pd, hashlib, sys, json, time
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
sys.path.insert(0,'../u194')
from rf194 import feat
def models():
    return {'RF':lambda:RandomForestClassifier(500,max_features='sqrt',min_samples_leaf=1,random_state=195,n_jobs=-1),
     'ET':lambda:ExtraTreesClassifier(500,max_features='sqrt',random_state=195,n_jobs=-1),
     'LR':lambda:LogisticRegression(C=1,max_iter=2000),
     'KNN':lambda:KNeighborsClassifier(5,metric='jaccard',weights='distance',algorithm='brute',n_jobs=-1),
     'SVM':lambda:LinearSVC(C=0.1,max_iter=5000),
     'HGB':lambda:HistGradientBoostingClassifier(max_iter=200,learning_rate=0.1,max_depth=4,random_state=195)}
def score(m,X):
    if hasattr(m,'predict_proba'): return m.predict_proba(X)[:,1]
    return m.decision_function(X)
def maxtan(A,B,chunk=500):
    A=A.astype(np.float32);B=B.astype(np.float32); nb=B.sum(1); out=np.zeros(len(A))
    for i in range(0,len(A),chunk):
        a=A[i:i+chunk]; inter=a@B.T; un=a.sum(1)[:,None]+nb[None,:]-inter
        out[i:i+chunk]=(inter/np.maximum(un,1e-9)).max(1)
    return out
def weights(s_oof,s_tgt,minc=20,clip=(0.1,10)):
    edges=np.quantile(s_tgt,np.linspace(0,1,11)); edges[0]=-1; edges[-1]=2
    b_o=np.clip(np.searchsorted(edges,s_oof,side='right')-1,0,9); b_t=np.clip(np.searchsorted(edges,s_tgt,side='right')-1,0,9)
    # merge small bins into neighbour: map bins -> groups
    cnt=np.bincount(b_o,minlength=10); grp=list(range(10))
    i=0
    while True:
        cnt_g={g:sum(cnt[k] for k in range(10) if grp[k]==g) for g in set(grp)}
        small=[g for g,c in cnt_g.items() if c<minc]
        if not small or len(cnt_g)==1: break
        g=min(small); gs=sorted(cnt_g); j=gs.index(g); nb=gs[j+1] if j+1<len(gs) else gs[j-1]
        grp=[nb if x==g else x for x in grp]
    go=np.array(grp)[b_o]; gt=np.array(grp)[b_t]
    w=np.ones(len(s_oof))
    for g in set(grp):
        po=(go==g).mean(); pt=(gt==g).mean(); w[go==g]=np.clip(pt/max(po,1e-9),*clip)
    return w
def run_models(Xp,yp,Xt,yt,sp_groups=None,scaf_split=None,seed=195):
    """returns per-model dict E_raw,E_sim,E_scaf,R"""
    # similarity of target to whole pool
    s_tgt=maxtan(Xt,Xp)
    skf=StratifiedKFold(5,shuffle=True,random_state=195); folds=list(skf.split(Xp,yp))
    s_oof=np.zeros(len(Xp))
    for tr,va in folds: s_oof[va]=maxtan(Xp[va],Xp[tr])
    w=weights(s_oof,s_tgt)
    tr_s,va_s=scaf_split
    out={}
    for name,mk in models().items():
        oof=np.zeros(len(Xp))
        for tr,va in folds: oof[va]=score(mk().fit(Xp[tr],yp[tr]),Xp[va])
        e_raw=roc_auc_score(yp,oof); e_sim=roc_auc_score(yp,oof,sample_weight=w)
        e_scaf=roc_auc_score(yp[va_s],score(mk().fit(Xp[tr_s],yp[tr_s]),Xp[va_s]))
        R=roc_auc_score(yt,score(mk().fit(Xp,yp),Xt))
        out[name]=dict(E_raw=e_raw,E_sim=e_sim,E_scaf=e_scaf,R=R)
        print(' ',name,{k:round(v,4) for k,v in out[name].items()},flush=True)
    return out,w
```

## dev195.py
```python
import numpy as np, pandas as pd, hashlib, json, time
from tdc.benchmark_group import admet_group
from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold
from est195 import *
g=admet_group(path='/tmp/tdcdata'); b=g.get('AMES'); tv=b['train_val']   # TEST ('test') never accessed
X,ok,scaf=feat(tv.Drug); y=tv.Y.values[ok]; print('train_val',len(y),'invalid dropped',int((~ok).sum()),flush=True)
uniq,inv=np.unique(scaf,return_inverse=True)
def scaffold_split_balanced(groups_idx,n,seed,frac_val=0.125):
    # chemprop-style: big groups (> half valid size) first to train, rest shuffled
    rng=np.random.default_rng(seed); nv=int(frac_val*n); big=[g for g in groups_idx if len(g)>nv/2]; small=[g for g in groups_idx if len(g)<=nv/2]
    rng.shuffle(big); rng.shuffle(small); order=big+small; tr=[];va=[]
    for g in order:
        (tr if len(tr)+len(g)<=n-nv else va).extend(g.tolist())
    return np.array(sorted(tr)),np.array(sorted(va))
res=[]
for salt in range(1,6):
    h=np.array([int(hashlib.sha256((s+str(salt)).encode()).hexdigest()[:8],16) for s in uniq])
    order=np.argsort(h); cnt=np.bincount(inv); pt_g=set(); tot=0
    for gi in order:
        if tot>=0.2*len(y): break
        pt_g.add(gi); tot+=cnt[gi]
    tgt=np.isin(inv,list(pt_g)); pool=np.where(~tgt)[0]; tg=np.where(tgt)[0]
    # scaffold split inside the pool
    pu,pinv=np.unique(inv[pool],return_inverse=True); gidx=[np.where(pinv==k)[0] for k in range(len(pu))]
    tr_s,va_s=scaffold_split_balanced(gidx,len(pool),salt)
    print('salt',salt,'pool',len(pool),'pseudo-test',len(tg),'scaf train/val',len(tr_s),len(va_s),flush=True)
    out,w=run_models(X[pool],y[pool],X[tg],y[tg],scaf_split=(tr_s,va_s))
    res.append(dict(salt=salt,out=out,wmin=float(w.min()),wmax=float(w.max())))
    json.dump(res,open('dev195_result.json','w'))
rows=[(r['salt'],m,v) for r in res for m,v in r['out'].items()]
mae={e:np.mean([abs(v[e]-v['R']) for _,_,v in rows]) for e in ('E_raw','E_scaf','E_sim')}
gap=np.mean([v['E_raw']-v['R'] for _,_,v in rows]); print('mean E_raw - R (leakage gap) %.4f'%gap)
print('DEV MAE',{k:round(v,4) for k,v in mae.items()})
D0=gap>=0.02; D1=mae['E_sim']<=0.75*min(mae['E_raw'],mae['E_scaf']); print('D0',D0,'D1',D1)
json.dump(dict(mae=mae,gap=float(gap),D0=bool(D0),D1=bool(D1)),open('dev195_gates.json','w'))
```
