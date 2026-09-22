import pandas as pd,numpy as np,re,json,json as js
from collections import Counter
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error,r2_score
from scipy.stats import spearmanr
AA='ACDEFGHIKLMNPQRSTVWY'; hyd=set('AVILMFWY'); charge=set('DEKR'); arom=set('FWY')
ref=pd.read_csv('/tmp/doc2009/ref.csv'); perf=pd.read_csv('/tmp/doc2009/dmslevel.csv')
d=ref.merge(perf[['DMS ID','ESM2 (650M)']],left_on='DMS_id',right_on='DMS ID',how='inner')
# InterPro map keyed by entry name
ip=pd.read_csv('/tmp/doc2009/uniprot_interpro.tsv',sep='\t').fillna('')
mp={r['Entry Name']:set(x for x in str(r['InterPro']).split(';') if x) for _,r in ip.iterrows()}
# union find across unique proteins via shared IPR
prots=list(d.UniProt_ID.unique()); par={x:x for x in prots}
def find(x):
 while par[x]!=x: par[x]=par[par[x]];x=par[x]
 return x
def union(a,b):
 a,b=find(a),find(b)
 if a!=b:par[b]=a
owners={}
for p in prots:
 for q in mp.get(p,set()):
  if q in owners: union(p,owners[q])
  else:owners[q]=p
# aggregate outcomes per protein, metadata mode/first; target sequence constant per UniProt
rows=[]
for p,g in d.groupby('UniProt_ID'):
 y=g['ESM2 (650M)'].mean(); seq=str(g.iloc[0].target_seq)
 if not np.isfinite(y) or any(a not in AA for a in seq):continue
 c=Counter(seq); n=len(seq); di=Counter(seq[i:i+2] for i in range(n-1))
 x=[c[a]/n for a in AA]+[di[a+b]/max(1,n-1) for a in AA for b in AA]
 probs=np.array([c[a]/n for a in AA]); ent=float(-(probs[probs>0]*np.log(probs[probs>0])).sum())
 x += [np.log(n),ent,sum(c[a] for a in arom)/n,sum(c[a] for a in charge)/n,sum(c[a] for a in hyd)/n,(c['G']+c['P'])/n,c['C']/n]
 rows.append(dict(p=p,y=y,x=x,group=find(p),annot=bool(mp.get(p)),taxon=g.iloc[0].taxon))
X=np.array([r['x'] for r in rows]); y=np.array([r['y'] for r in rows]); groups=np.array([r['group'] for r in rows]);
# deterministic folds: GroupKFold
outer=GroupKFold(n_splits=5); pred=np.full(len(y),np.nan); base=np.full(len(y),np.nan); alphas=[]
for tr,te in outer.split(X,y,groups):
 ug=np.unique(groups[tr]); ns=min(5,len(ug)); best=None
 for a in [.1,1,10,100]:
  vals=[]
  for it,iv in GroupKFold(n_splits=ns).split(X[tr],y[tr],groups[tr]):
   m=make_pipeline(StandardScaler(),Ridge(alpha=a));m.fit(X[tr][it],y[tr][it]); vals.extend(abs(y[tr][iv]-m.predict(X[tr][iv])))
  z=np.mean(vals)
  if best is None or z<best[0]:best=(z,a)
 a=best[1];alphas.append(a);m=make_pipeline(StandardScaler(),Ridge(alpha=a));m.fit(X[tr],y[tr]);pred[te]=m.predict(X[te]);base[te]=y[tr].mean()
rho=float(spearmanr(pred,y).statistic); r2=float(r2_score(y,pred)); mae=float(mean_absolute_error(y,pred)); bmae=float(mean_absolute_error(y,base)); gain=1-mae/bmae
rng=np.random.default_rng(2009); boots=[]
for _ in range(10000):
 z=rng.integers(0,len(y),len(y)); boots.append(spearmanr(pred[z],y[z]).statistic)
lo,hi=np.nanpercentile(boots,[2.5,97.5])
strata={}
for s in ['Human','Eukaryote','Prokaryote','Virus']:
 ix=np.array([r['taxon']==s for r in rows]); strata[s]={'n':int(ix.sum()),'rho':float(spearmanr(pred[ix],y[ix]).statistic) if ix.sum()>=3 else None}
res={'n_proteins':len(rows),'n_annotated':sum(r['annot'] for r in rows),'n_components':len(set(groups)),'n_assays':len(d),'rho':rho,'rho_ci':[float(lo),float(hi)],'r2':r2,'mae':mae,'baseline_mae':bmae,'mae_reduction':gain,'alphas':alphas,'strata':strata}
print(json.dumps(res,indent=2));open('/tmp/doc2009/results.json','w').write(json.dumps(res,indent=2))
pd.DataFrame({'UniProt_ID':[r['p'] for r in rows],'family_component':groups,'y_esm2_650m_spearman':y,'oof_pred':pred,'baseline_pred':base,'taxon':[r['taxon'] for r in rows],'interpro_annotated':[r['annot'] for r in rows]}).to_csv('/tmp/doc2009/oof_predictions.csv',index=False)
