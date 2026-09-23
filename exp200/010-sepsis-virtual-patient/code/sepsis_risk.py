#!/usr/bin/env python3
"""sepsis_risk.py - early sepsis risk for one ICU patient record (.psv, PhysioNet Challenge 2019 format).
Usage: python3 sepsis_risk.py patient.psv
Model: HistGradientBoosting trained on Challenge 2019 set A (20,086 patients), frozen cross-hospital
validation AUROC 0.881 on set B (19,748 patients). Features use only data before the first sepsis label."""
import sys, os, pickle, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_features import extract
def main():
    psv=sys.argv[1]
    here=os.path.dirname(os.path.abspath(__file__))
    bundle=pickle.load(open(os.path.join(here,'..','results','model.pkl'),'rb'))
    m,cols=bundle['model'],bundle['cols']
    feats,lab=extract(psv)
    if feats is None:
        print('Cannot score: no usable pre-onset window (patient may already be septic at admission).'); return
    x=[feats.get(c, math.nan) for c in cols]
    x=[(v if v==v else float('nan')) for v in x]
    risk=float(m.predict_proba([x])[0,1])
    top=json.load(open(os.path.join(here,'..','results','top_features.json')))
    print(f'patient: {os.path.basename(psv)}')
    print(f'sepsis risk score: {risk:.4f}')
    print('top contributing features (global importance, patient value):')
    for name,imp in top[:5]:
        print(f'  {name}: importance {imp:.4f}, value {feats.get(name)}')
    print(f'(ground-truth label in file: {lab})' if lab==1 else '(no sepsis label in file)' if lab==0 else '')
if __name__=='__main__': main()
