from pathlib import Path
import pandas as pd,numpy as np,json
from scipy.special import expit
from scipy.stats import rankdata
R=Path(__file__).resolve().parents[1]
def load(n):return pd.read_csv(R/f'data/processed/edges_{n}.csv' if n!='current' else R/'data/processed/edges_current.csv')
def cohort(a,b):
 x=a.merge(b,on=['GeneSymbol','norm'],suffixes=('_base','_future'));x=x[(x.p_base+x.b_base+x.conflict_base)>=2].copy().reset_index(drop=True);x['event']=((x.conflict_base==0)&(x.conflict_future>0))|((x.high_review_base==0)&(x.high_review_future>0));return x
tr=cohort(load('2020'),load('2023'));te=cohort(load('2023'),load('current'));tr.to_csv(R/'data/processed/transition_2020_2023.csv',index=False);te.to_csv(R/'data/processed/transition_2023_current.csv',index=False)
def score(x,k):
 if k=='raw':return np.log1p(x.variants_base.to_numpy(float))
 if k=='positive_only':return x.p_base.to_numpy(float)/(x.p_base.to_numpy(float)+1)
 return 1-x.reliability_base.to_numpy(float)
def fit(z,y):
 z=(z-np.mean(z))/(np.std(z)+1e-9);X=np.c_[np.ones(len(z)),z];b=np.zeros(2)
 for _ in range(50):
  p=expit(X@b);w=np.clip(p*(1-p),1e-6,None);b+=np.linalg.solve(X.T@(w[:,None]*X),X.T@(y-p))
 return b,np.mean(z),np.std(z)+1e-9
def metrics(y,p,z):
 brier=np.mean((p-y)**2);top=y[z>=np.quantile(z,.9)].mean()/y.mean();auc=(rankdata(z)[y==1].sum()-y.sum()*(y.sum()+1)/2)/(y.sum()*(len(y)-y.sum()))
 # calibration slope/intercept on logit p
 q=np.clip(p,1e-6,1-1e-6);lp=np.log(q/(1-q));X=np.c_[np.ones(len(y)),lp];b=np.zeros(2)
 for _ in range(30):
  pr=expit(X@b);w=np.clip(pr*(1-pr),1e-6,None);b+=np.linalg.solve(X.T@(w[:,None]*X),X.T@(y-pr))
 return brier,top,auc,b[0],b[1]
rows=[]
for k in ['raw','positive_only','reliability']:
 z=score(tr,k);mu=z.mean();sd=z.std()+1e-9;zs=(z-mu)/sd;X=np.c_[np.ones(len(z)),zs];y=tr.event.astype(int).to_numpy();b=np.zeros(2)
 for _ in range(50):
  p=expit(X@b);w=np.clip(p*(1-p),1e-6,None);b+=np.linalg.solve(X.T@(w[:,None]*X),X.T@(y-p))
 for name,x in [('2020_to_2023',tr),('2023_to_current',te)]:
  zz=(score(x,k)-mu)/sd;yy=x.event.astype(int).to_numpy();pp=expit(np.c_[np.ones(len(zz)),zz]@b);m=metrics(yy,pp,zz);rows.append({'transition':name,'model':k,'edges':len(x),'events':int(yy.sum()),'brier':m[0],'top_decile_enrichment':m[1],'auc':m[2],'calibration_intercept':m[3],'calibration_slope':m[4]})
# controls on reliability for train: labels permuted within condition/source strata, ontology randomization equivalent score shuffle within source
rng=np.random.default_rng(20260921);base=[r for r in rows if r['transition']=='2020_to_2023' and r['model']=='reliability'][0]['top_decile_enrichment'];ctrl=[]
z=score(tr,'reliability');y=tr.event.to_numpy()
for typ in ['within_source_label_permutation','ontology_label_randomization']:
 vals=[]
 for _ in range(200):
  yp=y.copy()
  if typ.startswith('within'):
   for _,idx in tr.groupby('source_base').groups.items():yp[list(idx)]=rng.permutation(yp[list(idx)])
   zz=z
  else:zz=rng.permutation(z)
  vals.append(yp[zz>=np.quantile(zz,.9)].mean()/yp.mean())
 ctrl.append({'control':typ,'mean_enrichment':np.mean(vals),'loss_fraction':1-np.mean(vals)/base})
pd.DataFrame(rows).to_csv(R/'results/locked_temporal_metrics.csv',index=False);pd.DataFrame(ctrl).to_csv(R/'results/negative_controls.csv',index=False)
M=pd.DataFrame(rows);w=M.pivot(index='transition',columns='model',values='brier');imp=(w.raw-w.reliability)/w.raw;test=M[(M.transition=='2023_to_current')&(M.model=='reliability')].iloc[0];gate={'events':{'development':int(tr.event.sum()),'replication':int(te.event.sum())},'brier_improvement':imp.to_dict(),'replication_calibration_slope':test.calibration_slope,'negative_controls':ctrl,'conditions':{'min_edges_events':len(tr)>=10000 and len(te)>=10000 and tr.event.sum()>=1000 and te.event.sum()>=1000,'brier_improve_5pct_both':bool((imp>=.05).all()),'replication_slope_0_8_1_2':bool(.8<=test.calibration_slope<=1.2),'controls_lose_50pct':bool(all(x['loss_fraction']>=.5 for x in ctrl))}};gate['passed']=all(gate['conditions'].values());(R/'results/gate_decision.json').write_text(json.dumps(gate,indent=2,default=lambda x:x.item() if hasattr(x,'item') else str(x)));print(json.dumps(gate,indent=2,default=lambda x:x.item() if hasattr(x,'item') else str(x)));print(M.to_string(index=False))
