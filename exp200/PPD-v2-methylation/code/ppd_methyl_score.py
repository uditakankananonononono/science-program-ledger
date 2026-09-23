#!/usr/bin/env python3
"""Score a blood 450K sample for PPD epigenetic risk (PPD-v2 panel, GSE44132-trained).
Usage: ppd_methyl_score.py sample.tsv   (two columns: probe_id<TAB>beta_value)
Prints PPD risk probability. VERIFICATION STATUS: passed internal-external batch
holdout (AUROC 0.90, n=9) + 200-perm discipline; NOT yet verified on an independent
PPD cohort (none exists publicly) - research use only."""
import json,sys,numpy as np,os
d=os.path.dirname(os.path.abspath(__file__))
P=json.load(open(os.path.join(d,'..','results','panel_full.json')))
vals={}
for line in open(sys.argv[1]):
    p=line.rstrip('\n').split('\t')
    if len(p)>=2:
        try: vals[p[0]]=float(p[1])
        except ValueError: pass
idx=[i for i,pr in enumerate(P['probes']) if pr in vals]
if len(idx)<len(P['probes'])*0.95: print(f'ERROR: only {len(idx)}/{len(P["probes"])} panel probes found');sys.exit(1)
b=np.array([vals[P['probes'][i]] for i in idx]);b=np.clip(b,1e-4,1-1e-4)
m=np.log2(b/(1-b))
mu=np.array(P['mean'])[idx];sd=np.array(P['scale'])[idx];cf=np.array(P['coef'])[idx]
z=(m-mu)/sd
logit=float(np.dot(z,cf))
print(f'PPD risk probability: {1/(1+np.exp(-logit)):.3f}')
