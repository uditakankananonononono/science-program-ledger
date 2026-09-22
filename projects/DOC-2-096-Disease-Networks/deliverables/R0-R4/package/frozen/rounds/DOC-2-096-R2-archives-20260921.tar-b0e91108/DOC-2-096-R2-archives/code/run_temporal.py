from pathlib import Path
import pandas as pd,numpy as np,re,collections,json,hashlib
from scipy.special import expit
from scipy.stats import rankdata
R=Path(__file__).resolve().parents[1];pat=re.compile(r'(MedGen:C\d+|OMIM:\d+|Orphanet:\d+|MONDO:MONDO:\d+)')
# 2020-only crosswalk
parent={}
def find(x):
 parent.setdefault(x,x)
 if parent[x]!=x:parent[x]=find(parent[x])
 return parent[x]
def union(a,b):
 a=find(a);b=find(b);parent[b]=a
for ch in pd.read_csv(R/'data/raw/2020_variant.txt.gz',sep='\t',usecols=['PhenotypeIDS'],dtype=str,chunksize=200000):
 for s in ch.PhenotypeIDS.dropna():
  for slot in s.split('||'):
   ids=pat.findall(slot)
   for x in ids[1:]:union(ids[0],x)
comp=collections.defaultdict(set)
for x in parent:comp[find(x)].add(x)
map20={};amb=[]
for root,ss in comp.items():
 c=collections.Counter(x.split(':')[0] for x in ss);bad=any(v>1 for v in c.values());
 for x in ss:map20[x]='' if bad else sorted(ss)[0]
 if bad:amb.append(root)
pd.DataFrame([{'identifier':x,'canonical':v,'ambiguous':v==''} for x,v in map20.items()]).to_csv(R/'data/processed/crosswalk_2020.csv',index=False)

def edges(path,label):
 parts=[];use=['VariationID','GeneSymbol','ClinicalSignificance','PhenotypeIDS','ReviewStatus','NumberSubmitters','Assembly']
 for ch in pd.read_csv(path,sep='\t',usecols=use,dtype=str,chunksize=200000):
  ch=ch[(ch.Assembly=='GRCh38')&ch.GeneSymbol.notna()&~ch.GeneSymbol.isin(['-','na'])].copy();ch['condition']=ch.PhenotypeIDS.fillna('').str.findall(pat);ch=ch.explode('condition');ch=ch[ch.condition.notna()];ch['norm']=ch.condition.map(map20);ch['norm']=ch['norm'].where(ch['norm'].notna()&ch['norm'].ne(''),ch.condition)
  cs=ch.ClinicalSignificance.fillna('').str.lower();ch['p']=(cs.str.contains('pathogenic')&~cs.str.contains('benign')).astype(int);ch['b']=(cs.str.contains('benign')&~cs.str.contains('pathogenic')).astype(int);ch['conflict']=cs.str.contains('conflict').astype(int);ch['high_review']=ch.ReviewStatus.fillna('').str.lower().str.contains('expert panel|practice guideline').astype(int);ch['submitters']=pd.to_numeric(ch.NumberSubmitters,errors='coerce').fillna(0)
  parts.append(ch.groupby(['GeneSymbol','norm'],as_index=False).agg(p=('p','sum'),b=('b','sum'),conflict=('conflict','sum'),high_review=('high_review','max'),submitters=('submitters','sum'),variants=('VariationID','nunique')))
 e=pd.concat(parts).groupby(['GeneSymbol','norm'],as_index=False).sum();e['source']=e.norm.str.split(':').str[0];e['reliability']=e.p/(e.p+e.b+e.conflict+1);e['benign_burden']=e.b/(e.p+e.b).replace(0,np.nan);e.to_csv(R/f'data/processed/edges_{label}.csv',index=False);return e
E20=edges(R/'data/raw/2020_variant.txt.gz','2020');E23=edges(R/'data/raw/2023_variant.txt.gz','2023')
# current from R0 processed mapped using 2020 unchanged
cur=pd.read_csv('/home/sandbox/DOC-2-096-R0-negative-evidence/data/processed/gene_condition_edges.csv');cur['norm']=cur.condition.map(map20);cur['norm']=cur['norm'].where(cur['norm'].notna()&cur['norm'].ne(''),cur.condition);EC=cur.groupby(['gene','norm'],as_index=False).agg(p=('p','sum'),b=('b','sum'),conflict=('conflict','sum'),high_review=('high_review','max'),variants=('variants','sum')).rename(columns={'gene':'GeneSymbol'});EC['source']=EC.norm.str.split(':').str[0];EC['reliability']=EC.p/(EC.p+EC.b+EC.conflict+1);EC['benign_burden']=EC.b/(EC.p+EC.b).replace(0,np.nan);EC.to_csv(R/'data/processed/edges_current.csv',index=False)
# prospective evaluations: outcome emergence conflict or high review among baseline absent.
def evaluate(a,b,name):
 x=a.merge(b,on=['GeneSymbol','norm'],suffixes=('_base','_future'));x=x[(x.p_base+x.b_base+x.conflict_base)>=2].copy();x['event']=((x.conflict_base==0)&(x.conflict_future>0))|((x.high_review_base==0)&(x.high_review_future>0));
 # fixed scores: raw testing burden, positive-only ratio, R0 reliability risk=1-rel
 scores={'raw':np.log1p(x.variants_base),'positive_only':x.p_base/(x.p_base+1),'reliability':1-x.reliability_base}
 mets=[]
 y=x.event.astype(int).to_numpy();prev=y.mean()
 for k,s in scores.items():
  z=np.asarray(s,float);z=np.nan_to_num(z,nan=np.nanmedian(z));z=(z-z.mean())/(z.std()+1e-9); # one-param logistic fit calibration on baseline transition itself descriptive
  X=np.c_[np.ones(len(z)),z];beta=np.zeros(2)
  for _ in range(30):
   pr=expit(X@beta);w=np.clip(pr*(1-pr),1e-6,None);beta+=np.linalg.solve(X.T@(w[:,None]*X),X.T@(y-pr))
  pr=expit(X@beta);brier=np.mean((pr-y)**2);top=y[z>=np.quantile(z,.9)].mean()/prev if prev else np.nan
  # auc ranks
  auc=(rankdata(z)[y==1].sum()-y.sum()*(y.sum()+1)/2)/(y.sum()*(len(y)-y.sum())) if 0<y.sum()<len(y) else np.nan
  mets.append({'transition':name,'model':k,'edges':len(x),'events':int(y.sum()),'prevalence':prev,'brier':brier,'top_decile_enrichment':top,'auc':auc,'coef':beta[1]})
 return x,pd.DataFrame(mets)
x1,m1=evaluate(E20,E23,'2020_to_2023');x2,m2=evaluate(E23,EC,'2023_to_current');M=pd.concat([m1,m2]);M.to_csv(R/'results/temporal_metrics.csv',index=False)
# gate strict
wide=M.pivot(index='transition',columns='model',values='brier');improve=(wide.raw-wide.reliability)/wide.raw
gate={'crosswalk':{'identifiers':len(map20),'ambiguous_components':len(amb)},'transition_events':{r.transition:int(r.events) for _,r in M[M.model=='raw'].iterrows()},'brier_improvement':improve.to_dict(),'conditions':{'min_edges':len(x1)>=10000 and len(x2)>=10000,'min_events':x1.event.sum()>=1000 and x2.event.sum()>=1000,'brier_improves_5pct_both':bool((improve>=.05).all())},'passed':False};gate['passed']=all(gate['conditions'].values())
(R/'results/gate_decision.json').write_text(json.dumps(gate,indent=2,default=lambda x:x.item() if hasattr(x,"item") else str(x)));print(json.dumps(gate,indent=2,default=lambda x:x.item() if hasattr(x,"item") else str(x)));print(M.to_string(index=False))
