#!/usr/bin/env python3
from pathlib import Path
import pandas as pd,numpy as np,json
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];O=R/'results';F=R/'figures';O.mkdir(exist_ok=True);F.mkdir(exist_ok=True);rng=np.random.default_rng(20260921)
base=pd.read_csv(R/'data/processed/r2_analysis_cohort.csv',dtype={'accession':str});base=base[base.domain.isin(['human','mouse','yeast'])]
# parse all Pfam and proteomics
frames=[]
for dom in ['human','mouse','yeast']:
 raw=pd.read_csv(R/f'data/raw/uniprot_{dom}.tsv',sep='\t',dtype=str).fillna('')[['Entry','Pfam']].rename(columns={'Entry':'accession','Pfam':'pfam_all'})
 pro=pd.read_csv(R/f'data/raw/proteomics_{dom}.tsv',sep='\t',dtype=str).fillna('').rename(columns={'Entry':'accession','PeptideAtlas':'pa','ProteomicsDB':'pdbx','MassIVE':'massive','PRIDE':'pride'})
 pro['any_proteomics']=pro[['pa','pdbx','massive','pride']].apply(lambda x:any(bool(str(v).strip()) for v in x),axis=1).astype(int)
 z=base[base.domain==dom].merge(raw,on='accession').merge(pro[['accession','any_proteomics','pa','pdbx','massive','pride']],on='accession');frames.append(z)
df=pd.concat(frames,ignore_index=True);df.to_csv(R/'data/processed/r4_cohort.csv',index=False)
outcomes=['has_function','has_exp_go','has_pdb','any_proteomics','has_alphafold']
def assess(z,fcol,definition,minarm=5):
 fam=[]
 for f,g in z.groupby(fcol):
  a=g[g.short==1];b=g[g.short==0]
  if len(a)>=minarm and len(b)>=minarm:
   row={'domain':g.domain.iloc[0],'definition':definition,'family':f,'short_n':len(a),'control_n':len(b),'harmonic':2/(1/len(a)+1/len(b))}
   for o in outcomes:row[o+'_rd']=a[o].mean()-b[o].mean()
   fam.append(row)
 ft=pd.DataFrame(fam)
 if len(ft)==0:return ft,[]
 unique_s=z[z[fcol].isin(ft.family)&z.short.eq(1)].accession.nunique();unique_c=z[z[fcol].isin(ft.family)&z.short.eq(0)].accession.nunique();largest=max(ft.short_n.max()/ft.short_n.sum(),ft.control_n.max()/ft.control_n.sum());estimable=len(ft)>=10 and unique_s>=200 and unique_c>=200 and largest<=.5
 sm=[]
 for o in outcomes:
  v=ft[o+'_rd'].to_numpy(); boot=np.array([rng.choice(v,len(v),True).mean() for _ in range(2000)])
  # narrow direction evaluated using same family IDs at 80-120
  nz=z[z.length.between(80,120)&z[fcol].isin(ft.family)];nv=[]
  for f,g in nz.groupby(fcol):
   a=g[g.short==1];b=g[g.short==0]
   if len(a)>=3 and len(b)>=3:nv.append(a[o].mean()-b[o].mean())
  sm.append({'domain':z.domain.iloc[0],'definition':definition,'outcome':o,'families':len(ft),'unique_short':unique_s,'unique_control':unique_c,'largest_arm_share':largest,'estimable':estimable,'family_equal_rd':v.mean(),'ci_low':np.quantile(boot,.025),'ci_high':np.quantile(boot,.975),'narrow_families':len(nv),'narrow_rd':np.mean(nv) if nv else np.nan,'short_prevalence':z[z.short==1][o].mean(),'control_prevalence':z[z.short==0][o].mean()})
 return ft,sm
families=[];summary=[]
for dom,z in df.groupby('domain'):
 # all pfam explode
 ex=z.assign(family=z.pfam_all.str.split(';')).explode('family');ex['family']=ex.family.str.strip();ex=ex[ex.family.ne('')]
 ft,sm=assess(ex,'family','all_pfam');families.append(ft);summary+=sm
 # accession equalized sensitivity: deduplicate outcome contribution by membership count via one row per accession-family retained, descriptive handled in report.
 # mmseq grid
 for p in sorted((R/f'data/processed/mmseqs/{dom}').glob('*_cluster.tsv')):
  definition='mmseqs_'+p.name.replace('_cluster.tsv','');cl=pd.read_csv(p,sep='\t',header=None,names=['family','accession'],dtype=str);q=z.merge(cl,on='accession');ft2,sm2=assess(q,'family',definition);families.append(ft2);summary+=sm2
pd.concat([x for x in families if len(x)],ignore_index=True).to_csv(O/'family_cluster_effects.csv',index=False);res=pd.DataFrame(summary);res.to_csv(O/'definition_summary.csv',index=False)
# gate and leave out for all pfam
loo=[]
allft=pd.concat([x for x in families if len(x)],ignore_index=True)
for (dom,definition),x in allft.groupby(['domain','definition']):
 for fam in x.sort_values('harmonic',ascending=False).head(10).family:
  q=x[x.family!=fam]
  for o in outcomes:loo.append({'domain':dom,'definition':definition,'left_out':fam,'outcome':o,'estimate':q[o+'_rd'].mean()})
pd.DataFrame(loo).to_csv(O/'leave_top_out.csv',index=False)
gate={}; successful=[]
for dom in ['human','mouse','yeast']:
 g={'all_pfam_estimable':False,'supported_outcomes':[],'mmseq_estimable_definitions':0};q=res[(res.domain==dom)&(res.definition=='all_pfam')]
 if len(q):
  g['all_pfam_estimable']=bool(q.estimable.iloc[0]); l=pd.DataFrame(loo)
  for o in ['has_function','has_exp_go','has_pdb','any_proteomics']:
   x=q[q.outcome==o]
   if len(x):
    xx=x.iloc[0];agree=(l[(l.domain==dom)&(l.definition=='all_pfam')&(l.outcome==o)].estimate<0).mean();ok=bool(xx.estimable and xx.family_equal_rd<=-.05 and xx.ci_high<0 and xx.narrow_rd<0 and agree>=.7 and (o!='any_proteomics' or max(xx.short_prevalence,xx.control_prevalence)>=.1));
    if ok:g['supported_outcomes'].append(o)
 m=res[(res.domain==dom)&res.definition.str.startswith('mmseqs_')];g['mmseq_estimable_definitions']=int(m[m.estimable].definition.nunique())
 gate[dom]=g
# strict protocol requires same outcome in 2 domains and mmseq agreement. none if no mmseq support.
for o in ['has_function','has_exp_go','has_pdb','any_proteomics']:
 ds=[d for d,g in gate.items() if o in g['supported_outcomes'] and g['mmseq_estimable_definitions']>=2]
 if len(ds)>=2:successful.append({'outcome':o,'domains':ds})
out={'domains':gate,'successful_replications':successful,'passed':bool(successful),'status':'SUCCESS' if successful else 'NON_ESTIMABLE_OR_MIXED'};(O/'gate_decision.json').write_text(json.dumps(out,indent=2))
# plot all pfam only
p=res[(res.definition=='all_pfam')&res.outcome.isin(['has_function','has_exp_go','any_proteomics'])];fig,axs=plt.subplots(1,3,figsize=(14,4.5))
for ax,o in zip(axs,['has_function','has_exp_go','any_proteomics']):
 q=p[p.outcome==o];x=np.arange(len(q));ax.errorbar(x,q.family_equal_rd,yerr=[q.family_equal_rd-q.ci_low,q.ci_high-q.family_equal_rd],fmt='o',capsize=4);ax.axhline(0,color='black');ax.set_xticks(x,q.domain,rotation=25);ax.set_title(o.replace('has_','').replace('any_','').replace('_',' ').title());ax.set_ylabel('All-Pfam family-equal RD')
fig.suptitle('All-Pfam eukaryotic target estimands');fig.tight_layout();fig.savefig(F/'all_pfam_estimands.png',dpi=220);plt.close(fig)
print(json.dumps(out,indent=2))
