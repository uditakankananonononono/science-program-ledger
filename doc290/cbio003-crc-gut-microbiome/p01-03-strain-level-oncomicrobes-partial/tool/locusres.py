#!/usr/bin/env python3
"""P01-03 partial: does virulence-locus resolution beat genus resolution for CRC transport?
Locked before results (lock evidence = the commit adding this file, before results/ exists).
Data: frozen 767-sample / 8-cohort benchmark (P01-01; names per erratum); genus (164), mOTU species
  (849, >=5% prevalence), and per-sample log10 gene abundances clb/bft/fadA/bai from Wirbel 2019
  MOESM8 Panel_c + MOESM9 Panel_c (767/767 matched, 0 label mismatches).
Model (identical for every resolution, spec 'identical gradient-boosted classifiers'):
  HistGradientBoostingClassifier(max_iter=150, early_stopping=True, random_state=7); LOCO over the
  8 cohorts - folds are identical across resolutions by construction (G3).
Resolutions: genus | species | locus (4 genes only) | genus+locus.
G1 (locus arm): primary comparison = locus vs genus. Per held-out cohort, diff = AUC(locus) - AUC(genus);
  paired bootstrap (1000 resamples of held-out samples, stratified by label), p = fraction of
  resampled diffs <= 0. A cohort counts if diff >= 0.05 and p < 0.05. PASS iff >= 4 of 8 cohorts
  (spec: 4 of 6; this benchmark has 8 cohorts - the absolute count 4 is kept).
  Reported with the same test, no gate: genus+locus vs genus, species vs genus.
G3: all resolutions evaluated on identical folds, all four reported; no metric other than AUC.
Amendments: strain level and G2 (SBS88) not built (partial scope); loci from published tables
  instead of ShortBRED/hmmsearch on raw reads.
Usage: python3 locusres.py <data_dir> <results_dir>
"""
import sys, os, json
import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
SEED=7; data,out=sys.argv[1],sys.argv[2]; os.makedirs(out,exist_ok=True)
NAMES={'AT-Wirbel':'FR-Zeller','CN-Feng':'AT-Feng'}
M=pd.read_csv(os.path.join(data,'samples.csv'),index_col=0); M['cohort']=M.cohort.replace(NAMES)
G=pd.read_csv(os.path.join(data,'genus_matrix.csv'),index_col=0).loc[M.index]
S=pd.read_csv(os.path.join(data,'species_matrix.csv'),index_col=0).loc[M.index]; S=S.loc[:,(S.values>0).mean(0)>=0.05]
L=pd.read_csv(os.path.join(data,'locus_matrix.csv'),index_col=0).loc[M.index]
assert L.notna().all().all()
views={'genus':G.values,'species':np.log10(S.values+1e-5),'locus':L.values,'genus+locus':np.hstack([G.values,L.values])}
y=(M.label=='CRC').astype(int).values; coh=M.cohort.values; cohorts=sorted(set(coh))
pred={v:{} for v in views}
for c in cohorts:
    tr=coh!=c; te=coh==c
    for v,X in views.items():
        m=HistGradientBoostingClassifier(max_iter=150,early_stopping=True,random_state=SEED).fit(X[tr],y[tr])
        pred[v][c]=m.predict_proba(X[te])[:,1]
auc={v:{c:float(roc_auc_score(y[coh==c],pred[v][c])) for c in cohorts} for v in views}
rng=np.random.RandomState(SEED)
def paired(v,ref='genus'):
    rows={}
    for c in cohorts:
        yy=y[coh==c]; a=pred[v][c]; b=pred[ref][c]; i1=np.where(yy==1)[0]; i0=np.where(yy==0)[0]; d=[]
        for _ in range(1000):
            ii=np.r_[rng.choice(i1,len(i1)),rng.choice(i0,len(i0))]
            d.append(roc_auc_score(yy[ii],a[ii])-roc_auc_score(yy[ii],b[ii]))
        diff=auc[v][c]-auc[ref][c]; p=float(np.mean(np.array(d)<=0))
        rows[c]={'diff':float(diff),'p':p,'counts':bool(diff>=0.05 and p<0.05)}
    return rows
cmp={v:paired(v) for v in ['locus','genus+locus','species']}
res={'loco_auc':auc,'mean_loco':{v:float(np.mean(list(d.values()))) for v,d in auc.items()},'vs_genus':cmp,
     'G1':{'n_cohorts_locus_better':int(sum(r['counts'] for r in cmp['locus'].values()))},
     'gates':{'G1_pass':bool(sum(r['counts'] for r in cmp['locus'].values())>=4),'G3_identical_folds':True}}
json.dump(res,open(os.path.join(out,'results.json'),'w'),indent=1)
print(json.dumps({k:res[k] for k in ['mean_loco','G1','gates']},indent=1))
for v in cmp: print(v,{c:(round(r['diff'],3),r['p']) for c,r in cmp[v].items()})
