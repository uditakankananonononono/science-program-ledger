#!/usr/bin/env python3
"""Fate forecast CLI: expression vector -> next-state distribution (DOC-1-005 payload).
Input: CSV with one column of UMI counts aligned to the model's 1000 genes (gene,count),
or a JSON dict {gene: umi_count}. Missing genes are treated as 0.
Output: JSON {state: probability} from the trained MLP forecaster."""
import sys, json
import numpy as np, pandas as pd, joblib
d=joblib.load('results/fate_forecast_model.joblib')
names=d['top_gene_names']
if sys.argv[1].endswith('.json'):
    counts=json.load(open(sys.argv[1]))
else:
    counts=dict(pd.read_csv(sys.argv[1],header=None,names=['gene','count']).values)
v=np.array([counts.get(g,0) for g in names],np.float32)
lib=v.sum(); lib=lib if lib>0 else 1
xn=np.log1p(v*(1e4/lib))[None,:]
proba=d['mlp'].predict_proba(d['pca'].transform(xn))[0]
print(json.dumps({str(c):float(p) for c,p in zip(d['mlp'].classes_,proba)},indent=2))
