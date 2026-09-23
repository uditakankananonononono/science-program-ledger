#!/usr/bin/env python3
"""DOC-1-004 tool: predict fecal metabolite levels from a genus profile.
Usage: twin_cli.py --profile <csv: genus_fullname,rel_abundance> [--out json]
Ships models only for metabolites that beat the permutation null at genus level;
abstains when the input profile is far from the training cohort."""
import argparse, json, pickle, gzip
import numpy as np, pandas as pd
p=argparse.ArgumentParser(); p.add_argument('--profile',required=True); a=p.parse_args()
art=pickle.load(gzip.open('results/twin_models.pkl.gz','rb'))
prof=pd.read_csv(a.profile,names=['genus','value']).set_index('genus')['value']
x=np.array([np.log10(prof.get(g,0)+1e-4) for g in art['genera']],dtype=np.float32)
z=(x-art['mu'])/art['sd']
dist=float(((z-art['centroid'])**2).mean())
abstain=dist>art['dist_threshold']
out={}
for mname,m in art['models'].items():
    pred=float(m['coef']@z+m['intercept'])
    out[mname]=dict(log10_level=round(pred,3), abstain=abstain, cv_r2=m['cv_r2'])
print(json.dumps(dict(predictions=out, abstain=abstain, profile_distance=round(dist,1), note='models only for permutation-significant metabolites; log10(intensity+half-min) scale')))
