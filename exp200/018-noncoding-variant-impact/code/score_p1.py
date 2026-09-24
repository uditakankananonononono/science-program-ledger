#!/usr/bin/env python3
"""score_p1.py - P1 arm: f1-f6 + 64-dim 3-mer composition (+/-25bp from local chr21 fasta)."""
import csv, json, numpy as np
from itertools import product
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
KMERS=[''.join(t) for t in product('ACGT',repeat=3)]
KIDX={k:i for i,k in enumerate(KMERS)}
seq=open('results/local/chr21.fa').read().split('\n',1)[1].replace('\n','')
rows=list(csv.DictReader(open('results/dev_features.tsv'),delimiter='\t'))
X6=np.array([[float(r[k]) for k in ['f1','f2','f3','f4','f5','f6']] for r in rows])
K=np.zeros((len(rows),64))
for i,r in enumerate(rows):
    pos=int(r['pos']); w=seq[pos-25:pos+26]
    for j in range(len(w)-2):
        k=w[j:j+3]
        if k in KIDX: K[i,KIDX[k]]+=1
    K[i]/=max(1,len(w)-2)
X=np.hstack([X6,K])
y=np.array([1 if r['label']=='P' else 0 for r in rows])
skf=StratifiedKFold(n_splits=5,shuffle=True,random_state=7)
aucs=[]
for tr,te in skf.split(X,y):
    sc=StandardScaler().fit(X[tr])
    clf=LogisticRegression(C=1.0,class_weight='balanced',max_iter=2000)
    clf.fit(sc.transform(X[tr]),y[tr])
    aucs.append(roc_auc_score(y[te],clf.predict_proba(sc.transform(X[te]))[:,1]))
m=float(np.mean(aucs))
g1=json.load(open('results/g1_dev.json'))
out={'p1_cv_auroc':m,'p1_folds':[round(a,4) for a in aucs],
     'margin_vs_phyloP':m-g1['phyloP_cv_auroc'],'margin_vs_phastCons':m-g1['phastCons_cv_auroc']}
out['P1_pass']=bool(out['margin_vs_phyloP']>=0.03 and out['margin_vs_phastCons']>=0.03)
print(json.dumps(out,indent=1))
json.dump(out,open('results/p1_dev.json','w'),indent=1)
