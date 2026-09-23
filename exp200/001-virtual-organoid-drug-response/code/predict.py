#!/usr/bin/env python3
"""DOC-1-001 tool: predict ln IC50 for a (expression vector, drug) pair with abstention.
Usage: predict.py --drug <name> --expression <csv row of gene,value> 
Model artifacts produced by train_tool.py (frozen after gate evaluation)."""
import argparse, json, pickle
import numpy as np, pandas as pd

p = argparse.ArgumentParser()
p.add_argument('--drug', required=True)
p.add_argument('--expression', required=True, help='CSV file: gene,value (log1p TPM)')
a = p.parse_args()
art = pickle.load(open('results/tool_model.pkl','rb'))
if a.drug not in art['models']:
    raise SystemExit(f"drug not covered: {a.drug}; covered: {sorted(art['models'])}")
row = pd.read_csv(a.expression, names=['gene','value']).set_index('gene')['value']
m = art['models'][a.drug]
x = np.array([row.get(g, np.nan) for g in m['genes']], dtype=np.float32)
if np.isnan(x).mean() > 0.5:
    raise SystemExit('ABSTAIN: >50% of model genes missing from input')
x = np.nan_to_num(x, nan=np.nanmean(x))
z = (x - m['mu']) / m['sd']
pred = float(m['coef'] @ z + m['intercept'])
dist = float(z @ art['prec'] @ z)  # Mahalanobis to training centroid
abstain = dist > art['dist_threshold']
print(json.dumps(dict(drug=a.drug, predicted_ln_ic50=round(pred,3),
                      ic50_uM=round(float(np.exp(pred)),3),
                      abstain=abstain, mahalanobis=round(dist,1),
                      threshold=art['dist_threshold'])))
