#!/usr/bin/env python3
"""Diagnosis + falsification test for colon biopsies (exp200/159; boundary result).
Usage: cf_test.py matrix.tsv (genes x samples; gene symbols in column 1; any scale).
Retrains the frozen L1 model from GSE87466 (needs data/) and prints, per sample:
P(UC) and the genes whose move to healthy levels would flip the call, with direction.
Caveat: the model is sparse (9 genes), so most flips rest on SLC6A14 / DPP10-AS1."""
import sys,os;os.chdir(os.path.join(os.path.dirname(__file__),'..'));sys.path.insert(0,'code')
import numpy as np,pandas as pd,geo
from sklearn.linear_model import LogisticRegression
d,m=geo.load('GSE87466');A=geo.genes(d,'GPL13158');y=np.array([0 if 'Normal' in x else 1 for x in m])
X=pd.read_csv(sys.argv[1],sep='\t',index_col=0);X=X[~X.index.duplicated()];U=sorted(set(A.index)&set(X.index))
A=A.loc[U].rank(pct=True);X=X.loc[U].rank(pct=True);mu=A.mean(1).values;sd=A.std(1).values+1e-9;H=A.values[:,y==0].mean(1)
c=LogisticRegression(penalty='l1',C=0.1,solver='liblinear',max_iter=5000).fit((A.values.T-mu)/sd,y);w=c.coef_[0];b=c.intercept_[0]
for s in X.columns:
    v=X[s].values;z=((v-mu)/sd)@w+b;p=1/(1+np.exp(-z));g={j:w[j]*(v[j]-H[j])/sd[j] for j in np.flatnonzero(w)};out=[]
    for j in sorted([j for j in g if g[j]>0],key=lambda j:-g[j]):
        if z<0: break
        z-=g[j];out.append(f"{U[j]}:{'down' if H[j]<v[j] else 'up'}")
    print(f"{s}\tP(UC)={p:.2f}\tflip-if: {','.join(out) if p>=0.5 else '-'}")
