#!/usr/bin/env python3
"""score_g1.py - G1 dev gates: Arm T (thermal vs non-thermal, IVYWREL baseline), Arm S (hypersaline vs rest, D+E baseline)."""
import json, numpy as np
from itertools import product
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
AA='ACDEFGHIKLMNPQRSTVWY'
DI=[''.join(t) for t in product(AA,repeat=2)]
DIDX={d:i for i,d in enumerate(DI)}
def recs(p):
    out=[]
    for blk in open(p).read().split('\n>'):
        blk=blk.lstrip('>')
        if blk and '\n' in blk:
            h,s=blk.split('\n',1); out.append(s.replace('\n',''))
    return out
def dipep(s):
    v=np.zeros(400)
    for i in range(len(s)-1):
        j=DIDX.get(s[i:i+2])
        if j is not None: v[j]+=1
    return v/max(1,len(s)-1)
def frac(s,res): return sum(1 for c in s if c in res)/len(s)
D={b:{'dev':recs(f'results/{b}_dev.fasta'),'frozen':recs(f'results/{b}_frozen.fasta')} for b in ['vent','hotspring','hypersaline','control']}
print({b:{s:len(D[b][s]) for s in D[b]} for b in D})
def build(groups):
    X=[]; y=[]
    for label,biomes in groups:
        for b in biomes:
            for s in D[b]['dev']:
                X.append(dipep(s)); y.append(label)
    return np.array(X),np.array(y)
skf=StratifiedKFold(n_splits=5,shuffle=True,random_state=7)
def cv_lr(X,y):
    a=[]
    for tr,te in skf.split(X,y):
        sc=StandardScaler().fit(X[tr])
        clf=LogisticRegression(C=1.0,class_weight='balanced',max_iter=3000).fit(sc.transform(X[tr]),y[tr])
        a.append(roc_auc_score(y[te],clf.predict_proba(sc.transform(X[te]))[:,1]))
    return float(np.mean(a)),[round(v,4) for v in a]
def base_auc(y,scores): return roc_auc_score(y,scores)
out={}
# Arm T: thermal (vent+hotspring) vs non-thermal (hypersaline+control)
X,y=build([(1,['vent','hotspring']),(0,['hypersaline','control'])])
seqs=[s for b in ['vent','hotspring'] for s in D[b]['dev']]+[s for b in ['hypersaline','control'] for s in D[b]['dev']]
ivy=np.array([frac(s,'IVYWREL') for s in seqs])
comp,folds=cv_lr(X,y)
out['armT']={'composite_cv':comp,'folds':folds,'ivywrel_auc':float(roc_auc_score(y,ivy)),'margin':comp-float(roc_auc_score(y,ivy))}
out['armT']['pass']=bool(out['armT']['margin']>=0.03)
# Arm S: hypersaline vs rest
X2,y2=build([(1,['hypersaline']),(0,['vent','hotspring','control'])])
seqs2=[s for s in D['hypersaline']['dev']]+[s for b in ['vent','hotspring','control'] for s in D[b]['dev']]
de=np.array([frac(s,'DE') for s in seqs2])
comp2,folds2=cv_lr(X2,y2)
out['armS']={'composite_cv':comp2,'folds':folds2,'DE_auc':float(roc_auc_score(y2,de)),'margin':comp2-float(roc_auc_score(y2,de))}
out['armS']['pass']=bool(out['armS']['margin']>=0.03)
out['G1_pass']=bool(out['armT']['pass'] and out['armS']['pass'])
print(json.dumps(out,indent=1))
json.dump(out,open('results/g1_dev.json','w'),indent=1)
