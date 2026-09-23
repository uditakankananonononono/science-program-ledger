import pandas as pd, numpy as np, json
from sklearn.metrics import roc_auc_score as A
e=pd.read_csv('results/scores.tsv',sep='\t')
# BLOSUM62 and Grantham
import itertools
B62txt="""A 4 -1 -2 -2 0 -1 -1 0 -2 -1 -1 -1 -1 -2 -1 1 0 -3 -2 0
R -1 5 0 -2 -3 1 0 -2 0 -3 -2 2 -1 -3 -2 -1 -1 -3 -2 -3
N -2 0 6 1 -3 0 0 0 1 -3 -3 0 -2 -3 -2 1 0 -4 -2 -3
D -2 -2 1 6 -3 0 2 -1 -1 -3 -4 -1 -3 -3 -1 0 -1 -4 -3 -3
C 0 -3 -3 -3 9 -3 -4 -3 -3 -1 -1 -3 -1 -2 -3 -1 -1 -2 -2 -1
Q -1 1 0 0 -3 5 2 -2 0 -3 -2 1 0 -3 -1 0 -1 -2 -1 -2
E -1 0 0 2 -4 2 5 -2 0 -3 -3 1 -2 -3 -1 0 -1 -3 -2 -2
G 0 -2 0 -1 -3 -2 -2 6 -2 -4 -4 -2 -3 -3 -2 0 -2 -2 -3 -3
H -2 0 1 -1 -3 0 0 -2 8 -3 -3 -1 -2 -1 -2 -1 -2 -2 2 -3
I -1 -3 -3 -3 -1 -3 -3 -4 -3 4 2 -3 1 0 -3 -2 -1 -3 -1 3
L -1 -2 -3 -4 -1 -2 -3 -4 -3 2 4 -2 2 0 -3 -2 -1 -2 -1 1
K -1 2 0 -1 -3 1 1 -2 -1 -3 -2 5 -1 -3 -1 0 -1 -3 -2 -2
M -1 -1 -2 -3 -1 0 -2 -3 -2 1 2 -1 5 0 -2 -1 -1 -1 -1 1
F -2 -3 -3 -3 -2 -3 -3 -3 -1 0 0 -3 0 6 -4 -2 -2 1 3 -1
P -1 -2 -2 -1 -3 -1 -1 -2 -2 -3 -3 -1 -2 -4 7 -1 -1 -4 -3 -2
S 1 -1 1 0 -1 0 0 0 -1 -2 -2 0 -1 -2 -1 4 1 -3 -2 -2
T 0 -1 0 -1 -1 -1 -1 -2 -2 -1 -1 -1 -1 -2 -1 1 5 -2 -2 0
W -3 -3 -4 -4 -2 -2 -3 -2 -2 -3 -2 -3 -1 1 -4 -3 -2 11 2 -3
Y -2 -2 -2 -3 -2 -1 -2 -3 2 -1 -1 -2 -1 3 -3 -2 -2 2 7 -1
V 0 -3 -3 -3 -1 -2 -2 -3 -3 3 1 -2 1 -1 -2 -2 0 -3 -1 4"""
aa=[l.split()[0] for l in B62txt.splitlines()]
B={(a,b):int(v) for l in B62txt.splitlines() for a,(b,v) in [(l.split()[0],x) for x in zip(aa,l.split()[1:])]}
e['s_blosum']=[B[(w,m)] for w,m in zip(e.wt,e.mut)]
y=e.label.values; score=lambda c:-e[c].values  # lower score = more damaging -> invert
out={}
out['n']=int(len(e)); out['n_genes']=int(e.gene.nunique())
out['auc_esm']=A(y,score('s_esm')); out['auc_blosum']=A(y,score('s_blosum'))
rng=np.random.default_rng(1); genes=e.gene.unique(); gi={g:np.where(e.gene.values==g)[0] for g in genes}
be=[];bd=[]
for _ in range(1000):
    idx=np.concatenate([gi[g] for g in rng.choice(genes,len(genes))])
    yy=y[idx]
    if yy.min()==yy.max(): continue
    a1=A(yy,-e.s_esm.values[idx]); a2=A(yy,-e.s_blosum.values[idx]); be.append(a1); bd.append(a1-a2)
out['auc_esm_ci']=list(np.percentile(be,[2.5,97.5])); out['diff_ci']=list(np.percentile(bd,[2.5,97.5]))
pg=[]
for g,s in e.groupby('gene'):
    if s.label.sum()>=5 and (s.label==0).sum()>=5: pg.append(A(s.label,-s.s_esm))
out['n_genes_G3']=len(pg); out['median_within_gene_auc']=float(np.median(pg)) if pg else None
e['lev']=pd.to_datetime(e.last_eval,errors='coerce')
new=e.lev>='2024-01-01'; old=e.lev<'2024-01-01'
out['n_new']=int(new.sum()); out['n_old']=int(old.sum())
out['auc_new']=A(y[new],-e.s_esm[new]); out['auc_old']=A(y[old],-e.s_esm[old])
out['G1']=out['auc_esm']>=0.75 and out['auc_esm_ci'][0]>=0.70
out['G2']=(out['auc_esm']-out['auc_blosum'])>=0.05 and out['diff_ci'][0]>0
out['G3']=out['median_within_gene_auc'] is not None and out['median_within_gene_auc']>=0.70
out['G4']=abs(out['auc_new']-out['auc_old'])<=0.05
# failure characterization
strat={}
e['lenbin']=pd.cut(e.seq_len,[0,300,600,1022]); e['entbin']=pd.qcut(e.site_entropy,4,labels=['q1_low','q2','q3','q4_high'])
for c in ['lenbin','entbin']:
    strat[c]={str(k):{'n':int(len(s)),'pos':int(s.label.sum()),'auc':(A(s.label,-s.s_esm) if s.label.nunique()==2 else None)} for k,s in e.groupby(c,observed=True)}
out['strata']=strat
e.to_csv('results/scores_full.tsv',sep='\t',index=False)
json.dump(out,open('results/metrics.json','w'),indent=1,default=float); print(json.dumps(out,indent=1,default=float))
