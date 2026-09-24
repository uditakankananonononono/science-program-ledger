#!/usr/bin/env python3
"""panelpick: P01-05 minimal qPCR-ready CRC microbial panel.
Gates (spec text, frozen) operationalized and LOCKED 2026-09-24 12:20 IST before any model was fit:
Data: Wirbel 2019 Suppl. Data 1 mOTU species relative abundance, same 767 samples / 8 cohorts as
  P01-01 (alignment spot-checked 10/10). Cohort names corrected per P01-01 erratum.
Features: log10(relab + 1e-5); species present in >=5% of samples.
Full reference model: RF 500 trees balanced seed 7 on all species; LOCO mean AUC over 8 cohorts.
Panel pipeline, fully NESTED inside each outer LOCO fold (held-out cohort never used for selection):
  1. replication filter: species with per-cohort two-sided MW BH-FDR<0.05 in >=3 training cohorts.
  2. stability selection: 1000 half-subsamples of the training set, L1 logistic (C=0.1, standardized),
     selection frequency per replicated species.
  3. G3 exclusion (before greedy): drop species flagged batch-confounded = (a) Spearman |rho|>=0.3
     with log10 read count among CONTROLS in >=2 of the 5 discovery cohorts with ENA tech metadata
     (P01-02 data/tech_metadata.csv), or (b) replicated only through cohorts P01-02 flagged
     CONFOUNDED (meta-only AUC >= 0.80), if any.
  4. greedy forward selection, budget 8, candidates = top 30 by stability frequency, objective =
     inner LOCO mean AUC over the 7 training cohorts; panel model = L2 logistic (C=1, standardized)
     on log10 abundances (qPCR readouts are scored linearly). Stop at 8 targets (no early stop).
  5. evaluate the 8-target panel (and each prefix size 1..8, ceiling curve) on the held-out cohort.
G1: panel mean LOCO AUC >= 0.90 x full-model mean LOCO AUC AND >= 0.70.
G2: qPCR noise on held-out features only: + N(0, 0.301) in log10 (Ct SD 1.0 = 1 log2 unit) and 5%
    of non-floor values set to the floor (1e-5) as LOD dropout; 20 noise draws; degradation = clean
    mean LOCO AUC - noisy mean LOCO AUC. PASS: < 0.05.
G3: final panels contain no flagged species (enforced by step 3; flagged list reported).
Amendments vs spec: 16S cross-platform penalty and primer drafting not run (no 16S cohort frozen;
  primers need wet-lab validation) - report lists published qPCR assays only where found; cost model
  descriptive. Stability selection uses L1 logistic, not an unspecified learner.
Usage: python3 panelpick.py <data_dir> <results_dir> <p01-02 tech_metadata.csv> [<p01-02 per_cohort.csv>]
"""
import sys, os, json
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score
from scipy.stats import mannwhitneyu, spearmanr
from statsmodels.stats.multitest import multipletests
SEED=7; NSS=1000; K=8; NCAND=30
data,out,techf=sys.argv[1],sys.argv[2],sys.argv[3]; p02=sys.argv[4] if len(sys.argv)>4 else None
os.makedirs(out,exist_ok=True)
NAMES={'AT-Wirbel':'FR-Zeller','CN-Feng':'AT-Feng'}
M=pd.read_csv(os.path.join(data,'samples.csv'),index_col=0); M['cohort']=M.cohort.replace(NAMES)
S=pd.read_csv(os.path.join(data,'species_matrix.csv'),index_col=0).loc[M.index]
S=S.loc[:,(S.values>0).mean(0)>=0.05]
X=np.log10(S.values+1e-5); names=np.array(S.columns)
y=(M.label=='CRC').astype(int).values; coh=M.cohort.values; cohorts=sorted(set(coh))
rng=np.random.RandomState(SEED)
# confound flags (step 3a), label-free w.r.t. CRC? uses controls only
T=pd.read_csv(techf,index_col=0); T['cohort']=T.cohort.replace(NAMES); T=T[T.n_runs>0]
cnt=np.zeros(X.shape[1],int)
for c in sorted(T.cohort.unique()):
    ids=T.index[(T.cohort==c)&(T.label=='CTR')]; ix=M.index.get_indexer(ids)
    lr=np.log10(T.loc[ids,'reads'].values)
    for j in range(X.shape[1]):
        v=X[ix,j]
        if np.ptp(v)>0 and abs(spearmanr(v,lr)[0])>=0.3: cnt[j]+=1
flag_a=set(names[cnt>=2])
conf_coh=set()
if p02 and os.path.exists(p02):
    P=pd.read_csv(p02); conf_coh=set(P.loc[P.G1_confounded,'cohort'])
def lr_model(): return make_pipeline(StandardScaler(),LogisticRegression(C=1.0,max_iter=2000))
def loco_auc(Xs,idx_cohorts,mask):
    aucs=[]
    for c in idx_cohorts:
        tr=mask&(coh!=c); te=mask&(coh==c)
        m=lr_model().fit(Xs[tr],y[tr]); aucs.append(roc_auc_score(y[te],m.predict_proba(Xs[te])[:,1]))
    return float(np.mean(aucs))
def noisy(Xte,r):
    Z=Xte+r.normal(0,0.301,Xte.shape); floor=np.log10(1e-5)
    nz=Xte>floor; drop=nz&(r.rand(*Xte.shape)<0.05); Z[drop]=floor; Z[Xte<=floor]=floor
    return np.maximum(Z,floor)
full={}; outer=[]
for c in cohorts:
    tr=coh!=c; te=coh==c
    full[c]=float(roc_auc_score(y[te],RandomForestClassifier(500,class_weight='balanced',random_state=SEED,n_jobs=2).fit(X[tr],y[tr]).predict_proba(X[te])[:,1]))
    tcs=[k for k in cohorts if k!=c]; rep={}
    for k in tcs:
        mk=coh==k; ps=[mannwhitneyu(X[mk&(y==1),j],X[mk&(y==0),j]).pvalue if np.ptp(X[mk,j])>0 else 1.0 for j in range(X.shape[1])]
        q=multipletests(ps,method='fdr_bh')[1]
        for j in np.where(q<0.05)[0]: rep.setdefault(j,set()).add(k)
    repl=[j for j,s in rep.items() if len(s)>=3]
    flag_b={names[j] for j in repl if rep[j]<=conf_coh and len(conf_coh)>0}
    freq=np.zeros(len(repl)); Xr=X[:,repl]; tri=np.where(tr)[0]
    for b in range(NSS):
        sub=rng.choice(tri,len(tri)//2,replace=False)
        m=make_pipeline(StandardScaler(),LogisticRegression(penalty='l1',C=0.1,solver='liblinear')).fit(Xr[sub],y[sub])
        freq+=(m[-1].coef_[0]!=0)
    freq/=NSS
    order=[repl[i] for i in np.argsort(-freq)]
    cand=[j for j in order if names[j] not in flag_a and names[j] not in flag_b][:NCAND]
    panel=[]; inner_path=[]
    for step in range(K):
        best=None
        for j in cand:
            if j in panel: continue
            a=loco_auc(X[:,panel+[j]],tcs,tr)
            if best is None or a>best[1]: best=(j,a)
        if best is None: break
        panel.append(best[0]); inner_path.append(best[1])
    curve=[]
    for k in range(1,len(panel)+1):
        m=lr_model().fit(X[tr][:,panel[:k]],y[tr]); curve.append(float(roc_auc_score(y[te],m.predict_proba(X[te][:,panel[:k]])[:,1])))
    m=lr_model().fit(X[tr][:,panel],y[tr]); r=np.random.RandomState(SEED)
    nz=[float(roc_auc_score(y[te],m.predict_proba(noisy(X[te][:,panel],r))[:,1])) for _ in range(20)]
    outer.append(dict(cohort=c,full_rf_auc=full[c],panel=[names[j] for j in panel],panel_auc=curve[-1],curve=curve,
        noisy_auc_mean=float(np.mean(nz)),n_replicated=len(repl),stability_top10=[(names[order[i]],float(np.sort(freq)[::-1][i])) for i in range(min(10,len(order)))],
        flagged_excluded=[names[j] for j in order if names[j] in flag_a or names[j] in flag_b]))
    print(json.dumps({k:outer[-1][k] for k in ['cohort','full_rf_auc','panel_auc','noisy_auc_mean']}),flush=True)
    json.dump(outer,open(os.path.join(out,'per_fold.json'),'w'),indent=1)
fm=float(np.mean([o['full_rf_auc'] for o in outer])); pm=float(np.mean([o['panel_auc'] for o in outer])); nm=float(np.mean([o['noisy_auc_mean'] for o in outer]))
curve_mean=[float(np.mean([o['curve'][k] for o in outer if len(o['curve'])>k])) for k in range(K)]
from collections import Counter
freqpanel=Counter(s for o in outer for s in o['panel'])
res={'full_mean_loco':fm,'panel_mean_loco':pm,'ratio':pm/fm,'noisy_mean_loco':nm,'degradation':pm-nm,
     'ceiling_curve_mean_auc_by_size':curve_mean,'species_in_panels_count':freqpanel.most_common(),
     'flag_a_readdepth':sorted(flag_a),'confounded_cohorts_from_p01_02':sorted(conf_coh),
     'gates':{'G1_pass':bool(pm>=0.9*fm and pm>=0.70),'G2_pass':bool(pm-nm<0.05),
              'G3_pass':bool(not any(s in flag_a for o in outer for s in o['panel']))}}
json.dump(res,open(os.path.join(out,'results.json'),'w'),indent=1); print(json.dumps(res,indent=1)[:2500])
