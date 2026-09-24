import json,numpy as np
from sklearn.metrics import roc_auc_score
from Bio import Align
from Bio.Align import substitution_matrices
S=json.load(open('data/sets.json'));P=json.load(open('data/proteins.txt'));R=json.load(open('results/dock.json'))
al=Align.PairwiseAligner();al.substitution_matrix=substitution_matrices.load('BLOSUM62');al.open_gap_score=-10;al.extend_gap_score=-0.5;al.mode='global'
def ident(a,b):
    x=al.align(a,b)[0];m=sum(1 for i,j in zip(*x.aligned) for _ in [0]) ;s=str(x).split('\n')
    A,B=x[0],x[1];same=sum(1 for p,q in zip(A,B) if p==q and p!='-');return same/min(len(a),len(b))
prim={'imatinib':'ABL1','erlotinib':'EGFR'};res={}
for d in prim:
    rows=[v|{'k':k} for k,v in R.items() if k.startswith(d+'|') and v['score'] is not None]
    y=np.array([r['label']=='b' for r in rows]);vs=-np.array([r['score'] for r in rows])
    b1=np.array([ident(P[prim[d]],P[r['gene']]) for r in rows])
    res[d]=dict(n_b=int(y.sum()),n_n=int((~y).sum()),vina_auroc=roc_auc_score(y,vs),B1_auroc=roc_auc_score(y,b1),
      rows=[dict(gene=r['gene'],label=r['label'],score=r['score'],pdb=r['pdb'],lig=r['lig'],ident=float(i)) for r,i in zip(rows,b1)])
m=lambda k:float(np.mean([res[d][k] for d in prim]))
res['mean_vina']=m('vina_auroc');res['mean_B1']=m('B1_auroc');res['G1']=res['mean_vina']>=0.70;res['G2']=res['mean_vina']-res['mean_B1']>=0.05
print(json.dumps({k:v for k,v in res.items() if k not in prim},indent=1));[print(d,{k:v for k,v in res[d].items() if k!='rows'}) for d in prim]
json.dump(res,open('results/analysis.json','w'),indent=1)
