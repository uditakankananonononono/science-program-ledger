import pandas as pd, numpy as np, re, gzip, json
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
rng=np.random.default_rng(0)
T0='2019-01-01'
PH=re.compile(r'^(C\d+orf\d+|CXorf\d+|CYorf\d+|FAM\d+[A-Z]*\d*|KIAA\d+|TMEM\d+[A-Z]*|CCDC\d+[A-Z]*|LOC\d+|ORF\d+)$')
h=pd.read_csv('data/hgnc.txt',sep='\t',dtype=str,low_memory=False)
h=h[(h.status=='Approved')&(h.locus_group=='protein-coding gene')]
info=pd.read_csv('data/9606.protein.info.v11.0.txt.gz',sep='\t')
info.columns=['pid','name','size','annot']
rows=[]
for _,r in h.iterrows():
    sym=r.symbol; prev=[p.strip() for p in str(r.prev_symbol).split('|')] if pd.notna(r.prev_symbol) else []
    dsc=r.date_symbol_changed if pd.notna(r.date_symbol_changed) else ''
    appr=r.date_approved_reserved if pd.notna(r.date_approved_reserved) else ''
    if appr and appr>=T0: continue
    if PH.match(sym) and (not dsc or dsc<T0):
        rows.append((sym,sym,0))
    elif not PH.match(sym) and dsc>=T0:
        ph=[p for p in prev if PH.match(p)]
        if ph: rows.append((sym,ph[0],1))
c=pd.DataFrame(rows,columns=['symbol','t0_symbol','y'])
c=c.merge(info[['pid','name','size']],left_on='t0_symbol',right_on='name',how='left')
print('cohort',len(c),'pos',c.y.sum(),'mapped',c.pid.notna().sum())
ph_pids=set(info.pid[info.name.str.match(PH)])
pids=set(c.pid.dropna())
agg={p:[0,0,0.0,0,0] for p in pids}  # d700,d400,sum,nonph700,max
for ch in pd.read_csv('data/9606.protein.links.v11.0.txt.gz',sep=' ',chunksize=2_000_000):
    ch=ch[ch.protein1.isin(pids)]
    for p,q,s in ch.itertuples(index=False):
        a=agg[p]; a[2]+=s/1000; a[4]=max(a[4],s)
        if s>=400: a[1]+=1
        if s>=700:
            a[0]+=1
            if q not in ph_pids: a[3]+=1
f=pd.DataFrame.from_dict(agg,orient='index',columns=['d700','d400','ssum','nonph700','maxs'])
f['frac_char700']=np.where(f.d700>0,f.nonph700/f.d700.clip(lower=1),np.nan)
c=c.merge(f,left_on='pid',right_index=True,how='left')
c['present']=c.pid.notna().astype(int)
for k in ['d700','d400','ssum','maxs']: c[k]=c[k].fillna(0)
c['frac_char700']=c.frac_char700.fillna(0)
c['loglen']=np.log1p(c['size'].fillna(c['size'].median()))
for k in ['d700','d400','ssum']: c['l'+k]=np.log1p(c[k])
c.to_csv('results/cohort_features.csv',index=False)
y=c.y.values
cv=StratifiedKFold(5,shuffle=True,random_state=0)
def cvauc(cols,yy=y):
    m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000))
    p=cross_val_predict(m,c[cols].values,yy,cv=cv,method='predict_proba')[:,1]
    return roc_auc_score(yy,p),p
F=['ld700','ld400','lssum','frac_char700','maxs']
res={}
res['full'],pf=cvauc(F); res['B0_presence'],_=cvauc(['present']); res['B1_length'],_=cvauc(['loglen'])
res['full_plus_len'],_=cvauc(F+['loglen'])
bs=[]
for i in range(1000):
    idx=rng.integers(0,len(y),len(y))
    if y[idx].min()==y[idx].max(): continue
    bs.append(roc_auc_score(y[idx],pf[idx]))
res['full_ci']=[float(np.percentile(bs,2.5)),float(np.percentile(bs,97.5))]
perm=[cvauc(F,rng.permutation(y))[0] for _ in range(20)]
res['perm_mean']=float(np.mean(perm)); res['perm_range']=[float(min(perm)),float(max(perm))]
res['n']=int(len(y)); res['pos']=int(y.sum())
# univariate directions
for k in F+['loglen']: res['uni_'+k]=float(roc_auc_score(y,c[k]))
json.dump(res,open('results/primary.json','w'),indent=1); print(json.dumps(res,indent=1))
