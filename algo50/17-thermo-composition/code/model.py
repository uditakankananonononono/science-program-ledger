import pandas as pd, numpy as np, json
from sklearn.linear_model import RidgeCV, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold
from scipy.stats import pearsonr
AA=list('ACDEFGHIKLMNPQRSTVWY')
s=pd.read_csv('../data/selected.tsv',sep='\t'); c=pd.read_csv('../results/composition.tsv',sep='\t')
d=s.merge(c,on='upid'); F=d[AA].div(d[AA].sum(1),axis=0).values; y=d['Topt_ave'].values
iv=F[:,[AA.index(a) for a in 'IVYWREL']].sum(1).reshape(-1,1)
fams=d['family'].fillna(d['genus']).astype(str).values; uf=np.unique(fams); rng=np.random.default_rng(17); perm=dict(zip(uf,rng.permutation(len(uf)))); g=np.array([perm[f] for f in fams])
def L(): return make_pipeline(StandardScaler(),RidgeCV(alphas=[0.01,0.1,1,10,100],cv=5))
pB=np.zeros(len(y)); pL=np.zeros(len(y))
for tr,te in GroupKFold(5).split(F,y,g):
    pB[te]=LinearRegression().fit(iv[tr],y[tr]).predict(iv[te]); pL[te]=L().fit(F[tr],y[tr]).predict(F[te])
eB=np.abs(pB-y); eL=np.abs(pL-y)
res={'n':len(y),'n_families':len(uf),'MAE_B':eB.mean(),'MAE_L':eL.mean(),'r_B':pearsonr(pB,y)[0],'r_L':pearsonr(pL,y)[0]}
b=[]
for _ in range(2000):
    i=rng.integers(0,len(y),len(y)); b.append(eB[i].mean()-eL[i].mean())
res['dMAE']=res['MAE_B']-res['MAE_L']; res['dMAE_ci']=list(np.percentile(b,[2.5,97.5]))
bac=d['superkingdom'].values=='Bacteria'; arc=~bac
res['n_bac']=int(bac.sum()); res['n_arc']=int(arc.sum())
if arc.sum()>=5:
    res['G3_MAE_B']=float(np.abs(LinearRegression().fit(iv[bac],y[bac]).predict(iv[arc])-y[arc]).mean())
    res['G3_MAE_L']=float(np.abs(L().fit(F[bac],y[bac]).predict(F[arc])-y[arc]).mean())
res['gates']={'G1':bool(res['dMAE']>=1.0 and res['dMAE_ci'][0]>0),'G2':bool(res['r_L']>=0.85),'G3':bool(res.get('G3_MAE_L',1e9)<=res.get('G3_MAE_B',-1))}
pd.DataFrame({'upid':d['upid'],'y':y,'pred_B':pB,'pred_L':pL}).to_csv('../results/predictions.tsv',sep='\t',index=False)
json.dump(res,open('../results/metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
