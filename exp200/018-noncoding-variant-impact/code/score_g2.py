#!/usr/bin/env python3
"""score_g2.py - G2 frozen gate (UTR stratum arm per ADDENDUM_P2): fit LR(f1-f6) on chr21 UTR dev, apply untouched to chr22 UTR frozen. Single pass, no refit."""
import csv, json, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
F=['f1','f2','f3','f4','f5','f6']
def load(p):
    rows=[r for r in csv.DictReader(open(p),delimiter='\t') if 'UTR' in r['mc']]
    X=np.array([[float(r[k]) for k in F] for r in rows])
    y=np.array([1 if r['label']=='P' else 0 for r in rows])
    return X,y
Xtr,ytr=load('results/dev_features.tsv')
Xte,yte=load('results/frozen_utr_features.tsv')
print('train',len(ytr),'P',int(ytr.sum()),'| frozen',len(yte),'P',int(yte.sum()),'B',int((1-yte).sum()))
sc=StandardScaler().fit(Xtr)
clf=LogisticRegression(C=1.0,class_weight='balanced',max_iter=2000).fit(sc.transform(Xtr),ytr)
comp=roc_auc_score(yte,clf.predict_proba(sc.transform(Xte))[:,1])
pp=roc_auc_score(yte,Xte[:,0]); pc=roc_auc_score(yte,Xte[:,1])
out={'frozen_composite_auroc':comp,'frozen_phyloP_auroc':pp,'frozen_phastCons_auroc':pc,
     'margin_vs_best_baseline':comp-max(pp,pc)}
out['G2_pass']=bool(comp>=0.65 and comp>=max(pp,pc)+0.01)
out['coef']=dict(zip(F,[round(float(c),4) for c in clf.coef_[0]]))
print(json.dumps(out,indent=1))
json.dump(out,open('results/g2_frozen_utr.json','w'),indent=1)
