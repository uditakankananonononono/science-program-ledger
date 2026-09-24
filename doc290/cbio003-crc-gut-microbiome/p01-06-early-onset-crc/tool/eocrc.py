#!/usr/bin/env python3
"""eo-crc-atlas: P01-06 does early-onset CRC (<50) carry a distinct stool microbiome signal?
Gates (spec text, frozen) operationalized and LOCKED 2026-09-24 12:56 IST before any result.
Cohort list (locked, QC FIX item): all 11 curatedMetagenomicData 2021-03-31 stool CRC studies with
  per-sample age: ZellerG_2014, FengQ_2015, YachidaS_2019, ThomasAM_2018a, ThomasAM_2018b,
  ThomasAM_2019_c, HanniganGD_2017, GuptaA_2019, VogtmannE_2016, WirbelJ_2018, YuJ_2015
  (1394 samples, one per subject; MetaPhlAn2 species; CRC vs control only). EO = age < 50.
Features: log10(relab/100 + 1e-5), species at >=1% prevalence. Model: parent RF (500 trees,
  balanced, seed 7) unless stated.
G1: cohorts with >= 30 EOCRC cases get a within-cohort 5-fold CV AUC (EO cases vs controls < 50).
    PASS iff >= 2 cohorts qualify. Always reported: EO counts per cohort and, for each cohort, the
    Hanley-McNeil SE of AUC 0.70 at its EO case/young-control counts (power statement).
G2: LOCO over cohorts with >= 3 EO cases and >= 3 controls < 50. For held-out cohort c:
    EO model = EO cases vs controls < 50 from the other cohorts; LO model = cases >= 50 vs controls
    >= 50 from the other cohorts, randomly subsampled (seed 7) to the EO model's case/control counts.
    Test = EO cases vs controls < 50 in c. Held-out predictions pooled across folds -> one AUC per
    model; 2000 case/control-stratified bootstraps of the paired difference.
    PASS (distinct signal) iff EO - LO(size-matched) >= 0.05; else shared-signal null accepted.
    Also reported: LO model trained on all available LO samples (no size matching).
G3: LOCO over all 11 cohorts, all ages, CRC vs control; features OLS-residualized on age inside
    each training fold (coefficients applied to the test fold). Age confounding declared the primary
    finding iff mean LOCO AUC < 0.60. Also reported: unadjusted LOCO AUC; age-from-microbiome
    5-fold CV R^2 (RF regressor, controls only).
Amendments vs spec: entropy balancing replaced by age-stratum restriction of controls (BMI is
  missing for most samples); TCGA tissue layer not used; 'shifted' classifier (stratum thresholds)
  not separately scored because AUC is threshold-free.
Usage: python3 eocrc.py <data_dir> <results_dir>
"""
import sys, os, json
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import StratifiedKFold, KFold, cross_val_predict
from sklearn.metrics import roc_auc_score, r2_score
SEED=7
data,out=sys.argv[1],sys.argv[2]; os.makedirs(out,exist_ok=True)
M=pd.read_csv(os.path.join(data,'samples.csv'),index_col=0)
A=pd.read_csv(os.path.join(data,'species_relab.csv.gz'),index_col=0).loc[M.index]
A=A.loc[:,(A.values>0).mean(0)>=0.01]; X=np.log10(A.values/100+1e-5)
y=(M.study_condition=='CRC').astype(int).values; coh=M.study_name.values; age=M.age.values.astype(float)
eo=age<50; cohorts=sorted(set(coh))
def rf(): return RandomForestClassifier(500,class_weight='balanced',random_state=SEED,n_jobs=2)
def hm_se(a,n1,n0):
    q1=a/(2-a); q2=2*a*a/(1+a)
    return float(np.sqrt((a*(1-a)+(n1-1)*(q1-a*a)+(n0-1)*(q2-a*a))/(n1*n0))) if n1>0 and n0>0 else None
counts={c:{'eo_crc':int(((coh==c)&eo&(y==1)).sum()),'young_ctrl':int(((coh==c)&eo&(y==0)).sum()),
           'lo_crc':int(((coh==c)&~eo&(y==1)).sum()),'old_ctrl':int(((coh==c)&~eo&(y==0)).sum())} for c in cohorts}
for c in cohorts: counts[c]['se_auc0.70']=hm_se(0.70,counts[c]['eo_crc'],counts[c]['young_ctrl'])
res={'counts':counts}
g1={}
for c in cohorts:
    if counts[c]['eo_crc']>=30:
        mk=(coh==c)&eo; p=cross_val_predict(rf(),X[mk],y[mk],cv=StratifiedKFold(5,shuffle=True,random_state=SEED),method='predict_proba')[:,1]
        g1[c]=float(roc_auc_score(y[mk],p))
res['G1']={'qualifying_cohort_auc':g1,'n_qualifying':len(g1)}
# G2
elig=[c for c in cohorts if counts[c]['eo_crc']>=3 and counts[c]['young_ctrl']>=3]
rng=np.random.RandomState(SEED); P={'eo':[],'lo_matched':[],'lo_full':[]}; Y=[]; per={}
for c in elig:
    tr=coh!=c; te=(coh==c)&eo
    e_tr=tr&eo; l_tr=tr&~eo
    n1=int((e_tr&(y==1)).sum()); n0=int((e_tr&(y==0)).sum())
    l1=rng.choice(np.where(l_tr&(y==1))[0],n1,replace=False); l0=rng.choice(np.where(l_tr&(y==0))[0],n0,replace=False)
    pe=rf().fit(X[e_tr],y[e_tr]).predict_proba(X[te])[:,1]
    lm=np.r_[l1,l0]; pl=rf().fit(X[lm],y[lm]).predict_proba(X[te])[:,1]
    pf=rf().fit(X[l_tr],y[l_tr]).predict_proba(X[te])[:,1]
    P['eo'].append(pe); P['lo_matched'].append(pl); P['lo_full'].append(pf); Y.append(y[te])
    per[c]={'n_eo_crc':int(y[te].sum()),'n_young_ctrl':int((1-y[te]).sum()),
            'auc_eo':float(roc_auc_score(y[te],pe)),'auc_lo_matched':float(roc_auc_score(y[te],pl)),'auc_lo_full':float(roc_auc_score(y[te],pf))}
    print(c,per[c],flush=True)
Yp=np.concatenate(Y); Pp={k:np.concatenate(v) for k,v in P.items()}
auc={k:float(roc_auc_score(Yp,v)) for k,v in Pp.items()}
i1=np.where(Yp==1)[0]; i0=np.where(Yp==0)[0]; b=[]
for _ in range(2000):
    ii=np.r_[rng.choice(i1,len(i1)),rng.choice(i0,len(i0))]
    b.append(roc_auc_score(Yp[ii],Pp['eo'][ii])-roc_auc_score(Yp[ii],Pp['lo_matched'][ii]))
diff=auc['eo']-auc['lo_matched']
res['G2']={'eligible_cohorts':elig,'per_cohort':per,'pooled_auc':auc,'diff_eo_minus_lo_matched':diff,
           'boot95':[float(np.percentile(b,2.5)),float(np.percentile(b,97.5))],'n_eo_crc_test':int(Yp.sum()),'n_young_ctrl_test':int((1-Yp).sum())}
# G3
adj=[]; raw=[]
for c in cohorts:
    tr=coh!=c; te=coh==c
    Z=np.c_[np.ones(tr.sum()),age[tr]]; B=np.linalg.lstsq(Z,X[tr],rcond=None)[0]
    Rtr=X[tr]-Z@B; Rte=X[te]-np.c_[np.ones(te.sum()),age[te]]@B
    adj.append(roc_auc_score(y[te],rf().fit(Rtr,y[tr]).predict_proba(Rte)[:,1]))
    raw.append(roc_auc_score(y[te],rf().fit(X[tr],y[tr]).predict_proba(X[te])[:,1]))
ctl=y==0
r2=r2_score(age[ctl],cross_val_predict(RandomForestRegressor(300,random_state=SEED,n_jobs=2),X[ctl],age[ctl],cv=KFold(5,shuffle=True,random_state=SEED)))
res['G3']={'loco_auc_age_residualized':dict(zip(cohorts,map(float,adj))),'mean_adj':float(np.mean(adj)),
           'loco_auc_unadjusted':dict(zip(cohorts,map(float,raw))),'mean_raw':float(np.mean(raw)),'age_from_microbiome_r2_controls':float(r2)}
res['gates']={'G1_pass':bool(len(g1)>=2),'G2_distinct_signal':bool(diff>=0.05),'G3_age_confounding_primary':bool(np.mean(adj)<0.60)}
json.dump(res,open(os.path.join(out,'results.json'),'w'),indent=1)
print(json.dumps({k:res[k] for k in ['G1','gates']},indent=1)); print('G2',auc,diff,res['G2']['boot95']); print('G3',res['G3']['mean_adj'],res['G3']['mean_raw'],r2)
