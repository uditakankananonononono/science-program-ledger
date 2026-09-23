import pandas as pd, numpy as np, json
from Bio.Align import substitution_matrices as SM
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score
import scipy.sparse as sp
AA='ACDEFGHIKLMNPQRSTVWY'
d=pd.read_csv('../data/missense.tsv',sep='\t',dtype={'variation_id':str})
B=SM.load('BLOSUM62'); P=SM.load('PAM250')
d['B62']=[-B[r][a] for r,a in zip(d.ref,d.alt)]; d['PAM']=[-P[r][a] for r,a in zip(d.ref,d.alt)]
pairs=[r+a for r in AA for a in AA if r!=a]; pi={p:i for i,p in enumerate(pairs)}
rows=np.arange(len(d)); X=sp.hstack([sp.csr_matrix((np.ones(len(d)),(rows,[pi[r+a] for r,a in zip(d.ref,d.alt)])),shape=(len(d),380)),
    sp.csr_matrix((np.ones(len(d)),(rows,[AA.index(r) for r in d.ref])),shape=(len(d),20)),
    sp.csr_matrix((np.ones(len(d)),(rows,[AA.index(a) for a in d.alt])),shape=(len(d),20))]).tocsr()
y=d.label.values; genes=d.gene.values; ug=np.unique(genes); rng=np.random.default_rng(25); perm=dict(zip(ug,rng.permutation(len(ug)))); g=np.array([perm[x] for x in genes])
M=np.zeros(len(d))
for tr,te in GroupKFold(5).split(X,y,g):
    M[te]=LogisticRegression(C=1.0,max_iter=2000).fit(X[tr],y[tr]).decision_function(X[te])
d['M']=M; d[['variation_id','gene','ref','pos','alt','label','review','B62','PAM','M']].to_csv('../results/scores.tsv.gz',sep='\t',index=False)
two=d.review.isin(['criteria provided, multiple submitters, no conflicts','reviewed by expert panel','practice guideline']).values
res={'n':len(d),'n_path':int(y.sum()),'n_genes':len(ug),'n_2star':int(two.sum()),'n_2star_path':int(y[two].sum())}
for k in ('B62','PAM','M'): res['auroc_'+k]=roc_auc_score(y,d[k]); res['auroc2_'+k]=roc_auc_score(y[two],d[k].values[two])
gi=pd.Series(np.arange(len(d))).groupby(genes).apply(lambda s:s.values).to_dict(); b1=[];b2=[];b3=[]
Mv,Bv,Pv=d.M.values,d.B62.values,d.PAM.values
for _ in range(2000):
    idx=np.concatenate([gi[x] for x in rng.choice(ug,len(ug))]); yy=y[idx]
    if yy.min()==yy.max(): continue
    am=roc_auc_score(yy,Mv[idx]); b1.append(am-roc_auc_score(yy,Bv[idx])); b2.append(am-roc_auc_score(yy,Pv[idx]))
    t=idx[two[idx]]
    if len(set(y[t]))==2: b3.append(roc_auc_score(y[t],Mv[t])-roc_auc_score(y[t],Bv[t]))
res['d_M_B62']=res['auroc_M']-res['auroc_B62']; res['ci1']=list(np.percentile(b1,[2.5,97.5]))
res['d_M_PAM']=res['auroc_M']-res['auroc_PAM']; res['ci2']=list(np.percentile(b2,[2.5,97.5]))
res['d2_M_B62']=res['auroc2_M']-res['auroc2_B62']; res['ci3']=list(np.percentile(b3,[2.5,97.5]))
res['gates']={'G1':bool(res['d_M_B62']>=0.03 and res['ci1'][0]>0),'G2':bool(res['d_M_PAM']>=0.03 and res['ci2'][0]>0),'G3':bool(res['d2_M_B62']>0 and res['ci3'][0]>0)}
json.dump(res,open('../results/metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
