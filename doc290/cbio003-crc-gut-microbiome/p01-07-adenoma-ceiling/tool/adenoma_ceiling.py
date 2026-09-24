#!/usr/bin/env python3
"""adenoma-ceiling: P01-07 can stool metagenomes detect (advanced) adenomas?
Gates (spec text, frozen) operationalized and LOCKED 2026-09-24 12:15 IST before any model was fit:
Data: curatedMetagenomicData (2021-03-31 release, ExperimentHub EH5938/EH5530/EH5902/EH5842/EH5566)
  MetaPhlAn2 species relative abundance + cMD sampleMetadata for ZellerG_2014, FengQ_2015,
  YachidaS_2019, ThomasAM_2018a, HanniganGD_2017 (adenoma, control, CRC only; Yachida
  carcinoma_surgery_history excluded). One sample per subject (verified).
Model (all tasks): RandomForest 500 trees, class_weight balanced, seed 7 (parent recipe, as P01-01),
  features log10(relab/100 + 1e-5), species present in >= 1% of samples.
G1: adenoma-vs-control model trained leave-one-cohort-out on ALL adenoma labels of the other 4
    cohorts (advanced labels are too scarce to train on alone); evaluated on ADVANCED adenomas vs
    controls of the held-out cohorts that label them: FengQ_2015 (advancedadenoma, 47) and
    ZellerG_2014 (largeadenoma, 15; >=1cm treated as advanced). G1 statistic = mean of these two
    held-out AUCs; 95% CI from 2000 stratified within-cohort sample bootstraps.
    PASS: mean >= 0.65 and CI lower bound > 0.55. Secondary (no gate): any-adenoma LOCO AUC, all 5.
G2: continuum. Carcinoma-vs-control model trained LOCO (other 4 cohorts); in held-out cohort,
    one-sided Mann-Whitney adenoma > control AND CRC > adenoma, both p < 0.05 => continuum in that
    cohort. PASS: >= 3 of 5 cohorts. (Spec 'paired test' -> two one-sided unpaired MW: groups are
    different people, no pairing exists.)
G3: species with adenoma-vs-control two-sided MW BH-FDR < 0.1 (within cohort, over tested species)
    and the same effect direction as that cohort's CRC-vs-control median shift, in >= 2 cohorts
    with consistent direction across those cohorts. PASS: >= 3 such species.
Amendments vs spec method: three-group ordinal classifier -> the two binary models above;
  pathway-restricted model (genotoxin/inflammation modules) not run (species-level build only);
  Yachida 'adenoma' in cMD is not advanced-labelled, so it enters training/G2/G3 but not G1 eval.
Usage: python3 adenoma_ceiling.py <data_dir> <results_dir>
"""
import sys, os, json
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests
SEED=7
data,out=sys.argv[1],sys.argv[2]; os.makedirs(out,exist_ok=True)
M=pd.read_csv(os.path.join(data,'samples.csv'),index_col=0)
A=pd.read_csv(os.path.join(data,'species_relab.csv.gz'),index_col=0).loc[M.index]
assert M.subject_id.is_unique
A=A.loc[:,(A.values>0).mean(0)>=0.01]
X=np.log10(A.values/100+1e-5)
coh=M.study_name.values; cond=M.study_condition.values; sub=M.disease_subtype.fillna('').values
cohorts=sorted(set(coh))
def rf(): return RandomForestClassifier(500,class_weight='balanced',random_state=SEED,n_jobs=2)
res={'n_by_cohort':M.groupby(['study_name','study_condition']).size().unstack(fill_value=0).to_dict('index')}
# G1 + secondary
adv={'FengQ_2015':'advancedadenoma','ZellerG_2014':'largeadenoma'}
any_auc={}; adv_pred={}
for c in cohorts:
    tr=(coh!=c)&np.isin(cond,['adenoma','control']); te=(coh==c)&np.isin(cond,['adenoma','control'])
    m=rf().fit(X[tr],(cond[tr]=='adenoma').astype(int)); p=m.predict_proba(X[te])[:,1]
    yt=(cond[te]=='adenoma').astype(int); any_auc[c]=float(roc_auc_score(yt,p))
    if c in adv:
        keep=(cond[te]=='control')|(sub[te]==adv[c])
        adv_pred[c]=(yt[keep],p[keep])
adv_auc={c:float(roc_auc_score(*v)) for c,v in adv_pred.items()}
rng=np.random.RandomState(SEED); boots=[]
for _ in range(2000):
    vals=[]
    for c,(yy,pp) in adv_pred.items():
        i1=rng.choice(np.where(yy==1)[0],(yy==1).sum()); i0=rng.choice(np.where(yy==0)[0],(yy==0).sum())
        ii=np.r_[i1,i0]; vals.append(roc_auc_score(yy[ii],pp[ii]))
    boots.append(np.mean(vals))
g1=float(np.mean(list(adv_auc.values()))); ci=[float(np.percentile(boots,2.5)),float(np.percentile(boots,97.5))]
res['G1']={'advanced_auc_by_cohort':adv_auc,'mean':g1,'boot95_ci':ci,'n_advanced':{c:int(v[0].sum()) for c,v in adv_pred.items()},
           'secondary_any_adenoma_loco_auc':any_auc,'secondary_mean':float(np.mean(list(any_auc.values())))}
# G2 continuum
cont={}
for c in cohorts:
    tr=(coh!=c)&np.isin(cond,['CRC','control'])
    m=rf().fit(X[tr],(cond[tr]=='CRC').astype(int))
    te=coh==c; s=m.predict_proba(X[te])[:,1]; cc=cond[te]
    p1=mannwhitneyu(s[cc=='adenoma'],s[cc=='control'],alternative='greater').pvalue
    p2=mannwhitneyu(s[cc=='CRC'],s[cc=='adenoma'],alternative='greater').pvalue
    cont[c]={'p_adenoma_gt_control':float(p1),'p_crc_gt_adenoma':float(p2),
             'median_score':{g:float(np.median(s[cc==g])) for g in ['control','adenoma','CRC']},
             'continuum':bool(p1<0.05 and p2<0.05)}
res['G2']={'by_cohort':cont,'n_cohorts_continuum':int(sum(v['continuum'] for v in cont.values()))}
# G3 stage-consistent markers
hits={}
for c in cohorts:
    mc=coh==c; Xa=X[mc&(cond=='adenoma')]; Xn=X[mc&(cond=='control')]; Xc=X[mc&(cond=='CRC')]
    ps=np.array([mannwhitneyu(Xa[:,j],Xn[:,j]).pvalue if np.ptp(np.r_[Xa[:,j],Xn[:,j]])>0 else 1.0 for j in range(X.shape[1])])
    q=multipletests(ps,method='fdr_bh')[1]
    da=np.sign(np.median(Xa,0)-np.median(Xn,0)+1e-12*(Xa.mean(0)-Xn.mean(0)))
    dc=np.sign(np.median(Xc,0)-np.median(Xn,0)+1e-12*(Xc.mean(0)-Xn.mean(0)))
    for j in np.where((q<0.1)&(da==dc)&(da!=0))[0]:
        hits.setdefault(A.columns[j],[]).append((c,int(da[j])))
stage=sorted(k for k,v in hits.items() if len(v)>=2 and len({d for _,d in v})==1)
res['G3']={'stage_consistent_species':stage,'n':len(stage),'all_hits':hits}
res['gates']={'G1_pass':bool(g1>=0.65 and ci[0]>0.55),'G2_pass':bool(res['G2']['n_cohorts_continuum']>=3),'G3_pass':bool(len(stage)>=3)}
json.dump(res,open(os.path.join(out,'results.json'),'w'),indent=1,default=str)
print(json.dumps({k:res[k] for k in ['G1','gates']},indent=1)); print('G2',res['G2']['n_cohorts_continuum'],'G3',stage)
