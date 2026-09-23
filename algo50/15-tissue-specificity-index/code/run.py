import gzip, json, numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
from scipy.stats import spearmanr
g=pd.read_csv('../data/gtex_median_tpm.gct.gz',sep='\t',skiprows=2)
g['ens']=g['Name'].str.split('.').str[0]; g=g.drop_duplicates('ens').set_index('ens')
tis=[c for c in g.columns if c not in('Name','Description') and not c.startswith('Cells')]
T=g[tis].astype(float); T=T[T.max(1)>=1]
L=np.log2(T+1)
def tau(M): x=M.values; mx=x.max(1,keepdims=True); return pd.Series(((1-x/mx).sum(1))/(x.shape[1]-1),M.index)
def gini(M):
    x=np.sort(M.values,1); n=x.shape[1]; i=np.arange(1,n+1)
    return pd.Series(((2*i-n-1)*x).sum(1)/(n*x.sum(1)),M.index)
def tsi(M): x=M.values; return pd.Series(x.max(1)/x.sum(1),M.index)
def zmax(M): x=M.values; return pd.Series((x.max(1)-x.mean(1))/(x.std(1)+1e-9),M.index)
def ent(M):
    x=M.values; p=x/x.sum(1,keepdims=True); h=-(np.where(p>0,p*np.log2(np.where(p>0,p,1)),0)).sum(1)
    return pd.Series(np.log2(x.shape[1])-h,M.index)
org=pd.Series([t.split(' - ')[0] for t in tis],index=tis)
O=L.T.groupby(org).median().T
h=pd.read_csv('../data/normal_ihc_data.tsv',sep='\t',usecols=['Gene','Tissue','Level','Reliability'])
h=h[h['Reliability']!='Uncertain']
h['det']=h['Level'].isin(['Low','Medium','High'])
pt=h.groupby(['Gene','Tissue'])['det'].max().reset_index()
agg=pt.groupby('Gene')['det'].agg(['size','sum'])
agg=agg[(agg['size']>=30)&(agg['sum']>=1)]
lab=pd.Series(np.where(agg['sum']<=3,1,np.where(agg['sum']>=20,0,-1)),agg.index); lab=lab[lab>=0]
genes=lab.index.intersection(L.index); y=lab[genes].values
S={'tau_raw':tau(L),'gini_raw':gini(L),'tsi_raw':tsi(L),'zmax_raw':zmax(L),'entropy_raw':ent(L),'tau_organ':tau(O)}
S={k:v[genes].values for k,v in S.items()}
res={'n_tissues':len(tis),'n_organs':O.shape[1],'n_genes':len(genes),'n_restricted':int(y.sum()),'n_broad':int((y==0).sum())}
for k,v in S.items(): res['auroc_'+k]=roc_auc_score(y,v)
others=[k for k in S if k not in('tau_raw','tau_organ')]; best=max(others,key=lambda k:res['auroc_'+k]); res['best_other']=best
rng=np.random.default_rng(15); d1=[];d2=[]
for _ in range(2000):
    i=rng.integers(0,len(y),len(y)); a=roc_auc_score(y[i],S['tau_organ'][i])
    d1.append(a-roc_auc_score(y[i],S['tau_raw'][i])); d2.append(a-roc_auc_score(y[i],S[best][i]))
res['d_organ_raw']=res['auroc_tau_organ']-res['auroc_tau_raw']; res['ci_organ_raw']=list(np.percentile(d1,[2.5,97.5]))
res['d_organ_best']=res['auroc_tau_organ']-res['auroc_'+best]; res['ci_organ_best']=list(np.percentile(d2,[2.5,97.5]))
full=tau(O).loc[genes]; rh=[]
for _ in range(100):
    cols=rng.choice(O.columns,O.shape[1]//2,replace=False); rh.append(spearmanr(tau(O[cols]).loc[genes],full).correlation)
res['half_spearman_mean']=float(np.mean(rh)); res['half_spearman_min']=float(np.min(rh))
res['gates']={'G1':bool(res['d_organ_raw']>=0.01 and res['ci_organ_raw'][0]>0),'G2':bool(res['d_organ_best']>0 and res['ci_organ_best'][0]>0),'G3':bool(res['half_spearman_mean']>=0.80)}
json.dump(res,open('../results/metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
