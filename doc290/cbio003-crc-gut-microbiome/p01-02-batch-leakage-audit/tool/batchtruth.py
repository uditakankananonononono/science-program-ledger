#!/usr/bin/env python3
"""batchtruth: P01-02 adversarial batch and leakage audit of single-cohort CRC microbiome models.
Gates (spec text, frozen) and operationalization LOCKED 2026-09-24 11:55 IST before any run:
  Cohorts: the 5 discovery cohorts with per-sample ENA technical metadata (FR-Zeller, AT-Feng,
  CN-Yu, DE-Wirbel, US-Vogtmann; names per the P01-01 erratum). IT1/IT2/JP external cohorts have
  no fetched tech metadata and are excluded from all gates (stated in report).
  Tech covariates: log10 reads, log10 bases, n_runs, instrument (one-hot), batch (one-hot; CN-Yu
  source block BEFORE/AFTER, DE instrument), library layout. Constant columns dropped per cohort.
  G1: metadata-only logistic regression (standardized, C=1), stratified 5-fold CV (seed 7) per
      cohort; AUC >= 0.80 => cohort flagged CONFOUNDED in the headline table.
  G2: features = genus CLR (pseudocount 1e-6, 1% prevalence). Leakage-protected pipeline = within
      each training fold, OLS-residualize every feature on the tech covariates and apply the
      training coefficients to the test fold; then the parent's RF (500 trees, balanced class
      weights, seed 7). Observed AUC = pooled out-of-fold AUC. Null = 100 label permutations
      stratified within batch (within cohort when single batch), same pipeline. adjusted AUC =
      observed - (mean null - 0.5); p = (1 + #null >= observed)/101. PASS: adjusted >= 0.70 and p < 0.01.
  G3: per-cohort verdicts are written to results/per_cohort.csv before anything pooled; this
      build fits no pooled model.
  Also reported (descriptive, no gate): unprotected RF AUC; ComBat-style arm (per-batch location/
      scale standardization estimated on training fold) for cohorts with >1 batch.
Amendments vs spec method: no torch in environment -> gradient-reversal MLP replaced by fold-wise
  covariate residualization (same goal: remove linearly-predictable technical signal); ComBat
  without empirical-Bayes shrinkage (numpy); SRA tech metadata taken from ENA filereport (same runs).
Usage: python3 batchtruth.py <data_dir> <results_dir>
"""
import sys, os, json
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
SEED=7; NPERM=100
data,out=sys.argv[1],sys.argv[2]; os.makedirs(out,exist_ok=True)
NAMES={'AT-Wirbel':'FR-Zeller','CN-Feng':'AT-Feng'}
T=pd.read_csv(os.path.join(data,'tech_metadata.csv'),index_col=0)
T['cohort']=T['cohort'].replace(NAMES)
T=T[T.n_runs>0]
G=pd.read_csv(os.path.join(data,'genus_matrix.csv'),index_col=0).loc[T.index]
G=G.loc[:,(G.values!=0).mean(0)>=0.01]
X=np.log(G.values+1e-6); X=X-X.mean(1,keepdims=True)  # CLR
blk=pd.read_csv(os.path.join(data,'cnyu_blocks.csv'),index_col=0)['block'] if os.path.exists(os.path.join(data,'cnyu_blocks.csv')) else pd.Series(dtype=str)
T['batch']=T['instruments']
T.loc[T.index.isin(blk.index),'batch']=blk.reindex(T.index[T.index.isin(blk.index)]).values
y_all=(T['label']=='CRC').astype(int).values

def covars(t):
    D=pd.DataFrame({'lr':np.log10(t.reads),'lb':np.log10(t.bases),'nr':t.n_runs.astype(float)},index=t.index)
    for col in ['instruments','batch','layout']:
        D=D.join(pd.get_dummies(t[col],prefix=col,dtype=float))
    return D.loc[:,D.std()>0]

def resid_rf(Xc,Z,y,folds,seed=SEED):
    p=np.zeros(len(y))
    for tr,te in folds:
        Zt=np.c_[np.ones(len(tr)),Z[tr]]; B=np.linalg.lstsq(Zt,Xc[tr],rcond=None)[0]
        Rtr=Xc[tr]-Zt@B; Rte=Xc[te]-np.c_[np.ones(len(te)),Z[te]]@B
        m=RandomForestClassifier(500,class_weight='balanced',random_state=seed,n_jobs=2).fit(Rtr,y[tr])
        p[te]=m.predict_proba(Rte)[:,1]
    return roc_auc_score(y,p)

def plain_rf(Xc,y,folds,transform=None):
    p=np.zeros(len(y))
    for tr,te in folds:
        A,Bm=(Xc[tr],Xc[te]) if transform is None else transform(tr,te)
        m=RandomForestClassifier(500,class_weight='balanced',random_state=SEED,n_jobs=2).fit(A,y[tr])
        p[te]=m.predict_proba(Bm)[:,1]
    return roc_auc_score(y,p)

rows=[]
for c in sorted(T.cohort.unique()):
    mk=(T.cohort==c).values; t=T[mk]; y=y_all[mk]; Xc=X[mk]
    Zdf=covars(t); Z=StandardScaler().fit_transform(Zdf.values)
    folds=list(StratifiedKFold(5,shuffle=True,random_state=SEED).split(Xc,y))
    pm=np.zeros(len(y))
    for tr,te in folds:
        lr=LogisticRegression(C=1.0,max_iter=2000).fit(Z[tr],y[tr]); pm[te]=lr.predict_proba(Z[te])[:,1]
    meta_auc=roc_auc_score(y,pm)
    unprot=plain_rf(Xc,y,folds)
    batches=t['batch'].values; nb=len(set(batches))
    combat=None
    if nb>1:
        def tf(tr,te):
            A=Xc[tr].copy(); Bm=Xc[te].copy()
            for b in set(batches):
                itr=batches[tr]==b; ite=batches[te]==b
                if itr.sum()<2: continue
                mu=Xc[tr][itr].mean(0); sd=Xc[tr][itr].std(0)+1e-6
                A[itr]=(Xc[tr][itr]-mu)/sd; Bm[ite]=(Xc[te][ite]-mu)/sd
            return A,Bm
        combat=plain_rf(Xc,y,folds,tf)
    obs=resid_rf(Xc,Z,y,folds)
    rng=np.random.RandomState(SEED); null=[]
    for i in range(NPERM):
        yp=y.copy()
        for b in set(batches):
            ix=np.where(batches==b)[0]; yp[ix]=rng.permutation(y[ix])
        fp=list(StratifiedKFold(5,shuffle=True,random_state=SEED).split(Xc,yp))
        null.append(resid_rf(Xc,Z,yp,fp))
    null=np.array(null); adj=obs-(null.mean()-0.5); p=(1+(null>=obs).sum())/(NPERM+1)
    r=dict(cohort=c,n=len(y),n_crc=int(y.sum()),n_batches=nb,tech_covariates=';'.join(Zdf.columns),
           meta_only_auc=meta_auc,G1_confounded=bool(meta_auc>=0.80),unprotected_rf_auc=unprot,
           combat_rf_auc=combat,residualized_rf_auc=obs,null_mean=float(null.mean()),
           null_95=float(np.percentile(null,95)),adjusted_auc=float(adj),perm_p=float(p),
           G2_pass=bool(adj>=0.70 and p<0.01))
    rows.append(r); print(json.dumps(r),flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(out,'per_cohort.csv'),index=False)
R=pd.DataFrame(rows)
summ={'G1_flagged_confounded':R.loc[R.G1_confounded,'cohort'].tolist(),
      'G2_pass':R.loc[R.G2_pass,'cohort'].tolist(),'G2_fail':R.loc[~R.G2_pass,'cohort'].tolist(),
      'G3':'per-cohort verdicts only; no pooled model fit','n_perm':NPERM}
json.dump(summ,open(os.path.join(out,'summary.json'),'w'),indent=1); print(json.dumps(summ))
