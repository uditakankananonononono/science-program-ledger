#!/usr/bin/env python3
"""score_g1.py - G1 dev gate: 5-fold stratified CV (seed 7) composite LR vs phyloP-only / phastCons-only."""
import csv, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
rows=list(csv.DictReader(open('results/dev_features.tsv'),delimiter='\t'))
X=np.array([[float(r[k]) for k in ['f1','f2','f3','f4','f5','f6']] for r in rows])
y=np.array([1 if r['label']=='P' else 0 for r in rows])
print('n',len(y),'P',int(y.sum()),'B',int((1-y).sum()))
skf=StratifiedKFold(n_splits=5,shuffle=True,random_state=7)
def cv_auroc(cols,model='lr'):
    aucs=[]
    for tr,te in skf.split(X,y):
        if model=='lr':
            sc=StandardScaler().fit(X[tr][:,cols])
            clf=LogisticRegression(C=1.0,class_weight='balanced',max_iter=2000)
            clf.fit(sc.transform(X[tr][:,cols]),y[tr])
            p=clf.predict_proba(sc.transform(X[te][:,cols]))[:,1]
        else:
            p=X[te][:,cols[0]]
        aucs.append(roc_auc_score(y[te],p))
    return float(np.mean(aucs)),[round(a,4) for a in aucs]
comp=cv_auroc([0,1,2,3,4,5]); pp=cv_auroc([0],'raw'); pc=cv_auroc([1],'raw')
g1={'composite_cv_auroc':comp[0],'composite_folds':comp[1],'phyloP_cv_auroc':pp[0],'phastCons_cv_auroc':pc[0],
    'margin_vs_phyloP':comp[0]-pp[0],'margin_vs_phastCons':comp[0]-pc[0]}
g1['G1_pass']=bool(g1['margin_vs_phyloP']>=0.03 and g1['margin_vs_phastCons']>=0.03)
import json; print(json.dumps(g1,indent=1))
json.dump(g1,open('results/g1_dev.json','w'),indent=1)
