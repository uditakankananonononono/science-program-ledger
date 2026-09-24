#!/usr/bin/env python3
"""ferroatlas: P02-01 is ferroptosis dysregulation a stable feature of AD brain?
Locked before results (lock evidence = the commit adding this file, before results/ exists).
Cohorts (GEO route; AMP-AD Synapse needs account + terms): one sample per subject, AD vs control only.
  GSE33000 PFC (Rosetta two-colour log ratio; Huntington's excluded) | GSE132903 middle temporal gyrus
  (Illumina) | GSE118553 temporal cortex (Illumina; AsymAD excluded) | GSE122063 temporal cortex
  (Agilent; technical replicates averaged per subject; vascular dementia excluded) | GSE48350 superior
  frontal gyrus (Affymetrix; AD from source name; controls restricted to age >= 60). GSE5281 excluded (laser-captured neurons, not bulk).
  Gene level = mean of uniquely-annotated probes (tool/extract_geo.py); raw GEO file sha256 in data/.
Gene set (locked from FerrDb V2 downloads, 2026-09-24, before any outcome): union of Validated,
  protein-coding human driver + suppressor + marker genes. Core genes (spec): GPX4, ACSL4, SLC7A11,
  FTH1, FTL, TFRC, SLC40A1.
DE per cohort: OLS z-scored expression ~ AD + age + sex; t for AD per gene (genes present in the cohort).
G1: competitive set test per cohort = two-sided Mann-Whitney of signed t, set genes
  vs all other genes (limma geneSetTest-style; ignores inter-gene correlation, stated), BH over the 5
  cohorts. A core gene is direction-consistent if its t sign agrees in >= 4 of 5 cohorts (>= 4 of the
  cohorts where measured). PASS iff set FDR < 0.05 in >= 3 cohorts AND >= 5 of 7 core genes consistent.
Meta: per core gene, DerSimonian-Laird random effects on the AD coefficient (z-scored expression), I^2.
G3: "ferroptosis dysregulation is not a stable AD feature" declared iff >= 4 of 7 core genes have
  I^2 > 75% and are not direction-consistent.
G2: LOCO over the 5 cohorts. Features z-scored within cohort. Ferroptosis model = elastic-net logistic
  (saga, l1_ratio 0.5, C 0.5, balanced) on set genes measured in all 5 cohorts + age + sex; baseline =
  same learner on age + sex only. PASS iff mean LOCO AUC >= 0.65 AND ferroptosis - baseline >= 0.03.
Amendments vs spec: GEO instead of AMP-AD (access terms); APOE not available in 4 of 5 cohorts ->
  age/sex baseline only; regions differ by cohort (one cortical region per subject).
Usage: python3 ferroatlas.py <geo_out_dir_with_npz> <data_dir> <results_dir>
"""
import sys, os, json, re
import numpy as np, pandas as pd
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score
npzdir,data,out=sys.argv[1],sys.argv[2],sys.argv[3]; os.makedirs(out,exist_ok=True)
CORE=['GPX4','ACSL4','SLC7A11','FTH1','FTL','TFRC','SLC40A1']
fd=pd.concat([pd.read_csv(os.path.join(data,f'ferrdb_{k}.csv')) for k in ['driver','suppressor','marker']])
fd=fd[(fd.confidence.str.startswith('Validat'))&(fd.uniformgenetype=='gene with protein product')]
SET=sorted(set(fd.symbol.dropna().str.strip()))
def kv(P):
    rows=[]
    for _,r in P.iterrows():
        d={}
        for c in P.columns:
            if 'characteristics' in c and isinstance(r[c],str) and ':' in r[c]:
                k,v=r[c].split(':',1); d[k.strip().lower()]=v.strip()
        rows.append(d)
    return pd.DataFrame(rows,index=P['sample'])
def load(g):
    d=np.load(os.path.join(npzdir,f'{g}_expr.npz'),allow_pickle=True)
    E=pd.DataFrame(d['X'],index=d['genes'],columns=d['samples'])
    P=pd.read_csv(os.path.join(data,f'{g}_pheno.csv')); K=kv(P); K['source']=P.set_index('sample')['source_name_ch1'].reindex(K.index).values
    K['title']=P.set_index('sample')['title'].reindex(K.index).values
    return E,K
cohorts={}
E,K=load('GSE33000'); K['ad']=K['disease status'].map({"Alzheimer's disease":1,'non-demented':0}); K['age']=K['age'].str.extract(r'(\d+)')[0].astype(float); K['sex']=(K['gender']=='male').astype(float); cohorts['GSE33000']=(E,K)
E,K=load('GSE132903'); K['ad']=K['diagnosis'].map({'AD':1,'ND':0}); K['age']=K['expired_age (years)'].str.replace('+','',regex=False).astype(float); K['sex']=(K['sex']=='male').astype(float); cohorts['GSE132903']=(E,K)
E,K=load('GSE118553'); K=K[K['tissue']=='Temporal_Cortex'].copy(); K['ad']=K['disease state'].map({'AD':1,'control':0}); K['age']=K['age'].astype(float); K['sex']=(K['gender']=='MALE').astype(float); cohorts['GSE118553']=(E,K)
E,K=load('GSE122063'); K=K[K['brain region']=='temporal cortex'].copy(); K['ad']=K['patient diagnosis'].map({"Alzheimer's disease":1,'Control':0}); K['age']=K['age'].astype(float); K['sex']=(K['sex']=='Male').astype(float)
K=K[K.ad.notna()]; grp=K.groupby('subject id'); Em=pd.DataFrame({s:E[idx].mean(1) for s,idx in grp.groups.items()}); Km=grp.first(); cohorts['GSE122063']=(Em,Km)
E,K=load('GSE48350'); K=K[K['brain region']=='superior frontal gyrus'].copy(); K['ad']=K['source'].str.contains('_AD').astype(int)
K['age']=K['age (yrs)'].astype(float); K['sex']=(K['gender']=='male').astype(float); K=K[(K.ad==1)|(K.age>=60)].copy(); cohorts['GSE48350']=(E,K)
summary={}; T={}; B={}; SEb={}
for g,(E,K) in cohorts.items():
    K=K[K.ad.notna()&K.age.notna()]; E=E[K.index].dropna(); E=E[E.var(1)>0]
    Z=((E.T-E.T.mean())/E.T.std()).values
    D=np.c_[np.ones(len(K)),K.ad.values,K.age.values,K.sex.values]
    beta,_,_,_=np.linalg.lstsq(D,Z,rcond=None); res=Z-D@beta; dof=len(K)-D.shape[1]
    s2=(res**2).sum(0)/dof; cov=np.linalg.inv(D.T@D); se=np.sqrt(s2*cov[1,1]); t=beta[1]/se
    T[g]=pd.Series(t,index=E.index); B[g]=pd.Series(beta[1],index=E.index); SEb[g]=pd.Series(se,index=E.index)
    summary[g]={'n_ad':int(K.ad.sum()),'n_ctrl':int((1-K.ad).sum()),'n_genes':int(E.shape[0]),'set_genes_present':int(E.index.isin(SET).sum())}
    cohorts[g]=(E,K)
pv={}
for g in T:
    ins=T[g].index.isin(SET); pv[g]=float(mannwhitneyu(T[g][ins],T[g][~ins]).pvalue); summary[g]['set_mean_t']=float(T[g][ins].mean()); summary[g]['other_mean_t']=float(T[g][~ins].mean())
q=dict(zip(pv,multipletests(list(pv.values()),method='fdr_bh')[1]))
core={}
for gene in CORE:
    ts={g:float(T[g][gene]) for g in T if gene in T[g].index}
    signs=np.sign(list(ts.values())); maj=max((signs>0).sum(),(signs<0).sum())
    b=np.array([B[g][gene] for g in ts]); s=np.array([SEb[g][gene] for g in ts]); w=1/s**2
    fe=(w*b).sum()/w.sum(); Q=(w*(b-fe)**2).sum(); df=len(b)-1; C=w.sum()-(w**2).sum()/w.sum()
    tau2=max(0,(Q-df)/C) if C>0 else 0; wr=1/(s**2+tau2); re=(wr*b).sum()/wr.sum(); rese=np.sqrt(1/wr.sum())
    I2=max(0,(Q-df)/Q)*100 if Q>0 else 0
    core[gene]={'t_by_cohort':ts,'consistent':bool(maj>=max(4,len(ts)-1) if len(ts)>=5 else maj>=len(ts)-1),'re_effect':float(re),'re_se':float(rese),'I2':float(I2),'n_cohorts':len(ts)}
ncons=sum(v['consistent'] for v in core.values())
g1={'set_p':pv,'set_q':q,'n_cohorts_fdr05':int(sum(v<0.05 for v in q.values())),'n_core_consistent':int(ncons)}
g3_decl=bool(sum((v['I2']>75) and not v['consistent'] for v in core.values())>=4)
# G2
common=sorted(set.intersection(*[set(E.index) for E,_ in cohorts.values()])&set(SET))
Xs=[];ys=[];cs=[];bs=[]
for g,(E,K) in cohorts.items():
    Zs=(E.loc[common].T-E.loc[common].T.mean())/E.loc[common].T.std()
    Xs.append(Zs.values); ys.append(K.ad.values.astype(int)); cs+= [g]*len(K); bs.append(np.c_[K.age.values,K.sex.values])
X=np.vstack(Xs); y=np.concatenate(ys); coh=np.array(cs); BA=np.vstack(bs); X=np.nan_to_num(X)
def en(): return make_pipeline(StandardScaler(),LogisticRegression(penalty='elasticnet',solver='saga',l1_ratio=0.5,C=0.5,class_weight='balanced',max_iter=5000))
fa={};ba={}
for g in cohorts:
    tr=coh!=g; te=coh==g
    F=np.c_[X,BA]; fa[g]=float(roc_auc_score(y[te],en().fit(F[tr],y[tr]).predict_proba(F[te])[:,1]))
    ba[g]=float(roc_auc_score(y[te],en().fit(BA[tr],y[tr]).predict_proba(BA[te])[:,1]))
fm=float(np.mean(list(fa.values()))); bm=float(np.mean(list(ba.values())))
res={'cohorts':summary,'set_size_locked':len(SET),'common_set_genes_for_classifier':len(common),'G1':g1,'core':core,
     'G2':{'ferro_loco_auc':fa,'baseline_loco_auc':ba,'ferro_mean':fm,'baseline_mean':bm,'delta':fm-bm},
     'gates':{'G1_pass':bool(g1['n_cohorts_fdr05']>=3 and ncons>=5),'G2_pass':bool(fm>=0.65 and fm-bm>=0.03),'G3_not_stable_declared':g3_decl}}
json.dump(res,open(os.path.join(out,'results.json'),'w'),indent=1)
print(json.dumps({k:res[k] for k in ['cohorts','set_size_locked','common_set_genes_for_classifier','G1','G2','gates']},indent=1))
for k,v in core.items(): print(k,{g:round(x,2) for g,x in v['t_by_cohort'].items()},'cons',v['consistent'],'I2',round(v['I2']),'re',round(v['re_effect'],3))
