#!/usr/bin/env python3
from pathlib import Path
import pandas as pd,numpy as np,re,json,collections
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];RAW=R/'data/raw';PROC=R/'data/processed';RES=R/'results';FIG=R/'figures';
for p in [PROC,RES,FIG]:p.mkdir(exist_ok=True)
ids=re.compile(r'(MedGen:C\d+|OMIM:\d+|Orphanet:\d+|MONDO:MONDO:\d+)')
parts=[]
use=['VariationID','GeneSymbol','ClinicalSignificance','PhenotypeIDS','ReviewStatus','NumberSubmitters','Assembly','Type']
for ch in pd.read_csv(RAW/'variant_summary.txt.gz',sep='\t',usecols=use,dtype=str,chunksize=250000,low_memory=False):
 ch=ch[(ch.Assembly=='GRCh38')&ch.GeneSymbol.notna()&~ch.GeneSymbol.isin(['-','na'])].copy()
 ch['condition']=ch.PhenotypeIDS.fillna('').str.findall(ids);ch=ch.explode('condition');ch=ch[ch.condition.notna()]
 cs=ch.ClinicalSignificance.fillna('').str.lower();ch['p']=(cs.str.contains('pathogenic')&~cs.str.contains('benign')).astype(int);ch['b']=(cs.str.contains('benign')&~cs.str.contains('pathogenic')).astype(int);ch['vus']=cs.str.contains('uncertain').astype(int);ch['conflict']=cs.str.contains('conflict').astype(int);ch['high_review']=ch.ReviewStatus.fillna('').str.lower().str.contains('expert panel|practice guideline').astype(int)
 parts.append(ch.groupby(['GeneSymbol','condition'],as_index=False).agg(variants=('VariationID','nunique'),p=('p','sum'),b=('b','sum'),vus=('vus','sum'),conflict=('conflict','sum'),high_review=('high_review','max')))
e=pd.concat(parts).groupby(['GeneSymbol','condition'],as_index=False).agg({'variants':'sum','p':'sum','b':'sum','vus':'sum','conflict':'sum','high_review':'max'}).rename(columns={'GeneSymbol':'gene'})
e['source']=e.condition.str.split(':').str[0];e['positive']=e.p>=2;e['contradictory']=((e.p>=1)&(e.b>=1))|(e.conflict>=1);e['benign_burden']=e.b/(e.p+e.b).replace(0,np.nan)
e.to_csv(PROC/'gene_condition_edges.csv',index=False)
# degrees and projection neighbor sets via genes -> conditions, only positive
pos=e[e.positive].copy();gd=pos.groupby('gene').size();cd=pos.groupby('condition').size();pos['gene_degree']=pos.gene.map(gd);pos['condition_degree']=pos.condition.map(cd)
# high burden threshold among positive finite top quartile
q=pos.benign_burden.fillna(0).quantile(.75);pos['high_burden']=pos.benign_burden.fillna(0)>=q
summary={'edges':len(e),'positive_edges':len(pos),'contradictory_edges':int(e.contradictory.sum()),'positive_contradictory':int(pos.contradictory.sum()),'genes':e.gene.nunique(),'conditions':e.condition.nunique(),'high_burden_threshold':q}
# instability endpoint: conflict variant presence. exact strata gene-degree, condition-degree, source, high review via logistic unavailable; stratified risk differences coarse bins.
pos['gdb']=pd.qcut(pos.gene_degree,5,duplicates='drop');pos['cdb']=pd.qcut(pos.condition_degree,5,duplicates='drop')
strata=[]
for key,z in pos.groupby(['source','gdb','cdb','high_review'],observed=True):
 if z.high_burden.nunique()==2 and min(z.high_burden.value_counts())>=5:
  a=z[z.high_burden].conflict.gt(0).mean();b=z[~z.high_burden].conflict.gt(0).mean();strata.append({'source':key[0],'n':len(z),'risk_difference':a-b})
s=pd.DataFrame(strata);s.to_csv(RES/'stratified_instability.csv',index=False)
# source replications
src=[]
for k,z in pos.groupby('source'):
 a=z[z.high_burden];b=z[~z.high_burden];src.append({'source':k,'n':len(z),'high_burden_n':len(a),'conflict_high':a.conflict.gt(0).mean(),'conflict_low':b.conflict.gt(0).mean(),'risk_difference':a.conflict.gt(0).mean()-b.conflict.gt(0).mean()})
pd.DataFrame(src).to_csv(RES/'source_replication.csv',index=False)
# disease projection top neighbors: shared positive genes unweighted vs reliability score contribution
from itertools import combinations
raw=collections.Counter();rel=collections.Counter();high=collections.Counter()
for g,z in pos.groupby('gene'):
 rec=z[['condition','p','b','conflict','high_review']].to_dict('records')
 for a,b in combinations(rec,2):
  pair=tuple(sorted((a['condition'],b['condition'])));raw[pair]+=1;ra=a['p']/(a['p']+a['b']+a['conflict']+1);rb=b['p']/(b['p']+b['b']+b['conflict']+1);rel[pair]+=ra*rb
  if a['high_review'] and b['high_review']:high[pair]+=1
n=max(1,int(.1*len(raw)));topraw=set(x for x,_ in raw.most_common(n));toprel=set(x for x,_ in rel.most_common(n));change=1-len(topraw&toprel)/len(topraw);hset=set(high);pres=len((topraw&hset)&toprel)/max(1,len(topraw&hset));summary.update(projection_pairs=len(raw),top_decile_change=change,high_review_neighbor_preservation=pres)
# gate
rep=pd.DataFrame(src);repdirs=int((rep[rep.n>=1000].risk_difference>0).sum());strat_effect=np.average(s.risk_difference,weights=s.n) if len(s) else np.nan;summary.update(stratified_rd=strat_effect,replication_positive_strata=repdirs)
neg_control=float(pos.groupby(pos.gene.str[0]).conflict.apply(lambda x:x.gt(0).mean()).std())
gate={'conditions':{'min_edges':len(e)>=10000,'min_contradictory':int(e.contradictory.sum())>=1000,'adjusted_instability_positive':bool(strat_effect>0),'replicates_two_sources':repdirs>=2,'projection_change':change>=.05,'high_review_preserved':pres>=.8,'negative_control_smaller':neg_control<abs(strat_effect)},'summary':summary,'negative_control_accession_initial_sd':neg_control};gate['passed']=all(gate['conditions'].values());(RES/'gate_decision.json').write_text(json.dumps(gate,indent=2,default=lambda x: x.item() if hasattr(x,"item") else str(x)))
# figs
fig,ax=plt.subplots(figsize=(8,5));r=pd.DataFrame(src).sort_values('n',ascending=False);ax.bar(r.source,r.risk_difference);ax.axhline(0,color='black');ax.set_ylabel('Conflict prevalence RD: high minus low benign burden');ax.tick_params(axis='x',rotation=30);fig.tight_layout();fig.savefig(FIG/'source_instability.png',dpi=220);plt.close(fig)
print(json.dumps(gate,indent=2,default=lambda x: x.item() if hasattr(x,"item") else str(x)))
