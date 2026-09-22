from pathlib import Path
import pandas as pd,numpy as np,json
from scipy.stats import rankdata
R=Path(__file__).resolve().parents[1];D=pd.read_csv(R/'data/dev.csv');T=pd.read_csv(R/'data/test.csv');features=['variants_base','p_base','benign_burden_base','reliability_base'];out=[]
def cohort(x,target):
 if target=='emergence':q=x[x.conflict_base==0].copy();q['y']=q.conflict_future>0
 elif target=='resolution':q=x[x.conflict_base>0].copy();q['y']=q.conflict_future==0
 else:q=x[x.high_review_base==0].copy();q['y']=q.high_review_future>0
 return q.reset_index(drop=True)
for target in ['emergence','resolution','upgrade']:
 d=cohort(D,target);t=cohort(T,target)
 for f in features:
  xd=d[f].fillna(d[f].median()).to_numpy();yd=d.y.to_numpy();auc=(rankdata(xd)[yd].sum()-yd.sum()*(yd.sum()+1)/2)/(yd.sum()*(len(yd)-yd.sum())) if 0<yd.sum()<len(yd) else .5;sgn=1 if auc>=.5 else -1
  for split,q in [('dev',d),('test',t)]:
   z=sgn*q[f].fillna(d[f].median()).to_numpy();y=q.y.to_numpy();top=y[z>=np.quantile(z,.9)].mean();base=y.mean();out.append({'target':target,'feature':f,'split':split,'n':len(q),'events':int(y.sum()),'prevalence':base,'top10_precision':top,'top10_enrichment':top/base if base else np.nan,'orientation':sgn})
r=pd.DataFrame(out);r.to_csv(R/'results/competing_risk_metrics.csv',index=False)
gate={}
for target in ['emergence','resolution','upgrade']:
 q=r[(r.target==target)&(r.split=='test')];best=q.loc[q.top10_enrichment.idxmax()];gate[target]={'events':int(best.events),'best_feature':best.feature,'best_enrichment':float(best.top10_enrichment),'precision_gain_pp':float(100*(best.top10_precision-best.prevalence)),'pass':False,'reason':'Outcome-specific model does not yet have condition-block CI and 20% improvement over a distinct baseline; abstain under locked rule.'}
g={'targets':gate,'passed_targets':0,'predictive_triage_closed':True};(R/'results/gate.json').write_text(json.dumps(g,indent=2));print(r.to_string(index=False));print(json.dumps(g,indent=2))
