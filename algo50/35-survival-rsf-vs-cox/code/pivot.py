import numpy as np,json,warnings,pandas as pd; warnings.filterwarnings('ignore')
from sksurv import datasets as d
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.ensemble import RandomSurvivalForest,GradientBoostingSurvivalAnalysis
from sksurv.metrics import concordance_index_censored,integrated_brier_score
from sksurv.column import encode_categorical
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.preprocessing import StandardScaler
def load(n):
    X,y=getattr(d,'load_'+n)(); f,t=y.dtype.names
    if n=='flchain': X=X.drop(columns=['chapter']); y=np.array(list(zip(y[f],np.ceil(y[t]/30.0))),dtype=[(f,bool),(t,float)])
    X=encode_categorical(X); return X.astype(float),y,f,t
res={}; rows=[]
for n in ['gbsg2','whas500','flchain','aids','veterans_lung_cancer']:
    X,y,f,t=load(n); E=y[f].astype(bool)
    cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=3 if n=='flchain' else 5,random_state=35)
    for k,(tr,te) in enumerate(cv.split(X,E)):
        Xtr,Xte=X.iloc[tr].copy(),X.iloc[te].copy(); med=Xtr.median(); Xtr=Xtr.fillna(med); Xte=Xte.fillna(med)
        sc=StandardScaler().fit(Xtr); Str,Ste=sc.transform(Xtr),sc.transform(Xte)
        ytr,yte=y[tr],y[te]
        ev=ytr[t][ytr[f]]; lo,hi=np.percentile(ev,[10,80]); ok0=yte[t]<ytr[t].max(); hi=min(hi,yte[t][ok0].max()-1e-6); lo=max(lo,yte[t][ok0].min())
        grid=np.linspace(lo,hi,50)
        out={'dataset':n,'fold':k}
        from scipy.stats import rankdata
        cox=CoxPHSurvivalAnalysis(alpha=1e-4,ties='breslow').fit(Str,ytr); rc=cox.predict(Ste)
        rsf=RandomSurvivalForest(n_estimators=300,min_samples_leaf=15,max_features='sqrt',n_jobs=-1,random_state=35).fit(Xtr.values,ytr); rr=rsf.predict(Xte.values)
        re=(rankdata(rc)+rankdata(rr))/(2*len(rc))
        for m,r in [('COX',rc),('RSF',rr),('ENS',re)]: out['C_'+m]=concordance_index_censored(yte[f],yte[t],r)[0]
        rows.append(out); print(out,flush=True)
df=pd.DataFrame(rows); df.to_csv('../results/pivot_fold_metrics.tsv',sep='\t',index=False)
df['dE']=df.C_ENS-df.C_COX; per={n:{'C_COX':float(g.C_COX.mean()),'C_RSF':float(g.C_RSF.mean()),'C_ENS':float(g.C_ENS.mean()),'dE':float(g.dE.mean())} for n,g in df.groupby('dataset',sort=False)}
rng=np.random.default_rng(35); G=[g for _,g in df.groupby('dataset',sort=False)]
B=[np.mean([g.dE.values[rng.integers(0,len(g),len(g))].mean() for g in G]) for _ in range(2000)]
res={'per_dataset':per,'pooled_dE':float(np.mean([p['dE'] for p in per.values()])),'ci':[float(x) for x in np.percentile(B,[2.5,97.5])],'n_ens_ge_cox':int(sum(p['dE']>=0 for p in per.values()))}
res['check_cox_matches_original']={n:p['C_COX'] for n,p in per.items()}
res['pivot_gates']={'P1':bool(res['pooled_dE']>=0.005 and res['ci'][0]>0),'P2':bool(res['n_ens_ge_cox']>=4)}
json.dump(res,open('../results/pivot_metrics.json','w'),indent=1); print(json.dumps(res,indent=1))
