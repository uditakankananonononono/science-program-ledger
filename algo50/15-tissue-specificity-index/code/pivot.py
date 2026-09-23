exec(open('run.py').read().split("lab=pd.Series")[0])
from scipy.stats import spearmanr
Sa={'tau_raw':tau(L),'gini_raw':gini(L),'entropy_raw':ent(L),'zmax_raw':zmax(L),'tau_organ':tau(O)}
lab=pd.Series(np.where(agg['sum']<=3,1,np.where(agg['sum']>=20,-1,0)),agg.index); lab=lab[lab>=0]
genes=lab.index.intersection(L.index); y=lab[genes].values
S={k:v[genes].values for k,v in Sa.items()}
res={'n_restricted':int(y.sum()),'n_intermediate':int((y==0).sum())}
for k,v in S.items(): res['auroc_RvI_'+k]=roc_auc_score(y,v)
rng=np.random.default_rng(15); d=[]
for _ in range(2000):
    i=rng.integers(0,len(y),len(y)); d.append(roc_auc_score(y[i],S['tau_organ'][i])-roc_auc_score(y[i],S['tau_raw'][i]))
res['d_organ_raw']=res['auroc_RvI_tau_organ']-res['auroc_RvI_tau_raw']; res['ci']=list(np.percentile(d,[2.5,97.5]))
# G3 with NaN fix, on original Restricted+Broad gene set
lab0=pd.Series(np.where(agg['sum']<=3,1,np.where(agg['sum']>=20,0,-1)),agg.index); g0=lab0[lab0>=0].index.intersection(L.index)
full=tau(O).loc[g0]; rh=[]
rng3=np.random.default_rng(15)
for _ in range(100):
    cols=rng3.choice(O.columns,O.shape[1]//2,replace=False); rh.append(spearmanr(tau(O[cols]).loc[g0],full,nan_policy='omit').correlation)
res['G3_half_spearman_mean']=float(np.mean(rh)); res['G3_half_spearman_min']=float(np.min(rh)); res['G3']=bool(np.mean(rh)>=0.80)
res['pivot_gates']={'P1':bool(res['d_organ_raw']>=0.01 and res['ci'][0]>0),'P2':bool(all(res['auroc_RvI_tau_organ']>res['auroc_RvI_'+k] for k in ('gini_raw','entropy_raw','zmax_raw')))}
json.dump(res,open('../results/pivot_metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
