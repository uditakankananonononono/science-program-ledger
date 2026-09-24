#!/usr/bin/env python3
"""metabolite_predict.py - predict fecal metabolite levels from a metagenome.

Input : HUMAnN2 genefamilies.tsv (one sample) - rows 'UniRef90_XXX<tab>RPK',
        stratified rows (containing '|') are ignored.
Output: TSV 'compound<TAB>predicted_level' (80 metabolites, model units).

Model : per-metabolite ridge (alpha=1000, LOO-CV grid pick) on log1p(x*1e6)
        UniRef90 relative-abundance features, trained on PRISM (n=157).
        Cross-cohort (HMP2) skill: 30.0% of metabolites well-predicted
        (Spearman>=0.3), mean rho 0.236 - see REPORT.md before relying on it.
Usage : python3 metabolite_predict.py genefamilies.tsv > predictions.tsv
"""
import sys, numpy as np, os

MODEL = os.path.join(os.path.dirname(__file__), '..', 'results', 'armB_prism_model.npz')

def main(path):
    z = np.load(MODEL)
    feats, W, b = z['feats'], z['W'], z['b']
    fidx = {f: i for i, f in enumerate(feats)}
    vals, tot = {}, 0.0
    with open(path) as fh:
        for line in fh:
            if line.startswith('#'): continue
            p = line.rstrip('\n').split('\t')
            if len(p) < 2 or '|' in p[0]: continue
            try: v = float(p[1])
            except ValueError: continue
            vals[p[0]] = v; tot += v
    if tot <= 0:
        sys.exit('no unstratified UniRef90 rows found in %s' % path)
    x = np.zeros(len(feats))
    for f, v in vals.items():
        if f in fidx: x[fidx[f]] = v / tot
    pred = np.log1p(x * 1e6) @ W + b
    for c, v in zip(z['compounds'], pred):
        print('%s\t%.6g' % (c, v))

if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])
