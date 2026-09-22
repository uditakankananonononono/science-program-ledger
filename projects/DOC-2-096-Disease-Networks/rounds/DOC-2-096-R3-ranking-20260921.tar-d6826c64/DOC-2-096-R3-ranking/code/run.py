from pathlib import Path
import pandas as pd,numpy as np,json
from scipy.stats import rankdata
R=Path(__file__).resolve().parents[1];dev=pd.read_csv(R/'data/dev.csv');test=pd.read_csv(R/'data/test.csv');rng=np.random.default_rng(20260921)
features=['benign_burden_base','conflict_base','variants_base','p_base','b_base','reliability_base']
# orient by development Spearman-like AUC direction, freeze equal rank ensemble
orient={}
for f in features:
 x=dev[f].fillna(dev[f].median()).to_numpy();y=dev.event.to_numpy();auc=(rankdata(x)[y].sum()-y.sum()*(y.sum()+1)/2)/(y.sum()*(len(y)-y.sum()));orient[f]=1 if auc>=.5 else -1
def scores(d):
 Z=[]
 for f in features:Z.append(orient[f]*rankdata(d[f].fillna(dev[f].median()).to_numpy())/len(d))
 return np.mean(Z,axis=0)
def met(d,s):
 y=d.event.to_numpy();out={}
 for q in [.01,.05,.1]:out[f'top_{int(q*100)}_enrichment']=y[s>=np.quantile(s,1-q)].mean()/y.mean();out[f'top_{int(q*100)}_precision']=y[s>=np.quantile(s,1-q)].mean()
 order=np.argsort(-s);rel=y[order];dcg=np.sum(rel/np.log2(np.arange(len(y))+2));ideal=np.sum(np.sort(y)[::-1]/np.log2(np.arange(len(y))+2));out['ndcg']=dcg/ideal
 return out
sd= scores(dev);st=scores(test);res={'orientations':orient,'development':met(dev,sd),'replication':met(test,st)}
# condition-block bootstrap replication top10
# Cluster bootstrap collapsed to per-condition sufficient statistics at fixed top-10 threshold.
thr=np.quantile(st,.9);tmp=test[['norm','event']].copy();tmp['top']=st>=thr;A=tmp.groupby('norm').apply(lambda g:pd.Series({'n':len(g),'ev':g.event.sum(),'topn':g.top.sum(),'topev':g.loc[g.top,'event'].sum()})).to_numpy(float);vals=[]
for _ in range(1000):
 q=A[rng.integers(0,len(A),len(A))].sum(0);vals.append((q[3]/q[2])/(q[1]/q[0]))
res['replication_top10_ci']=[float(np.quantile(vals,.025)),float(np.quantile(vals,.975))]
# best simple baseline test
simple=[]
for f in features:simple.append((f,met(test,orient[f]*test[f].fillna(dev[f].median()).to_numpy())['top_10_enrichment']))
res['best_simple']=max(simple,key=lambda x:x[1]);res['ranking_pass']=bool(res['replication_top10_ci'][0]>1 and res['replication']['top_10_enrichment']>=1.2*res['best_simple'][1])
(R/'results/ranking.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
