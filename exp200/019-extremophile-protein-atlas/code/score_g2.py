#!/usr/bin/env python3
"""score_g2.py - G2 frozen gates: fit on dev only, single pass on frozen (study-level hotspring, sample-level others)."""
import json, numpy as np
from itertools import product
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
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
D={b:{s:recs(f'results/{b}_{s}.fasta') for s in ['dev','frozen']} for b in ['vent','hotspring','hypersaline','control']}
def build(groups,split):
    X=[]; y=[]; raw=[]
    for label,biomes in groups:
        for b in biomes:
            for s in D[b][split]:
                X.append(dipep(s)); y.append(label); raw.append(s)
    return np.array(X),np.array(y),raw
out={}
# Arm T
Xtr,ytr,_=build([(1,['vent','hotspring']),(0,['hypersaline','control'])],'dev')
Xte,yte,rte=build([(1,['vent','hotspring']),(0,['hypersaline','control'])],'frozen')
sc=StandardScaler().fit(Xtr)
clf=LogisticRegression(C=1.0,class_weight='balanced',max_iter=3000).fit(sc.transform(Xtr),ytr)
comp=roc_auc_score(yte,clf.predict_proba(sc.transform(Xte))[:,1])
ivy=roc_auc_score(yte,[frac(s,'IVYWREL') for s in rte])
out['armT']={'frozen_composite':comp,'frozen_ivywrel':ivy,'margin':comp-ivy,
             'pass':bool(comp>=0.70 and comp>=ivy+0.01)}
# Arm S
Xtr2,ytr2,_=build([(1,['hypersaline']),(0,['vent','hotspring','control'])],'dev')
Xte2,yte2,rte2=build([(1,['hypersaline']),(0,['vent','hotspring','control'])],'frozen')
sc2=StandardScaler().fit(Xtr2)
clf2=LogisticRegression(C=1.0,class_weight='balanced',max_iter=3000).fit(sc2.transform(Xtr2),ytr2)
comp2=roc_auc_score(yte2,clf2.predict_proba(sc2.transform(Xte2))[:,1])
de=roc_auc_score(yte2,[frac(s,'DE') for s in rte2])
out['armS']={'frozen_composite':comp2,'frozen_DE':de,'margin':comp2-de,
             'pass':bool(comp2>=0.70 and comp2>=de+0.01)}
out['G2_pass']=bool(out['armT']['pass'] and out['armS']['pass'])
print(json.dumps(out,indent=1))
json.dump(out,open('results/g2_frozen.json','w'),indent=1)
