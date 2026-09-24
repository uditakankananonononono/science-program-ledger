#!/usr/bin/env python3
"""stabl: P01-08 longitudinal stability of CRC microbiome markers + stability-weighted classifier.
Gates (spec text, frozen) operationalized and LOCKED 2026-09-24 12:52 IST before any result:
Data (curatedMetagenomicData 2021-03-31, MetaPhlAn2 species, via ExperimentHub + python rdata):
  CRC: ZellerG_2014, FengQ_2015, YachidaS_2019, ThomasAM_2018a, HanniganGD_2017 (CRC vs control only;
       same frozen tables as P01-07). Healthy longitudinal: HMP_2019_ibdmdb non-IBD controls (426
       samples, 27 subjects). Perturbed longitudinal: HMP_2019_ibdmdb IBD arm (reported, no gate).
  Antibiotic: RaymondF_2016 cephalosporin arm, paired day 7 vs day 0 (18 subjects).
Transform: v = log10(relab/100 + 1e-5), floor = -5.
Top-50 CRC markers: species at >=1% prevalence in CRC data; per-cohort univariate AUC(CRC vs
  control); ranked by |mean(AUC - 0.5)| over the 5 cohorts; top 50.
ICC: one-way random-effects ICC(1) on v across subjects (unbalanced k0), computed for every
  species present in the HMP table; species absent from HMP have no ICC.
G1: scorecard (ICC healthy, ICC IBD arm, within-subject SD, antibiotic day7-day0 mean log10 change,
    CRC effect) for all 50; PASS iff every top-50 marker has a healthy ICC.
G2: PASS iff >= 60% of the top-50 have healthy ICC >= 0.4; else "snapshot signal" limitation.
G3: LOCO over the 5 CRC cohorts, all species at >=1% prevalence as features.
    unweighted = parent RF (500 trees, balanced, seed 7). weighted = L2 logistic (C=1) on
    standardized features multiplied by w = clip(ICC,0,1) (w=0 where no ICC). Model-matched
    control (reported, no gate) = same logistic with w=1.
    Primary perturbation: add species-wise mean antibiotic log10 change (0 where species absent
    from Raymond) to held-out samples, clip at floor. Loss = clean mean LOCO AUC - perturbed.
    PASS iff weighted loss < 0.03 AND unweighted loss >= 0.05.
    Secondary (no gate): temporal noise = add one random HMP-control within-subject deviation vector
    per test sample (20 draws).
Amendments vs spec: David 2014 diet cohort is 16S (not in cMD, not shotgun) -> diet arm dropped;
  top markers taken from cMD CRC cohorts (MetaPhlAn names) rather than P01-01/P01-03 mOTU lists so
  that marker names match the longitudinal tables; stability weighting implemented via feature
  scaling in L2 logistic (RF is scale-invariant, so weights cannot enter it directly).
Usage: python3 stabl.py <data_dir> <results_dir>
"""
import sys, os, json
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
SEED=7; FL=-5.0
data,out=sys.argv[1],sys.argv[2]; os.makedirs(out,exist_ok=True)
tf=lambda A: np.log10(A/100+1e-5)
M=pd.read_csv(os.path.join(data,'crc_samples.csv'),index_col=0); M=M[M.study_condition.isin(['CRC','control'])]
A=pd.read_csv(os.path.join(data,'crc_species.csv.gz'),index_col=0).loc[M.index]
A=A.loc[:,(A.values>0).mean(0)>=0.01]; sp=np.array(A.columns); X=tf(A.values)
y=(M.study_condition=='CRC').astype(int).values; coh=M.study_name.values; cohorts=sorted(set(coh))
auc=pd.DataFrame({c:[roc_auc_score(y[coh==c],X[coh==c,j]) if np.ptp(X[coh==c,j])>0 else 0.5 for j in range(len(sp))] for c in cohorts},index=sp)
eff=(auc-0.5).mean(1); top=eff.abs().sort_values(ascending=False).index[:50]
H=pd.read_csv(os.path.join(data,'HMP_2019_ibdmdb_samples.csv'),index_col=0)
HA=pd.read_csv(os.path.join(data,'HMP_2019_ibdmdb_species.csv.gz'),index_col=0).loc[H.index]
def icc(V,subj):
    df=pd.DataFrame(V); df['s']=subj.values; g=df.groupby('s')
    n=g.size().values; k=len(n); N=n.sum(); k0=(N-(n**2).sum()/N)/(k-1)
    gm=df.drop(columns='s').mean().values; means=g.mean().values
    ssb=(n[:,None]*(means-gm)**2).sum(0); ssw=((df.drop(columns='s').values-means[pd.factorize(subj.values,sort=True)[0]])**2).sum(0)
    msb=ssb/(k-1); msw=ssw/(N-k); den=msb+(k0-1)*msw
    with np.errstate(invalid='ignore',divide='ignore'): r=np.where(den>0,(msb-msw)/den,np.nan)
    return r, np.sqrt(msw)
res={}
arms={}
for arm,cond in [('healthy','control'),('ibd','IBD')]:
    h=H[H.study_condition==cond]; h=h[h.subject_id.map(h.subject_id.value_counts())>=2]
    V=tf(HA.loc[h.index].values); r,wsd=icc(V,h.subject_id)
    arms[arm]=(pd.Series(r,index=HA.columns),pd.Series(wsd,index=HA.columns))
    res[f'{arm}_n_samples']=len(h); res[f'{arm}_n_subjects']=int(h.subject_id.nunique())
R=pd.read_csv(os.path.join(data,'RaymondF_2016_samples.csv'),index_col=0)
RA=pd.read_csv(os.path.join(data,'RaymondF_2016_species.csv.gz'),index_col=0).loc[R.index]
d0=R[R.days_from_first_collection==0].set_index('subject_id'); d7=R[(R.days_from_first_collection==7)&(R.study_condition=='cephalosporins')].set_index('subject_id')
subs=d7.index.intersection(d0.index)
i0=[R.index[(R.subject_id==s)&(R.days_from_first_collection==0)][0] for s in subs]
i7=[R.index[(R.subject_id==s)&(R.days_from_first_collection==7)&(R.study_condition=='cephalosporins')][0] for s in subs]
lfc=pd.Series((tf(RA.loc[i7].values)-tf(RA.loc[i0].values)).mean(0),index=RA.columns)
res['abx_n_subjects']=len(subs)
icc_h,wsd_h=arms['healthy']; icc_i,_=arms['ibd']
card=pd.DataFrame({'crc_effect_mean_auc_minus_0.5':eff[top],'icc_healthy':icc_h.reindex(top),'within_subject_sd_healthy':wsd_h.reindex(top),
                   'icc_ibd_arm':icc_i.reindex(top),'abx_day7_log10_change':lfc.reindex(top)},index=top)
card.index.name='species'; card.to_csv(os.path.join(out,'top50_scorecard.csv'))
has=card.icc_healthy.notna(); frac=float((card.icc_healthy>=0.4).mean())
res['G1']={'n_with_icc':int(has.sum()),'missing':card.index[~has].tolist()}
res['G2']={'frac_icc_ge_0.4':frac,'median_icc_top50':float(card.icc_healthy.median())}
# G3
w=icc_h.reindex(sp).clip(0,1).fillna(0).values
shift_abx=lfc.reindex(sp).fillna(0).values
hc=H[H.study_condition=='control']; hc=hc[hc.subject_id.map(hc.subject_id.value_counts())>=2]
HV=pd.DataFrame(tf(HA.loc[hc.index].values),index=hc.index,columns=HA.columns)
dev=(HV-HV.groupby(hc.subject_id).transform('mean')).reindex(columns=sp).fillna(0).values
def fit_pred(kind,Xtr,ytr,Xte_list):
    if kind=='rf':
        m=RandomForestClassifier(500,class_weight='balanced',random_state=SEED,n_jobs=2).fit(Xtr,ytr); return [m.predict_proba(Z)[:,1] for Z in Xte_list]
    ww=w if kind=='weighted' else np.ones(len(sp))
    sc=StandardScaler().fit(Xtr); m=LogisticRegression(C=1.0,max_iter=3000).fit(sc.transform(Xtr)*ww,ytr)
    return [m.predict_proba(sc.transform(Z)*ww)[:,1] for Z in Xte_list]
rng=np.random.RandomState(SEED); per={}
for c in cohorts:
    tr=coh!=c; te=coh==c; Xte=X[te]
    Xabx=np.maximum(Xte+shift_abx,FL)
    Xtmp=[np.maximum(Xte+dev[rng.randint(len(dev),size=te.sum())],FL) for _ in range(20)]
    per[c]={}
    for kind in ['rf','weighted','logit_unweighted']:
        ps=fit_pred(kind,X[tr],y[tr],[Xte,Xabx]+Xtmp)
        a=[roc_auc_score(y[te],p) for p in ps]
        per[c][kind]={'clean':a[0],'abx':a[1],'temporal':float(np.mean(a[2:]))}
    print(c,json.dumps(per[c]),flush=True)
def m(kind,sc): return float(np.mean([per[c][kind][sc] for c in cohorts]))
summ={k:{s:m(k,s) for s in ['clean','abx','temporal']} for k in ['rf','weighted','logit_unweighted']}
for k in summ: summ[k]['loss_abx']=summ[k]['clean']-summ[k]['abx']; summ[k]['loss_temporal']=summ[k]['clean']-summ[k]['temporal']
res['G3']={'per_cohort':per,'means':summ}
res['gates']={'G1_pass':bool(has.all()),'G2_pass':bool(frac>=0.6),
              'G3_pass':bool(summ['weighted']['loss_abx']<0.03 and summ['rf']['loss_abx']>=0.05)}
json.dump(res,open(os.path.join(out,'results.json'),'w'),indent=1,default=float)
print(json.dumps({k:res[k] for k in ['G1','G2','gates']},indent=1)); print(json.dumps(summ,indent=1))
