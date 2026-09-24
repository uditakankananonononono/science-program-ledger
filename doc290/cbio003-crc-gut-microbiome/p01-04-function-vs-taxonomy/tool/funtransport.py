#!/usr/bin/env python3
"""funtransport: P01-04 does microbial function out-transport taxonomy for CRC?
Locked pipeline (gates frozen 2026-09-24 before any model was fit):
  views: taxonomy (genus rel. abundance, 1% prevalence) | function (COG rel. abundance, 5% prevalence) | both
  model (identical across views): HistGradientBoostingClassifier(max_iter=150, early_stopping, seed=7)
  eval: LOCO over the same 8 frozen cohorts as P01-01
  G1: mean LOCO AUC(function) - mean LOCO AUC(taxonomy) >= 0.03, cohort-bootstrap 95% CI of paired diff excludes 0
  G2: mean LOCO AUC(combined) - max(single views) >= 0.02 else combination non-additive
  G3: >=10 COGs CRC-associated (per-cohort Mann-Whitney, BH FDR<0.05) in >=3 cohorts
Amendment (locked): function = COG relative abundance from the same frozen supplement
(Wirbel 2019 Suppl. Data 2) - one pipeline for all cohorts; HUMAnN3/MetaCyc rerun on
raw reads is infeasible in this environment and would mix pipelines across cohorts.
Amendment 2 (locked 2026-09-24 11:48 IST, before any result existed; all earlier runs were
OOM-killed at load/fit): HistGradientBoosting histograms over 25,684 COGs exceed the 1GB
environment. The function view therefore uses the top K=2000 COGs by mean relative abundance
in the TRAINING fold only (label-blind, recomputed per LOCO fold, drawn from the 20%-prevalence
set). Combined = genus + the same fold-specific 2000 COGs. Model settings unchanged for all views.
G3 still scans every extracted COG. K is fixed now and will not be tuned.
Usage: python3 funtransport.py <data_dir> <results_dir>
"""
import sys, json, os
import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score

from statsmodels.stats.multitest import multipletests

SEED=7
data, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
M = pd.read_csv(os.path.join(data,'samples.csv'), index_col=0)
G = pd.read_csv(os.path.join(data,'genus_matrix.csv'), index_col=0).loc[M.index]
def load_wide(path, order):
    # row-streaming float32 loader (1GB-RAM environment; pd.read_csv on 30k columns OOMs)
    import csv as _csv
    with open(path) as f:
        r = _csv.reader(f); hdr = next(r)[1:]
        ids, rows = [], []
        for row in r:
            ids.append(row[0]); rows.append(np.asarray(row[1:], dtype=np.float32))
    X = np.vstack(rows); del rows
    pos = {s:i for i,s in enumerate(ids)}
    return pd.DataFrame(X[[pos[s] for s in order]], index=list(order), columns=hdr)
C = load_wide(os.path.join(data,'cog_matrix.csv'), M.index)
y = (M['label']=='CRC').astype(int).values
coh = M['cohort'].values
cohorts = sorted(set(coh))
gm = (G.values!=0).mean(axis=0) >= 0.01
Gv, gnames = G.values[:, gm], G.columns[gm]
cm = (C.values!=0).mean(axis=0) >= 0.20  # locked amendment: 20% prevalence for the model view
Cv, cnames = C.values[:, cm], C.columns[cm]
Cv_full = C.values  # G3 scans all extracted COGs
views = ['taxonomy','function','combined']

def gbm(): return HistGradientBoostingClassifier(max_iter=150, early_stopping=True, random_state=SEED)

K = 2000
loco = {v: {} for v in views}
for c in cohorts:
    m = coh==c
    top = np.argsort(-Cv[~m].mean(axis=0))[:K]  # label-blind, training fold only
    fold_views = {'taxonomy': Gv, 'function': Cv[:, top], 'combined': np.hstack([Gv, Cv[:, top]])}
    for v, Xv in fold_views.items():
        mdl = gbm().fit(Xv[~m], y[~m])
        loco[v][c] = float(roc_auc_score(y[m], mdl.predict_proba(Xv[m])[:,1]))
mean = {v: float(np.mean(list(d.values()))) for v,d in loco.items()}
rng = np.random.RandomState(SEED)
diffs = np.array([loco['function'][c]-loco['taxonomy'][c] for c in cohorts])
boot = [rng.choice(diffs, len(diffs)).mean() for _ in range(10000)]
G1 = {'diff': float(diffs.mean()), 'boot95_ci': [float(np.percentile(boot,2.5)), float(np.percentile(boot,97.5))]}
# G3: per-cohort MW + BH FDR
rep = {}
for c in cohorts:
    m = coh==c
    sub = C.values[m]; yy = y[m]
    n1, n0 = int(yy.sum()), int((1-yy).sum())
    from scipy.stats import rankdata
    ranks = rankdata(sub, axis=0)  # average ranks, same as pandas rank()
    R1 = ranks[yy==1].sum(axis=0)
    U1 = R1 - n1*(n1+1)/2.0
    mu = n1*n0/2.0
    sd = np.sqrt(n1*n0*(n1+n0+1)/12.0)
    from scipy.stats import norm
    z = (U1-mu)/sd
    p = 2*norm.sf(np.abs(z))  # normal approx, no tie correction (locked amendment)
    q = multipletests(p, method='fdr_bh')[1]
    rep[c] = set(C.columns[q < 0.05])
from collections import Counter
nc = Counter()
for s in rep.values():
    for g in s: nc[g]+=1
rep3 = sorted(g for g,n in nc.items() if n>=3)
res = {'loco': loco, 'mean_loco': mean, 'G1': G1,
       'G3': {'n_rep_cogs_ge3cohorts': len(rep3), 'cogs': rep3[:50]},
       'gates': {'G1_pass': bool(G1['diff']>=0.03 and G1['boot95_ci'][0]>0),
                 'G2_pass': bool(mean['combined'] - max(mean['taxonomy'],mean['function']) >= 0.02),
                 'G3_pass': bool(len(rep3)>=10)},
       'combined_minus_best_single': float(mean['combined']-max(mean['taxonomy'],mean['function']))}
pd.DataFrame([(v,c,a) for v,d in loco.items() for c,a in d.items()], columns=['view','held_out_cohort','loco_auc']).to_csv(os.path.join(out,'loco_by_view.csv'), index=False)
json.dump(res, open(os.path.join(out,'results.json'),'w'), indent=1)
print(json.dumps(res, indent=1, default=str)[:3000])
