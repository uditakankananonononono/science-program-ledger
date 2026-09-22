#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];D=R/'data/processed';O=R/'results';F=R/'figures';O.mkdir(exist_ok=True);F.mkdir(exist_ok=True)
rng=np.random.default_rng(20260921); df=pd.read_csv(D/'r2_analysis_cohort.csv',dtype={'accession':str,'first_family':str}); df=df[df.first_family.notna()&df.first_family.ne('NO_PFAM')].copy()
outcomes=['has_function','has_exp_go','has_pdb','has_alphafold']

def family_table(z,minarm=5,band=None):
 if band:z=z[z.length.between(*band)]
 g=z.groupby(['first_family','short'])[outcomes].agg(['mean','size'])
 rows=[]
 for fam in z.first_family.unique():
  q=z[z.first_family==fam]
  a=q[q.short==1];b=q[q.short==0]
  if len(a)>=minarm and len(b)>=minarm:
   row={'family':fam,'short_n':len(a),'control_n':len(b),'harmonic_weight':2/(1/len(a)+1/len(b))}
   for o in outcomes:
    if a[o].notna().any() and b[o].notna().any():row[f'{o}_rd']=a[o].mean()-b[o].mean()
   rows.append(row)
 return pd.DataFrame(rows)
def boot(x,col,B=2000):
 a=x[col].dropna().to_numpy();
 if len(a)==0:return (np.nan,np.nan)
 # family bootstrap
 vals=np.array([rng.choice(a,len(a),True).mean() for _ in range(B)])
 return tuple(np.quantile(vals,[.025,.975]))
summary=[]; famall=[]; loo=[]; sensitivity=[]
raw=pd.read_csv(R/'provenance/R2_unadjusted_effects.csv')
for dom,z in df.groupby('domain'):
 ft=family_table(z,5);ft['domain']=dom;famall.append(ft)
 narrow=family_table(z,3,(80,120));narrow.to_csv(O/f'{dom}_narrow_families.csv',index=False)
 for o in outcomes:
  col=f'{o}_rd'
  if col not in ft:continue
  est=ft[col].mean();lo,hi=boot(ft,col);west=np.average(ft[col].dropna(),weights=ft.loc[ft[col].notna(),'harmonic_weight'])
  nest=narrow[col].mean() if col in narrow else np.nan
  summary.append({'domain':dom,'outcome':o,'families':ft[col].notna().sum(),'short_n':ft.short_n.sum(),'control_n':ft.control_n.sum(),'family_equal_rd':est,'ci_low':lo,'ci_high':hi,'protein_targeted_rd':west,'narrow_families':narrow[col].notna().sum() if col in narrow else 0,'narrow_family_equal_rd':nest})
 # leave top families
 for fam in ft.sort_values('harmonic_weight',ascending=False).head(10).family:
  q=ft[ft.family!=fam]
  for o in ['has_function','has_exp_go','has_pdb']:
   col=f'{o}_rd'
   if col in q:loo.append({'domain':dom,'left_out_family':fam,'outcome':o,'estimate':q[col].mean()})
 for m in [3,5,10]:
  q=family_table(z,m)
  for o in ['has_function','has_exp_go','has_pdb']:
   col=f'{o}_rd'
   if col in q:sensitivity.append({'domain':dom,'min_per_arm':m,'outcome':o,'families':q[col].notna().sum(),'estimate':q[col].mean()})
pd.concat(famall,ignore_index=True).to_csv(O/'family_effects.csv',index=False);res=pd.DataFrame(summary);res.to_csv(O/'domain_summary.csv',index=False);pd.DataFrame(loo).to_csv(O/'leave_top_family_out.csv',index=False);pd.DataFrame(sensitivity).to_csv(O/'minimum_family_size_sensitivity.csv',index=False)
# gate
gate={}; stable=0;struct=0
for dom in df.domain.unique():
 q=res[res.domain==dom].set_index('outcome'); estimable=bool(len(q) and q.iloc[0].families>=10 and q.iloc[0].short_n>=200 and q.iloc[0].control_n>=200);g={'estimable':estimable}
 l=pd.DataFrame(loo); l=l[l.domain==dom]
 for o in ['has_function','has_exp_go']:
  if o in q.index:
   x=q.loc[o]; agreement=(l[l.outcome==o].estimate<0).mean(); ok=bool(estimable and x.family_equal_rd<=-.05 and x.ci_high<0 and x.narrow_family_equal_rd<0 and agreement>=.7);g[o+'_stable_gap']=ok
 rawp=raw[(raw.domain==dom)&(raw.outcome=='has_pdb')]
 if 'has_pdb' in q.index and len(rawp):
  rr=float(rawp.iloc[0].risk_difference);x=q.loc['has_pdb'];att=(abs(rr)-abs(x.family_equal_rd))/abs(rr) if rr else 0; ok=bool(estimable and (np.sign(rr)!=np.sign(x.family_equal_rd) or att>=.75) and x.narrow_family_equal_rd*x.family_equal_rd>=0 and (x.ci_low<=0<=x.ci_high or np.sign(x.family_equal_rd)!=np.sign(rr)));g.update(raw_pdb_rd=rr,family_pdb_rd=float(x.family_equal_rd),pdb_attenuation=float(att),structural_selection=ok)
 gate[dom]=g
 stable+=int(any(v for k,v in g.items() if k.endswith('stable_gap')));struct+=int(g.get('structural_selection',False))
out={'domains':gate,'stable_gap_domains':stable,'structural_selection_domains':struct,'passed':bool(stable>=2 or struct>=2),'status':'SUCCESS' if stable>=2 or struct>=2 else 'MIXED_OR_NONTRANSPORTING'};(O/'gate_decision.json').write_text(json.dumps(out,indent=2))
# fig
p=res[res.outcome.isin(['has_function','has_pdb'])];fig,axs=plt.subplots(1,2,figsize=(12,5))
for ax,o in zip(axs,['has_function','has_pdb']):
 q=p[p.outcome==o];x=np.arange(len(q));ax.errorbar(x,q.family_equal_rd,yerr=[q.family_equal_rd-q.ci_low,q.ci_high-q.family_equal_rd],fmt='o',capsize=4);ax.axhline(0,color='black');ax.set_xticks(x,q.domain,rotation=25);ax.set_title(o.replace('has_','').title());ax.set_ylabel('Family-equal short minus control RD')
fig.suptitle('Shared-Pfam-family target estimands');fig.tight_layout();fig.savefig(F/'family_estimands.png',dpi=220);plt.close(fig)
print(json.dumps(out,indent=2))
