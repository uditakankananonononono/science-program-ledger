import pandas as pd,numpy as np,pathlib,json
from sklearn.model_selection import RepeatedStratifiedKFold,StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,average_precision_score,balanced_accuracy_score,roc_curve
B=pathlib.Path(__file__).resolve().parents[1];d=pd.read_csv(B/'data/processed/cohort_features.csv');y=d.label.values
cov=['length','hydrophobic_fraction','charged_fraction','aromatic_fraction','low_complexity_fraction'];agg=['agg_max','agg_fraction_ge2','agg_top5_mean'];X0=d[cov].values;X1=d[cov+agg].values;Cs=[.01,.1,1,10]
def fitpred(X,tr,te,yy):
 sc=StandardScaler().fit(X[tr]);a=sc.transform(X[tr]);b=sc.transform(X[te]);inn=StratifiedKFold(4,shuffle=True,random_state=60060);score={c:[] for c in Cs}
 for ia,ib in inn.split(a,yy[tr]):
  for c in Cs:score[c].append(roc_auc_score(yy[tr][ib],LogisticRegression(C=c,class_weight='balanced',max_iter=2000,random_state=60060).fit(a[ia],yy[tr][ia]).predict_proba(a[ib])[:,1]))
 c=max(Cs,key=lambda z:(np.mean(score[z]),-z));m=LogisticRegression(C=c,class_weight='balanced',max_iter=2000,random_state=60060).fit(a,yy[tr]);pr=m.predict_proba(b)[:,1];ptr=m.predict_proba(a)[:,1];f,t,th=roc_curve(yy[tr],ptr);thr=th[np.argmax(t-f)];return pr,(pr>=thr),c
cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=10,random_state=60060);rec=[];pred={k:np.zeros((10,len(y))) for k in ['covariate','aggregation','permuted']}
for fold,(tr,te) in enumerate(cv.split(X0,y)):
 rep=fold//5
 for name,X,yy in [('covariate',X0,y),('aggregation',X1,y)]:
  p,q,c=fitpred(X,tr,te,yy);pred[name][rep,te]=p;rec.append({'repeat':rep,'fold':fold%5,'model':name,'auroc':roc_auc_score(y[te],p),'auprc':average_precision_score(y[te],p),'balanced_accuracy':balanced_accuracy_score(y[te],q),'C':c})
 # permute within length quartiles globally per repeat/fold deterministically
 rng=np.random.default_rng(60060+fold);yp=y.copy();bins=pd.qcut(d.length,4,duplicates='drop')
 for b in bins.unique():
  ix=np.where(bins==b)[0];yp[ix]=rng.permutation(yp[ix])
 p,q,c=fitpred(X1,tr,te,yp);pred['permuted'][rep,te]=p;rec.append({'repeat':rep,'fold':fold%5,'model':'permuted','auroc':roc_auc_score(yp[te],p),'auprc':average_precision_score(yp[te],p),'balanced_accuracy':balanced_accuracy_score(yp[te],q),'C':c})
r=pd.DataFrame(rec);r.to_csv(B/'results/fold_metrics.csv',index=False)
rows=[]
for name in pred:
 for rep in range(10):rows.append({'repeat':rep,'model':name,'auroc':roc_auc_score(y if name!='permuted' else y,pred[name][rep]),'auprc':average_precision_score(y if name!='permuted' else y,pred[name][rep])})
# only true-label model comparisons from out-of-fold predictions, average repeat scores
s=r.groupby('model')[['auroc','auprc','balanced_accuracy']].mean().reset_index();s.to_csv(B/'results/summary_metrics.csv',index=False)
# bootstrap proteins, compare mean predictions over repeats to avoid pseudoreplicating repeats
p0=pred['covariate'].mean(0);p1=pred['aggregation'].mean(0);rng=np.random.default_rng(60060);diff=[]
for _ in range(10000):
 ix=rng.integers(0,len(y),len(y));
 if len(np.unique(y[ix]))<2:continue
 diff.append(roc_auc_score(y[ix],p1[ix])-roc_auc_score(y[ix],p0[ix]))
obs=roc_auc_score(y,p1)-roc_auc_score(y,p0);ci=np.quantile(diff,[.025,.975]);obj={'covariate_auroc':roc_auc_score(y,p0),'aggregation_auroc':roc_auc_score(y,p1),'aggregation_minus_covariate':obs,'bootstrap_95_ci':ci.tolist(),'success':bool(obs>=.05 and ci[0]>0),'permuted_mean_fold_auroc':float(s[s.model=='permuted'].auroc.iloc[0]),'sanity_pass':bool(.45<=s[s.model=='permuted'].auroc.iloc[0]<=.55),'seed':60060,'bootstrap_resamples':len(diff)}
(B/'results/primary_inference.json').write_text(json.dumps(obj,indent=2)+'\n');np.savez(B/'results/oof_predictions.npz',**pred,y=y)
print(s.to_string(index=False));print(obj)
