# 196 driver (run as driver196.py, sha256 8ee999c273ee6efcfc24d7d593adffa2ccd552995e85579df3c7b9a61ab18ae3)
```python
import sys, json, time, numpy as np, pandas as pd, torch
sys.path.insert(0,'mega27-05-yeast-metabolic-twin-4b66f67/src')
from yeasttwin import evaluate as E
from yeasttwin.evaluate import *
from yeasttwin.labels import load_labels
from yeasttwin.ml import train_gcn, auc_roc
def run(seed, tag):
    labels=load_labels(); feat=load_feature_table()
    genes=[g for g in feat.index if g in labels.index]
    y=labels.loc[genes].to_numpy(dtype=bool); feat=feat.loc[genes]
    x_raw=feat.to_numpy(dtype=np.float32)
    gg,a_hat=load_graph(); gpos={g:i for i,g in enumerate(gg)}
    order=np.array([gpos[g] for g in genes])
    xgr=np.zeros((len(gg),x_raw.shape[1]),dtype=np.float32); xgr[order]=x_raw
    yg=np.zeros(len(gg),dtype=np.float32); yg[order]=y.astype(np.float32)
    folds=make_folds(y,5,3,seed); rows=[]
    for r in range(3):
        for f in range(5):
            te=np.flatnonzero(folds[:,r]==f); tr=np.flatnonzero(folds[:,r]!=f)
            m=x_raw[tr].mean(0); s=x_raw[tr].std(0)+1e-9
            xtr=(x_raw[tr]-m)/s; xte=(x_raw[te]-m)/s
            xg=torch.tensor((xgr-m)/s)
            sg=train_gcn(xg,a_hat,yg,torch.tensor(order[tr]),epochs=300,seed=seed+r*100+f)
            fba=1.0-x_raw[te][:,0]
            lr=score_logreg(pd.DataFrame(xtr),pd.DataFrame(xte),y[tr])
            rows.append(dict(tag=tag,repeat=r,fold=f,fba=auc_roc(y[te],fba),logreg=auc_roc(y[te],lr),gcn=auc_roc(y[te],sg[order[te]])))
            print(rows[-1],flush=True)
    return pd.DataFrame(rows)
def boot(d):
    rng=np.random.default_rng(7); b=rng.choice(d,size=(2000,len(d)),replace=True).mean(1)
    return float(d.mean()),float(np.percentile(b,2.5)),float(np.percentile(b,97.5))
out={}
for tag,seed in [('A',20260924),('B',196196)]:
    df=run(seed,tag); df.to_csv(f'folds_{tag}.csv',index=False)
    out[tag]={'mean_auc':{k:float(df[k].mean()) for k in ['fba','logreg','gcn']},
              'gcn_minus_fba':boot((df.gcn-df.fba).to_numpy())}
    if tag=='B': out['C_gcn_minus_logreg']=boot((df.gcn-df.logreg).to_numpy())
    print(json.dumps(out,indent=1),flush=True)
json.dump(out,open('result196.json','w'),indent=1)
```
