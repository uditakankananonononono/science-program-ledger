from pathlib import Path
import pandas as pd,numpy as np,json
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score
R=Path(__file__).resolve().parents[2];O=R/'experiment/results';d=pd.read_csv(O/'audit_configurations.csv');dims=['dependence','feature_shift','missingness','prevalence','calibration','subgroup']; y=(d.optimism>=.05).astype(int)
rho,p=spearmanr(d.audit_score,d.optimism)
# cluster bootstrap domains, resample configs within each sampled domain
rng=np.random.default_rng(20260921);doms=d.domain.unique();bs=[]
for _ in range(5000):
 parts=[]
 for dm in rng.choice(doms,len(doms),replace=True):
  z=d[d.domain==dm];parts.append(z.iloc[rng.integers(0,len(z),len(z))])
 b=pd.concat(parts,ignore_index=True);r=spearmanr(b.audit_score,b.optimism).statistic
 if np.isfinite(r):bs.append(r)
ci=np.quantile(bs,[.025,.975])
# leave-domain-out threshold chosen on two train domains by balanced accuracy; apply held domain
def choose_thr(z):
 cand=np.unique(np.r_[0,z.audit_score.values,1]);best=(-1,.5)
 for t in cand:
  pr=(z.audit_score>=t);tp=((pr)&(z.material==1)).sum();fn=((~pr)&(z.material==1)).sum();tn=((~pr)&(z.material==0)).sum();fp=((pr)&(z.material==0)).sum();sen=tp/(tp+fn) if tp+fn else 0;sp=tn/(tn+fp) if tn+fp else 0
  if (sen+sp)/2>best[0]:best=((sen+sp)/2,float(t))
 return best[1]
d['material']=y; preds=[]
for dm in doms:
 tr=d[d.domain!=dm];te=d[d.domain==dm];t=choose_thr(tr);preds.extend(zip(te.index,(te.audit_score>=t).astype(int),[t]*len(te)))
pr=pd.Series({i:v for i,v,t in preds}).sort_index();tp=((pr==1)&(y==1)).sum();fn=((pr==0)&(y==1)).sum();tn=((pr==0)&(y==0)).sum();fp=((pr==1)&(y==0)).sum();sens=tp/(tp+fn);spec=tn/(tn+fp)
full_auc=roc_auc_score(y,d.audit_score); abl={}
for dim in dims:
 sc=d[[x for x in dims if x!=dim]].mean(axis=1);abl[dim]=roc_auc_score(y,sc)
# gates. Domain material from primary max delta
mat_domains=int((d.groupby('domain').optimism.max()>=.05).sum())
gates={'G1_rho':bool(rho>=.6 and ci[0]>0),'G2_two_domains':bool(mat_domains>=2),'G3_lodo_detection':bool(sens>=.8 and spec>=.6),'G4_ablation_superiority':bool(all(full_auc-a>=.02 for a in abl.values())),'G5_controls':False,'G6_reproducibility':False}
# controls/repro pending means fail, honestly
res={'rho':rho,'rho_p':p,'rho_cluster_bootstrap_ci95':ci.tolist(),'material_domains':mat_domains,'lodo_sensitivity':sens,'lodo_specificity':spec,'full_auc':full_auc,'ablated_auc':abl,'gates':gates,'success':all(gates.values()),'status':'NEGATIVE' if not all(gates.values()) else 'SUCCESS','paper_allowed':all(gates.values()),'note':'Controls and clean rerun are pending; an all-required protocol cannot pass. Existing G4 also fails if any ablation is within 0.02.'}
json.dump(res,open(O/'locked_gate_results.json','w'),indent=2);print(json.dumps(res,indent=2))
