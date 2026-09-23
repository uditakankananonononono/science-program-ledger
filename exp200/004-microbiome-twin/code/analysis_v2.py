#!/usr/bin/env python3
import json, time
import numpy as np, pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold, KFold
from scipy.stats import mannwhitneyu
t0=time.time(); rng=np.random.default_rng(20260923)
gen=pd.read_csv('data/species.tsv',sep='\t',index_col=0)
mtb=pd.read_csv('data/mtb.tsv',sep='\t',index_col=0)
meta=pd.read_csv('data/metadata.tsv',sep='\t')
mmap=pd.read_csv('data/mtb.map.tsv',sep='\t')
print('genera',gen.shape,'mtb',mtb.shape,flush=True)
common=[s for s in gen.index if s in mtb.index]
subj=meta.set_index('Sample')['Subject']
common=[s for s in common if s in subj.index]
print('paired samples:',len(common),flush=True)
# metabolite panel rule (frozen)
det=(mtb.loc[common]>0).mean(0)
cand=det[det>=0.5].index
mv=mtb.loc[common,cand].apply(lambda c: np.log10(c[c>0]+ (c[c>0][c>0].min()/2 if (c>0).any() else 1)).var(),axis=0)
# simpler: variance of log values among detected
def lv(c):
    v=c[c>0]; 
    return np.log10(v+ v[v>0].min()/2).var() if len(v)>10 else -1
mv=mtb.loc[common,cand].apply(lv,axis=0)
panel=list(mv.sort_values(ascending=False).head(30).index)
print('panel metabolites:',len(panel),flush=True)
# genera features
prev=(gen.loc[common]>0).mean(0)
g200=prev[prev>=0.10].index
g200=gen.loc[common,g200].mean(0).sort_values(ascending=False).head(200).index
X=np.log10(gen.loc[common,g200].values+1e-4)
subjects=subj.loc[common].values
ALPHAS=[0.1,1.0,10.0,100.0,1000.0]
def run_met(mname):
    y=mtb.loc[common,mname].values.astype(float)
    detmask=y>0
    Xm=X[detmask]; ym=np.log10(y[detmask]+np.min(y[detmask])/2); sub=subjects[detmask]
    gkf=GroupKFold(5); oof=np.zeros(len(ym)); oofb=np.zeros(len(ym)); alphas=[]
    for tr,te in gkf.split(Xm,ym,groups=sub):
        Xtr,Xte=Xm[tr],Xm[te]
        mu,sd=Xtr.mean(0),Xtr.std(0)+1e-8
        Xtr,Xte=(Xtr-mu)/sd,(Xte-mu)/sd
        best,best_a=np.inf,ALPHAS[0]
        for a in ALPHAS:
            ms=[np.mean((Ridge(alpha=a).fit(Xtr[itr],ym[tr][itr]).predict(Xtr[ite])-ym[tr][ite])**2) for itr,ite in KFold(3,shuffle=True,random_state=1).split(Xtr)]
            if np.mean(ms)<best: best,best_a=np.mean(ms),a
        alphas.append(best_a)
        oof[te]=Ridge(alpha=best_a).fit(Xtr,ym[tr]).predict(Xte); oofb[te]=ym[tr].mean()
    rm=lambda p: float(np.sqrt(np.mean((p-ym)**2)))
    red=1-rm(oof)/rm(oofb)
    ss=1-np.sum((oof-ym)**2)/np.sum((ym-ym.mean())**2)
    null=[]
    for _ in range(20):
        # subject-level permutation: permute labels within fold splits (recompute split each time is fine)
        yp=rng.permutation(ym); oofp=np.zeros(len(ym))
        for k,(tr,te) in enumerate(gkf.split(Xm,ym,groups=sub)):
            Xtr,Xte=Xm[tr],Xm[te]
            mu,sd=Xtr.mean(0),Xtr.std(0)+1e-8
            oofp[te]=Ridge(alpha=alphas[k]).fit((Xtr-mu)/sd,yp[tr]).predict((Xte-mu)/sd)
        null.append(1-np.sum((oofp-yp)**2)/np.sum((yp-yp.mean())**2))
    pval=(1+sum(1 for z in null if z>=ss))/21
    return dict(metabolite=mname,n=int(detmask.sum()),rel_reduction=float(red),r2=float(ss),perm_p=float(pval))
res=[run_met(m) for m in panel]
R=pd.DataFrame(res); R.to_csv('results/v2_per_metabolite_metrics.csv',index=False)
print(R.round(3).to_string(index=False),flush=True)
# G2 classes
hc=mmap[mmap['High.Confidence.Annotation'].astype(str).str.upper()=='TRUE']
name_of={}
for _,r in hc.iterrows():
    key=str(r['Compound']).split(':')[0].strip()
    name_of[key]=str(r['Compound.Name'])
MICRO=['acetate','propionate','butyrate','valerate','isobutyrate','isovalerate','deoxychol','lithochol','ursodeoxychol','indolepropion','indoleacet','indolelact','tryptamine','putrescine','cadaverine']
def klass(m):
    nm=name_of.get(m.split(':')[0].strip(),'').lower()
    return 'microbial' if any(k in nm for k in MICRO) else 'other'
R['klass']=[klass(m) for m in R.metabolite]
R['name']=[name_of.get(m.split(':')[0].strip(),'') for m in R.metabolite]
R.to_csv('results/v2_per_metabolite_metrics.csv',index=False)
med=R.rel_reduction.median(); frac=(R.perm_p<=0.05).mean()
g1=bool(med>=0.10 and frac>=0.5)
mic=R[R.klass=='microbial'].r2; oth=R[R.klass=='other'].r2
if len(mic)>=3 and len(oth)>=3:
    U,p_mw=mannwhitneyu(mic,oth,alternative='greater'); g2=bool(p_mw<=0.05)
else:
    p_mw=float('nan'); g2=False
summary=dict(panel_n=len(panel),paired_samples=len(common),
  G1=dict(median_rel_reduction=float(med),frac_perm_sig=float(frac),PASS=g1),
  G2=dict(n_microbial=int(len(mic)),median_r2_microbial=float(mic.median()) if len(mic) else None,median_r2_other=float(oth.median()) if len(oth) else None,mannwhitney_p=float(p_mw) if p_mw==p_mw else None,PASS=g2),
  runtime_min=(time.time()-t0)/60)
json.dump(summary,open('results/v2_gate_summary.json','w'),indent=2)
print(json.dumps(summary,indent=2),flush=True)
