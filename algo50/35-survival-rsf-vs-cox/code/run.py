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
        ev=ytr[t][ytr[f]]; lo,hi=np.percentile(ev,[10,80]); hi=min(hi,yte[t].max()-1e-6); lo=max(lo,yte[t].min())
        grid=np.linspace(lo,hi,50)
        out={'dataset':n,'fold':k}
        for m,mod,A,B in [('COX',CoxPHSurvivalAnalysis(alpha=1e-4,ties='breslow'),Str,Ste),
                          ('RSF',RandomSurvivalForest(n_estimators=300,min_samples_leaf=15,max_features='sqrt',n_jobs=-1,random_state=35),Xtr.values,Xte.values),
                          ('GBM',GradientBoostingSurvivalAnalysis(random_state=35),Xtr.values,Xte.values)]:
            mod.fit(A,ytr); r=mod.predict(B)
            out['C_'+m]=concordance_index_censored(yte[f],yte[t],r)[0]
            sf=mod.predict_survival_function(B); P=np.array([s(grid) for s in sf])
            out['IBS_'+m]=integrated_brier_score(ytr,yte,P,grid)
        rows.append(out); print(out,flush=True)
df=pd.DataFrame(rows); df.to_csv('../results/fold_metrics.tsv',sep='\t',index=False)
df['dC']=df.C_RSF-df.C_COX; df['dI']=df.IBS_COX-df.IBS_RSF
per={}
for n,g in df.groupby('dataset',sort=False):
    J=len(g); nte_ntr=0.25
    def nb(v): m=v.mean(); s=np.sqrt((1/J+nte_ntr)*v.var(ddof=1)); from scipy.stats import t as T; q=T.ppf(0.975,J-1); return [float(m-q*s),float(m+q*s)]
    per[n]={k:float(g[k].mean()) for k in ['C_COX','C_RSF','C_GBM','IBS_COX','IBS_RSF','IBS_GBM','dC','dI']}; per[n]['nb_ci_dC']=nb(g.dC); per[n]['nb_ci_dI']=nb(g.dI)
res['per_dataset']=per
rng=np.random.default_rng(35); G=[g for _,g in df.groupby('dataset',sort=False)]; B=[]
for _ in range(2000):
    B.append([np.mean([g.dC.values[rng.integers(0,len(g),len(g))].mean() for g in G]),np.mean([g.dI.values[rng.integers(0,len(g),len(g))].mean() for g in G])])
B=np.array(B); ci=lambda v:[float(x) for x in np.percentile(v,[2.5,97.5])]
res['pooled_dC']=float(np.mean([p['dC'] for p in per.values()])); res['ci1']=ci(B[:,0])
res['pooled_dIBS']=float(np.mean([p['dI'] for p in per.values()])); res['ci2']=ci(B[:,1])
res['n_datasets_RSF_wins']=int(sum(p['dC']>0 for p in per.values()))
res['gates']={'G1':bool(res['pooled_dC']>=0.01 and res['ci1'][0]>0),'G2':bool(res['ci2'][0]>0),'G3':bool(res['n_datasets_RSF_wins']>=4)}
json.dump(res,open('../results/metrics.json','w'),indent=1); print(json.dumps(res,indent=1))
