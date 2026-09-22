#!/usr/bin/env python3
from pathlib import Path
import gzip, hashlib, json, math, re, warnings
import numpy as np, pandas as pd
from scipy.special import expit
from scipy.stats import fisher_exact
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore', category=RuntimeWarning)
R=Path(__file__).resolve().parents[1]; RAW=R/'data/raw'; PROC=R/'data/processed'; RES=R/'results'; FIG=R/'figures'
for p in [PROC,RES,FIG]:p.mkdir(parents=True,exist_ok=True)
SEED=20260921; rng=np.random.default_rng(SEED)
MAP={'Entry':'accession','Protein names':'protein_name','Length':'length','Organism (ID)':'organism_id','Date of creation':'created','Date of last modification':'modified','Annotation':'annotation_score','Protein existence':'protein_existence','Function [CC]':'function','Gene Ontology IDs':'go','PDB':'pdb','AlphaFoldDB':'alphafold','InterPro':'interpro','Pfam':'pfam','PubMed ID':'pubmed','Signal peptide':'signal','Transmembrane':'tm','Sequence':'sequence','Taxonomic lineage':'lineage'}
EXP={'EXP','IDA','IPI','IMP','IGI','IEP','HTP','HDA','HMP','HGI','HEP'}
PE={'Evidence at protein level':1,'Evidence at transcript level':2,'Inferred from homology':3,'Predicted':4,'Uncertain':5}
DIS=set('PGQSEKRDAN'); HYD=set('AVILMFWY'); CHG=set('DEKR')
def countsemi(x): return 0 if not str(x).strip() else len([y for y in str(x).split(';') if y.strip()])
def tryptic(seq):
 ps=re.split(r'(?<=[KR])(?!P)',seq); return sum(7<=len(x)<=35 for x in ps)
def entropy(seq):
 if not seq:return np.nan
 _,c=np.unique(list(seq),return_counts=True); p=c/c.sum(); return -(p*np.log2(p)).sum()
def prepare(name):
 d=pd.read_csv(RAW/f'uniprot_{name}.tsv',sep='\t',dtype=str,keep_default_na=False).rename(columns=MAP)
 d['domain']=name; d.length=pd.to_numeric(d.length,errors='coerce'); d.organism_id=pd.to_numeric(d.organism_id,errors='coerce').astype('Int64'); d.annotation_score=pd.to_numeric(d.annotation_score,errors='coerce'); d['short']=(d.length<=100).astype(int)
 for src,out in [('function','has_function'),('go','has_go'),('pdb','has_pdb'),('alphafold','has_alphafold'),('interpro','has_interpro'),('pfam','has_pfam'),('signal','has_signal'),('tm','has_tm')]: d[out]=d[src].str.strip().ne('').astype(int)
 d['go_count']=d.go.map(countsemi); d['pdb_count']=d.pdb.map(countsemi); d['pub_count']=d.pubmed.map(countsemi); d['interpro_count']=d.interpro.map(countsemi); d['pfam_count']=d.pfam.map(countsemi)
 d['first_family']=d.pfam.str.split(';').str[0].str.strip(); d.loc[d.first_family.eq(''),'first_family']='NO_PFAM'
 d['created_year']=pd.to_numeric(d.created.str[:4],errors='coerce'); d['created_era']=pd.cut(d.created_year,[0,2010,2015,2020,9999],labels=['pre2011','2011_15','2016_20','2021plus']).astype(str)
 d['pe_tier']=d.protein_existence.map(PE).fillna(5).astype(int); d['pub_bin']=pd.cut(d.pub_count,[-1,0,1,4,10**9],labels=['0','1','2_4','5plus']).astype(str)
 d['phylum']=d.lineage.str.extract(r'([^,]+) \(phylum\)',expand=False).fillna('unresolved')
 for col,chars in [('hydrophobic_fraction',HYD),('charged_fraction',CHG),('disorder_fraction',DIS)]: d[col]=d.sequence.map(lambda s: sum(x in chars for x in s)/len(s) if s else np.nan)
 d['low_complexity_fraction']=d.sequence.map(lambda s:max([s.count(x) for x in set(s)])/len(s) if s else np.nan); d['sequence_entropy']=d.sequence.map(entropy); d['tryptic_peptides']=d.sequence.map(tryptic)
 d['uncertain_name']=d.protein_name.str.contains(r'\b(hypothetical|uncharacterized|putative)\b',case=False,regex=True).astype(int); d['ribosomal']=d.protein_name.str.contains('ribosomal',case=False).astype(int)
 return d

def goa_exp(name, accessions):
 f=RAW/f'goa_{name}.gaf.gz'
 if not f.exists(): return set()
 hit=set()
 with gzip.open(f,'rt',errors='replace') as h:
  for line in h:
   if line.startswith('!'):continue
   z=line.rstrip('\n').split('\t')
   if len(z)>6 and z[1] in accessions and z[6] in EXP:hit.add(z[1])
 return hit

cache=PROC/'analysis_cohort.csv'
if cache.exists():
 df=pd.read_csv(cache,dtype={'accession':str,'first_family':str,'phylum':str})
else:
 df=pd.concat([prepare(n) for n in ['bacteria','human','mouse','yeast']],ignore_index=True)
 for n in ['human','mouse','yeast']:
  hit=goa_exp(n,set(df.loc[df.domain.eq(n),'accession'])); df.loc[df.domain.eq(n),'has_exp_go']=df.loc[df.domain.eq(n),'accession'].isin(hit).astype(float)
 df.loc[df.domain.eq('bacteria'),'has_exp_go']=np.nan
 bad=df.accession.eq('')|df.length.isna()|~df.length.between(20,200)|df.duplicated(['domain','accession'],False)
 ex=df.loc[bad,['domain','accession','length']].copy(); ex['reason']='missing/range/duplicate'; ex.to_csv(PROC/'exclusions.csv',index=False); df=df[~bad].copy()
cols=['domain','accession','protein_name','length','organism_id','short','created_year','created_era','modified','annotation_score','protein_existence','pe_tier','has_function','has_go','has_exp_go','has_pdb','has_alphafold','has_interpro','has_pfam','has_signal','has_tm','go_count','pdb_count','pub_count','pub_bin','interpro_count','pfam_count','first_family','phylum','hydrophobic_fraction','charged_fraction','disorder_fraction','low_complexity_fraction','sequence_entropy','tryptic_peptides','uncertain_name','ribosomal']
df[cols].to_csv(PROC/'analysis_cohort.csv',index=False)

def smd(x,t,w=None):
 if w is None:w=np.ones(len(t))
 a=t==1;b=~a; ma=np.average(x[a],weights=w[a]); mb=np.average(x[b],weights=w[b]); va=np.average((x[a]-ma)**2,weights=w[a]); vb=np.average((x[b]-mb)**2,weights=w[b]); return (ma-mb)/np.sqrt((va+vb)/2+1e-12)
def design(z,stage):
 X=[]; names=[]
 def addnum(c,log=False):
  x=z[c].astype(float).to_numpy(); x=np.log1p(x) if log else x; x=np.nan_to_num(x,nan=np.nanmedian(x)); x=(x-x.mean())/(x.std()+1e-9); X.append(x);names.append(c)
 def addcat(c,top=20):
  v=z[c].astype(str); cats=list(v.value_counts().head(top).index)
  for a in cats[1:]:X.append(v.eq(a).astype(float).to_numpy());names.append(f'{c}={a}')
 if z.domain.iloc[0]=='bacteria': addcat('phylum',15)
 if stage>=1:
  for c in ['length','hydrophobic_fraction','charged_fraction','disorder_fraction','low_complexity_fraction','sequence_entropy','tryptic_peptides']:addnum(c)
  for c in ['has_tm','has_signal']:addnum(c)
 if stage>=2:
  addnum('created_year');addnum('pub_count',True);addcat('pe_tier',6);addcat('created_era',5);addcat('pub_bin',5)
 if stage>=3:
  addnum('has_interpro');addnum('has_pfam');addcat('first_family',25)
 return np.column_stack(X) if X else np.empty((len(z),0)),names
def propensity(X,t,lam=1.0):
 X=np.column_stack([np.ones(len(t)),X]); b=np.zeros(X.shape[1]); pen=np.eye(X.shape[1])*lam;pen[0,0]=0
 for _ in range(15):
  p=expit(np.clip(X@b,-25,25)); W=np.clip(p*(1-p),1e-6,None); H=X.T@(W[:,None]*X)+pen; g=X.T@(t-p)-pen@b; step=np.linalg.solve(H,g);b+=step
  if np.max(abs(step))<1e-7:break
 return np.clip(expit(X@b),.01,.99)
def wrd(y,t,w):
 return np.average(y[t==1],weights=w[t==1])-np.average(y[t==0],weights=w[t==0])
def boot_ci(z,y,t,w,B=1000):
 vals=[]
 if z.domain.iloc[0]=='bacteria':
  ids=z.organism_id.fillna(-1).astype(str).to_numpy()
  tmp=pd.DataFrame({'id':ids,'wy1':w*y*t,'w1':w*t,'wy0':w*y*(~t),'w0':w*(~t)})
  A=tmp.groupby('id',sort=False)[['wy1','w1','wy0','w0']].sum().to_numpy(); uniq=np.arange(len(A))
  for start in range(0,B,100):
   m=rng.poisson(1,size=(min(100,B-start),len(uniq)))
   q=m@A
   vals.extend(np.where((q[:,1]>0)&(q[:,3]>0),q[:,0]/q[:,1]-q[:,2]/q[:,3],np.nan).tolist())
 else:
  # Poisson(1) multiplier bootstrap is the scalable nonparametric bootstrap limit.
  for start in range(0,B,100):
   m=rng.poisson(1,size=(min(100,B-start),len(z)))
   wa=m*w
   a=wa[:,t]; b=wa[:,~t]
   vals.extend((a@y[t]/a.sum(1)-b@y[~t]/b.sum(1)).tolist())
 return np.nanquantile(vals,[.025,.975])

outcomes=['has_function','has_go','has_exp_go','has_pdb','has_alphafold']
rows=[]; balance=[]; weight_store=[]
for dom,z0 in df.groupby('domain',sort=False):
 z=z0.reset_index(drop=True); t=z.short.to_numpy().astype(bool)
 for st in range(4):
  X,names=design(z,st); p=propensity(X,t.astype(int)); w=np.where(t,1-p,p); ess1=w[t].sum()**2/(w[t]@w[t]);ess0=w[~t].sum()**2/(w[~t]@w[~t])
  covars=['length','hydrophobic_fraction','charged_fraction','disorder_fraction','low_complexity_fraction','sequence_entropy','tryptic_peptides','has_tm','has_signal','created_year','pub_count','has_interpro','has_pfam']
  bpre={c:abs(smd(np.nan_to_num(z[c].to_numpy(float),nan=np.nanmedian(z[c].to_numpy(float))),t)) for c in covars}; bpost={c:abs(smd(np.nan_to_num(z[c].to_numpy(float),nan=np.nanmedian(z[c].to_numpy(float))),t,w)) for c in covars}
  balance.append({'domain':dom,'stage':f'M{st}','ess_short':ess1,'ess_control':ess0,'max_weight':w.max(),'max_abs_smd_pre':max(bpre.values()),'max_abs_smd_post':max(bpost.values()),**{f'post_{c}':v for c,v in bpost.items()}})
  weight_store.append(pd.DataFrame({'domain':dom,'accession':z.accession,'stage':f'M{st}','propensity':p,'overlap_weight':w}))
  for o in outcomes:
   ok=z[o].notna().to_numpy(); y=z[o].fillna(0).to_numpy(float); tt=t[ok]; ww=w[ok]; yy=y[ok]
   if not ok.any() or len(np.unique(tt))<2: continue
   rd=wrd(yy,tt,ww); lo,hi=boot_ci(z[ok].reset_index(drop=True),yy,tt,ww)
   a=z.loc[t&o.__class__(str),'accession'] if False else None
   rows.append({'domain':dom,'stage':f'M{st}','outcome':o,'short_n':int(tt.sum()),'control_n':int((~tt).sum()),'short_prop':np.average(yy[tt],weights=ww[tt]),'control_prop':np.average(yy[~tt],weights=ww[~tt]),'risk_difference':rd,'ci_low':lo,'ci_high':hi,'ess_short':ess1,'ess_control':ess0})
weights_all=pd.concat(weight_store); weights_all.to_csv(PROC/'overlap_weights.csv',index=False); pd.DataFrame(balance).to_csv(RES/'balance_diagnostics.csv',index=False); effects=pd.DataFrame(rows);effects.to_csv(RES/'sequential_effects.csv',index=False)
# Unadjusted exact descriptive and CEM matched strata.
un=[]; cem=[]
for dom,z in df.groupby('domain'):
 t=z.short.astype(bool)
 for o in outcomes:
  q=z[z[o].notna()];a=q[q.short.eq(1)][o];b=q[q.short.eq(0)][o]
  if len(a) and len(b): un.append({'domain':dom,'outcome':o,'short_n':len(a),'control_n':len(b),'short_prop':a.mean(),'control_prop':b.mean(),'risk_difference':a.mean()-b.mean(),'odds_ratio':fisher_exact([[a.sum(),len(a)-a.sum()],[b.sum(),len(b)-b.sum()]])[0]})
 keys=['created_era','pe_tier','has_tm','has_signal','has_pfam','pub_bin']
 if dom=='bacteria':keys=['organism_id']+keys
 counts=z.groupby(keys+['short']).size().unstack(fill_value=0); valid=counts[(counts.get(0,0)>0)&(counts.get(1,0)>0)].index
 zz=z.set_index(keys).loc[valid].reset_index() if len(valid) else z.iloc[0:0]
 for o in outcomes:
  q=zz[zz[o].notna()]
  if len(q) and q.short.nunique()==2:
   # equal stratum weight; within-stratum differences
   ds=[]
   for _,g in q.groupby(keys):
    if g.short.nunique()==2:ds.append(g[g.short.eq(1)][o].mean()-g[g.short.eq(0)][o].mean())
   cem.append({'domain':dom,'outcome':o,'matched_entries':len(q),'matched_strata':len(ds),'mean_stratum_difference':np.mean(ds) if ds else np.nan})
pd.DataFrame(un).to_csv(RES/'unadjusted_effects.csv',index=False);pd.DataFrame(cem).to_csv(RES/'coarsened_exact_matching.csv',index=False)
# Sensitivity at M3: cutoffs, exclusions, leave phylum/family.
sens=[]
def m3effect(z,cut,label):
 z=z.copy();z['short']=(z.length<=cut).astype(int); z=z[((z.length>=20)&(z.length<=cut))|((z.length>cut)&(z.length<=200))]
 if z.short.nunique()<2 or min(z.short.value_counts())<50:return
 t=z.short.to_numpy(bool)
 # Reuse frozen full-cohort M3 weights for exclusion/leave-out checks; refit only changed cutoffs.
 if cut==100:
  wm=weights_all[(weights_all.domain==z.domain.iloc[0])&(weights_all.stage=='M3')].set_index('accession').overlap_weight
  w=z.accession.map(wm).to_numpy(float)
 else:
  X,_=design(z,3);p=propensity(X,t.astype(int));w=np.where(t,1-p,p)
 for o in ['has_function','has_pdb']:
  sens.append({'domain':z.domain.iloc[0],'analysis':label,'cutoff':cut,'outcome':o,'n':len(z),'risk_difference':wrd(z[o].to_numpy(float),t,w)})
for dom,z in df.groupby('domain'):
 for cut in [80,100,120]:m3effect(z,cut,f'cutoff_{cut}')
 for label,q in [('exclude_ribosomal',z.ribosomal.eq(0)),('exclude_uncertain',z.uncertain_name.eq(0)),('exclude_tm',z.has_tm.eq(0)),('exclude_signal',z.has_signal.eq(0)),('created_pre2021',z.created_year.le(2020)),('family_known',z.has_pfam.eq(1))]:m3effect(z[q],100,label)
 # top family leave-outs
 for fam in z.first_family.value_counts().head(5).index:m3effect(z[z.first_family.ne(fam)],100,f'leave_family_{fam}')
 if dom=='bacteria':
  for ph in z.phylum.value_counts().head(6).index:m3effect(z[z.phylum.ne(ph)],100,f'leave_phylum_{ph}')
pd.DataFrame(sens).to_csv(RES/'sensitivity.csv',index=False)
# Gate explanations.
u=pd.DataFrame(un);e=effects;b=pd.DataFrame(balance);s=pd.DataFrame(sens)
gate_domains={}
for dom in df.domain.unique():
 raw=u[(u.domain==dom)].set_index('outcome'); m3=e[(e.domain==dom)&(e.stage=='M3')].set_index('outcome'); bd=b[(b.domain==dom)&(b.stage=='M3')].iloc[0]
 gd={'overlap_ok':bool(bd.ess_short>=200 and bd.ess_control>=200 and bd.max_abs_smd_post<=.10)}
 for o in ['has_function','has_exp_go']:
  if o in m3.index:
   sensx=s[(s.domain==dom)&(s.outcome=='has_function')]; gd[f'{o}_gap']=bool(m3.loc[o].risk_difference<=-.05 and m3.loc[o].ci_high<0 and (sensx.risk_difference<0).mean()>=.75)
 if 'has_pdb' in raw.index:
  r=raw.loc['has_pdb'].risk_difference; q=m3.loc['has_pdb'].risk_difference; att=(abs(r)-abs(q))/abs(r) if r else 0; gd['pdb_raw_rd']=float(r);gd['pdb_m3_rd']=float(q);gd['pdb_attenuation']=float(att);gd['pdb_resolved']=bool(r>0 and (q<=0 or att>=.75))
 gate_domains[dom]=gd
gap_repl=sum(any(v for k,v in g.items() if k.endswith('_gap')) and g['overlap_ok'] for g in gate_domains.values()); rev_repl=sum(g.get('pdb_resolved',False) and g['overlap_ok'] for g in gate_domains.values())
gate={'domains':gate_domains,'gap_replication_count':gap_repl,'resolved_reversal_count':rev_repl,'passed':bool(gap_repl>=2 or rev_repl>=2),'status':'SUCCESS' if gap_repl>=2 or rev_repl>=2 else 'UNRESOLVED_MIXED'}
(RES/'gate_decision.json').write_text(json.dumps(gate,indent=2))
# Figures
plot=e[e.stage.isin(['M0','M3'])&e.outcome.isin(['has_function','has_pdb'])]
fig,axs=plt.subplots(1,2,figsize=(12,5),sharey=False)
for ax,o in zip(axs,['has_function','has_pdb']):
 q=plot[plot.outcome==o]; doms=list(df.domain.unique()); x=np.arange(len(doms));
 for j,st in enumerate(['M0','M3']):
  qq=q[q.stage==st].set_index('domain').reindex(doms);ax.errorbar(x+(j-.5)*.08,qq.risk_difference,yerr=[qq.risk_difference-qq.ci_low,qq.ci_high-qq.risk_difference],fmt='o',capsize=3,label=st)
 ax.axhline(0,color='black',lw=1);ax.set_xticks(x,doms,rotation=25);ax.set_title(o.replace('has_','').replace('_',' ').title());ax.set_ylabel('Short minus control risk difference');ax.legend()
fig.suptitle('Small-protein evidence contrasts before and after prespecified balancing');fig.tight_layout();fig.savefig(FIG/'sequential_contrasts.png',dpi=220);plt.close(fig)
print(json.dumps(gate,indent=2))
