#!/usr/bin/env python3
from pathlib import Path
import csv, json, hashlib, re, urllib.request, urllib.parse, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import fisher_exact

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/raw'; PROC=ROOT/'data/processed'; RES=ROOT/'results'; FIG=ROOT/'figures'; PROV=ROOT/'provenance'
for p in (PROC,RES,FIG,PROV): p.mkdir(parents=True,exist_ok=True)
SEED=20260921; rng=np.random.default_rng(SEED)
COL={'Entry':'accession','Entry Name':'entry_name','Protein names':'protein_name','Length':'length','Organism (ID)':'organism_id','Gene Ontology (GO)':'go','EC number':'ec','PDB':'pdb','Annotation':'annotation_score','Protein existence':'protein_existence','Signal peptide':'signal_peptide','Transmembrane':'transmembrane','Function [CC]':'function_comment','Taxonomic lineage':'lineage'}

def load(label):
 d=pd.read_csv(RAW/f'uniprot_{label}.tsv',sep='\t',dtype=str,keep_default_na=False).rename(columns=COL)
 d['cohort']=label; d['length']=pd.to_numeric(d.length,errors='coerce'); d['organism_id']=pd.to_numeric(d.organism_id,errors='coerce').astype('Int64'); d['annotation_score']=pd.to_numeric(d.annotation_score,errors='coerce')
 for src,out in [('go','has_go'),('function_comment','has_function_comment'),('pdb','has_pdb'),('ec','has_ec'),('signal_peptide','has_signal'),('transmembrane','has_transmembrane')]: d[out]=d[src].str.strip().ne('')
 d['is_ribosomal']=d.protein_name.str.contains('ribosomal',case=False,na=False)
 d['is_uncertain_name']=d.protein_name.str.contains(r'\b(hypothetical|uncharacterized|putative)\b',case=False,na=False,regex=True)
 d['phylum']=d.lineage.str.extract(r'([^,]+) \(phylum\)',expand=False).fillna('unresolved')
 d['evidence_score']=d[['has_go','has_function_comment','has_pdb','has_ec']].sum(axis=1)
 return d

df=pd.concat([load('short'),load('control')],ignore_index=True)
ex=[]
bad=df.accession.eq('')|df.length.isna()|df.organism_id.isna()|df.accession.duplicated(keep=False)
for _,r in df[bad].iterrows(): ex.append({'accession':r.accession,'cohort':r.cohort,'reason':'missing core field or duplicate accession'})
df=df[~bad].copy()
rangebad=((df.cohort=='short')&~df.length.between(30,100))|((df.cohort=='control')&~df.length.between(101,200))
for _,r in df[rangebad].iterrows(): ex.append({'accession':r.accession,'cohort':r.cohort,'reason':'length outside locked range'})
df=df[~rangebad].copy()
pd.DataFrame(ex,columns=['accession','cohort','reason']).to_csv(PROC/'exclusions.csv',index=False)
keep=['accession','entry_name','protein_name','length','organism_id','cohort','phylum','annotation_score','protein_existence','has_go','has_function_comment','has_pdb','has_ec','has_signal','has_transmembrane','is_ribosomal','is_uncertain_name','evidence_score']
df[keep].to_csv(PROC/'analysis_cohort.csv',index=False)

endpoints=['has_go','has_function_comment','has_pdb']
labels={'has_go':'GO term','has_function_comment':'Function comment','has_pdb':'PDB cross-reference'}

def effects(data, tag):
 rows=[]
 for e in endpoints+['has_ec','has_signal','has_transmembrane']:
  a=data[data.cohort=='short'][e]; b=data[data.cohort=='control'][e]
  ps=a.mean(); pc=b.mean(); rd=ps-pc; rr=(a.sum()+.5)/(len(a)+1)/((b.sum()+.5)/(len(b)+1))
  tab=[[int(a.sum()),int((~a).sum())],[int(b.sum()),int((~b).sum())]]
  p=fisher_exact(tab,alternative='less').pvalue
  rows.append({'analysis':tag,'endpoint':e,'short_n':len(a),'short_yes':int(a.sum()),'short_prop':ps,'control_n':len(b),'control_yes':int(b.sum()),'control_prop':pc,'risk_difference':rd,'risk_ratio':rr,'fisher_one_sided_p':p})
 return rows
rows=effects(df,'primary_entry_level')
rows+=effects(df[~df.is_ribosomal],'exclude_ribosomal')
rows+=effects(df[~df.is_uncertain_name],'exclude_uncertain_names')
rows+=effects(df[df.annotation_score.ge(4)],'annotation_score_ge4')
# Exact organism comparison using equal-weight organism proportions.
org=df.groupby(['organism_id','cohort'])[endpoints].mean().unstack('cohort').dropna()
paired=[]
for e in endpoints:
 diff=(org[(e,'short')]-org[(e,'control')]).dropna()
 paired.append({'endpoint':e,'organisms':len(diff),'mean_paired_difference':diff.mean(),'median_paired_difference':diff.median(),'negative_fraction':(diff<0).mean(),'zero_fraction':(diff==0).mean()})
pd.DataFrame(paired).to_csv(RES/'organism_paired_effects.csv',index=False)
# Cluster bootstrap over organism-level paired effects, equal weight per organism.
boots=[]
for e in endpoints:
 vals=(org[(e,'short')]-org[(e,'control')]).dropna().to_numpy()
 reps=np.array([rng.choice(vals,size=len(vals),replace=True).mean() for _ in range(2000)])
 boots.append({'endpoint':e,'organisms':len(vals),'estimate':vals.mean(),'ci_low':np.quantile(reps,.025),'ci_high':np.quantile(reps,.975),'bootstrap_p_ge_zero':(np.sum(reps>=0)+1)/(len(reps)+1)})
pd.DataFrame(boots).to_csv(RES/'organism_cluster_bootstrap.csv',index=False)
# Benjamini-Hochberg on primary Fisher tests.
eff=pd.DataFrame(rows)
prim=eff[(eff.analysis=='primary_entry_level')&eff.endpoint.isin(endpoints)].copy(); p=prim.fisher_one_sided_p.to_numpy(); order=np.argsort(p); q=np.empty(len(p)); running=1
for rank,idx in reversed(list(enumerate(order,start=1))): running=min(running,p[idx]*len(p)/rank); q[idx]=running
prim['bh_q']=q; eff=eff.merge(prim[['endpoint','bh_q']],on='endpoint',how='left'); eff.to_csv(RES/'endpoint_effects.csv',index=False)
# Length strata.
strata=[]
for name,sub in [('short_30_60',df[(df.cohort=='short')&df.length.between(30,60)]),('short_61_100',df[(df.cohort=='short')&df.length.between(61,100)]),('control_101_200',df[df.cohort=='control'])]:
 for e in endpoints: strata.append({'stratum':name,'endpoint':e,'n':len(sub),'yes':int(sub[e].sum()),'prop':sub[e].mean()})
pd.DataFrame(strata).to_csv(RES/'length_strata.csv',index=False)
# Phylum leave-one-out, entry-level descriptive.
phy=df.phylum.value_counts(); major=list(phy[phy>=500].index)
loo=[]
for ph in major:
 sub=df[df.phylum!=ph]
 for e in endpoints:
  s=sub[sub.cohort=='short'][e].mean(); c=sub[sub.cohort=='control'][e].mean(); loo.append({'left_out_phylum':ph,'endpoint':e,'risk_difference':s-c,'short_n':sum(sub.cohort=='short'),'control_n':sum(sub.cohort=='control')})
pd.DataFrame(loo).to_csv(RES/'leave_one_phylum_out.csv',index=False)
# Composition and family/name transparency.
df.groupby(['cohort','phylum']).size().rename('n').reset_index().sort_values(['cohort','n'],ascending=[True,False]).to_csv(RES/'phylum_composition.csv',index=False)
df.groupby(['cohort','protein_name']).size().rename('n').reset_index().sort_values(['cohort','n'],ascending=[True,False]).groupby('cohort').head(50).to_csv(RES/'top_protein_names.csv',index=False)
# Positive and negative-space controls.
controls=[]
for group,sub in [('ribosomal',df[df.is_ribosomal]),('non_ribosomal',df[~df.is_ribosomal]),('uncertain_name',df[df.is_uncertain_name]),('named',df[~df.is_uncertain_name])]:
 for e in endpoints: controls.append({'group':group,'endpoint':e,'n':len(sub),'prop':sub[e].mean()})
pd.DataFrame(controls).to_csv(RES/'controls.csv',index=False)
# Deterministic RCSB audit sample: 20 with and 20 without PDB per cohort, hash-ranked.
def rankkey(x): return hashlib.sha256(('SP004'+x).encode()).hexdigest()
sample=[]
for cohort in ['short','control']:
 for state in [True,False]:
  z=df[(df.cohort==cohort)&(df.has_pdb==state)].copy(); z['rank']=z.accession.map(rankkey)
  sample.append(z.sort_values('rank').head(20)[['accession','cohort','has_pdb']])
aud=pd.concat(sample,ignore_index=True); aud.to_csv(PROC/'rcsb_audit_sample.csv',index=False)
# RCSB search API for UniProt accession reference. Live and cached as raw JSON.
query_url='https://search.rcsb.org/rcsbsearch/v2/query'
rc=[]
for i,r in aud.iterrows():
 payload={"query":{"type":"terminal","service":"text","parameters":{"attribute":"rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession","operator":"exact_match","value":r.accession}},"return_type":"polymer_entity","request_options":{"return_all_hits":True}}
 raw=json.dumps(payload).encode(); req=urllib.request.Request(query_url,data=raw,headers={'Content-Type':'application/json','User-Agent':'SP-004-research-audit/1.0'})
 try:
  with urllib.request.urlopen(req,timeout=30) as fh: body=fh.read(); status=fh.status
  hit=json.loads(body).get('total_count',0)>0
 except Exception as ex:
  body=json.dumps({'error':str(ex)}).encode(); status=0; hit=None
 (RAW/f'rcsb_{r.accession}.json').write_bytes(body)
 rc.append({'accession':r.accession,'cohort':r.cohort,'uniprot_has_pdb':bool(r.has_pdb),'rcsb_has_entry':hit,'http_status':status,'agreement':(hit==bool(r.has_pdb)) if hit is not None else None})
 time.sleep(.03)
rc=pd.DataFrame(rc); rc.to_csv(RES/'rcsb_concordance.csv',index=False)
# Gate.
b=pd.DataFrame(boots).set_index('endpoint'); pp=pd.DataFrame(paired).set_index('endpoint'); base=eff[eff.analysis=='primary_entry_level'].set_index('endpoint'); rib=eff[eff.analysis=='exclude_ribosomal'].set_index('endpoint'); loo_df=pd.DataFrame(loo)
conditions={
'all_directions_negative':bool((base.loc[endpoints].risk_difference<0).all()),
'min_two_cluster_ci_below_zero':bool((b.loc[endpoints].ci_high<0).sum()>=2),
'min_two_negative_exact_organism_and_ribosomal_exclusion':bool(((pp.loc[endpoints].mean_paired_difference<0)&(rib.loc[endpoints].risk_difference<0)).sum()>=2),
'no_leave_phylum_out_reversal_gt_2pp':bool((loo_df.risk_difference<=.02).all()),
'rcsb_agreement_ge_95pct':bool(rc.agreement.dropna().mean()>=.95),
'integrity_checks_pass':bool(len(pd.read_csv(PROC/'exclusions.csv'))==0 and len(df.accession)==df.accession.nunique())}
gate={'conditions':conditions,'passed':all(conditions.values()),'rcsb_agreement':float(rc.agreement.dropna().mean()),'n_entries':len(df),'short_n':int(sum(df.cohort=='short')),'control_n':int(sum(df.cohort=='control'))}
(RES/'gate_decision.json').write_text(json.dumps(gate,indent=2))
# Figures.
plt.style.use('seaborn-v0_8-whitegrid')
x=np.arange(3); w=.36
s=[base.loc[e].short_prop for e in endpoints]; c=[base.loc[e].control_prop for e in endpoints]
fig,ax=plt.subplots(figsize=(9,5.4)); ax.bar(x-w/2,s,w,label='30-100 aa'); ax.bar(x+w/2,c,w,label='101-200 aa'); ax.set_xticks(x,[labels[e] for e in endpoints]); ax.set_ylim(0,1); ax.set_ylabel('Proportion of reviewed bacterial entries'); ax.legend(); ax.set_title('Evidence coverage by protein length cohort'); fig.tight_layout(); fig.savefig(FIG/'evidence_coverage.png',dpi=220); plt.close(fig)
fig,ax=plt.subplots(figsize=(9,5.4)); est=[b.loc[e].estimate for e in endpoints]; lo=[b.loc[e].ci_low for e in endpoints]; hi=[b.loc[e].ci_high for e in endpoints]; ax.errorbar(est,x,xerr=[np.array(est)-np.array(lo),np.array(hi)-np.array(est)],fmt='o',capsize=5); ax.axvline(0,color='black',lw=1); ax.set_yticks(x,[labels[e] for e in endpoints]); ax.set_xlabel('Organism-paired difference: short minus control'); ax.set_title('Equal-weight organism effects with cluster-bootstrap 95% CI'); fig.tight_layout(); fig.savefig(FIG/'organism_paired_effects.png',dpi=220); plt.close(fig)
# Integrity/provenance.
manifest=[]
for p in sorted(ROOT.rglob('*')):
 if p.is_file() and p.name!='file_manifest_sha256.csv': manifest.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
pd.DataFrame(manifest).to_csv(PROV/'file_manifest_sha256.csv',index=False)
print(json.dumps(gate,indent=2))
