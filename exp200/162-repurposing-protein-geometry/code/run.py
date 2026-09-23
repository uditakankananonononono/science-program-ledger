import json, numpy as np, pandas as pd, itertools
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
rng=np.random.default_rng(0)
U=pd.read_csv('data/uniprot_targets.tsv',sep='\t').dropna(subset=['Sequence'])
ipr={r.Entry:set(x for x in str(r.InterPro).split(';') if x.startswith('IPR')) for r in U.itertuples()}
km={r.Entry:{r.Sequence[i:i+3] for i in range(len(r.Sequence)-2)} for r in U.itertuples()}
gene=dict(zip(U.Entry,U['Gene Names (primary)']))
tg=json.load(open('data/targets.json')); t2a={}
for t in tg:
    if t.get('organism')=='Homo sapiens' and t.get('target_type')=='SINGLE PROTEIN':
        a=[c['accession'] for c in t['target_components'] if c.get('accession') in km]
        if a: t2a[t['target_chembl_id']]=a[0]
mech=json.load(open('data/mechanisms.json')); d2a={}
for m in mech:
    if m['target_chembl_id'] in t2a and m['parent_molecule_chembl_id']: d2a.setdefault(m['parent_molecule_chembl_id'],set()).add(t2a[m['target_chembl_id']])
pos=set()
for d,s in d2a.items():
    for a,b in itertools.combinations(sorted(s),2): pos.add((a,b))
allA=sorted(km); neg=set()
while len(neg)<20*len(pos):
    a,b=sorted(rng.choice(allA,2,replace=False))
    if (a,b) not in pos: neg.add((a,b))
J=lambda x,y: len(x&y)/len(x|y) if x|y else 0
rows=[(a,b,1,J(ipr[a],ipr[b]),J(km[a],km[b])) for a,b in pos]+[(a,b,0,J(ipr[a],ipr[b]),J(km[a],km[b])) for a,b in neg]
D=pd.DataFrame(rows,columns=['a','b','y','ipr','kmer']); D.to_csv('results/pairs.csv',index=False)
cut=D[D.y==0].kmer.quantile(.75); L=D[D.kmer<cut]
auc=roc_auc_score(L.y,L.ipr); bs=[]
for _ in range(1000):
    s=L.sample(len(L),replace=True,random_state=int(rng.integers(1e9)))
    if s.y.nunique()==2: bs.append(roc_auc_score(s.y,s.ipr))
cv=StratifiedKFold(5,shuffle=True,random_state=0); lr=LogisticRegression(max_iter=1000)
pk=cross_val_predict(lr,D[['kmer']],D.y,cv=cv,method='predict_proba')[:,1]
pb=cross_val_predict(lr,D[['kmer','ipr']],D.y,cv=cv,method='predict_proba')[:,1]
res={'n_drugs_multi':sum(len(s)>=2 for s in d2a.values()),'n_pos':int(D.y.sum()),'n_neg':int((D.y==0).sum()),'kmer_cut':float(cut),
 'low_stratum_pos':int(L.y.sum()),'low_stratum_auc_ipr':float(auc),'ci':[float(np.percentile(bs,2.5)),float(np.percentile(bs,97.5))],
 'auc_kmer_all':float(roc_auc_score(D.y,pk)),'auc_kmer_ipr_all':float(roc_auc_score(D.y,pb)),'auc_ipr_all':float(roc_auc_score(D.y,D.ipr)),
 'low_stratum_pos_ipr_zero':float((L[L.y==1].ipr==0).mean()),'high_stratum_pos':int((D[D.kmer>=cut].y).sum())}
res['G3_gain']=res['auc_kmer_ipr_all']-res['auc_kmer_all']
ex=L[(L.y==1)].sort_values('ipr',ascending=False).head(15)
res['examples_low_seq_pos']=[(gene.get(a),gene.get(b),round(i,2),round(k,3)) for a,b,i,k in ex[['a','b','ipr','kmer']].values]
print(json.dumps(res,indent=1)); json.dump(res,open('results/primary.json','w'),indent=1)
