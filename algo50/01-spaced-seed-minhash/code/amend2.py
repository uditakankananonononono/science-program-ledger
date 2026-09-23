import json,numpy as np,sys
sys.path.insert(0,'code'); from sketch import *
from scipy.stats import binomtest
d=json.load(open('data/set.json')); S=[x['seq'] for x in d]; F=np.array([x['fam'] for x in d]); n=len(S)
W=np.zeros((n,n),np.float32)
for i in range(n):
    r=np.load(f'results/sw_rows/{i}.npy'); W[i,i:]=r; W[i:,i]=r
s=np.diag(W).copy(); Wn=W/np.minimum.outer(s,s); np.fill_diagonal(Wn,-np.inf)
tw=np.load('results/bestid.npy')<40
SPEC={'RA-SP-X':(MURPHY10,['11011','1101011'],None),'MH3-1024':(PLAIN,['111'],1024),'RA-SP-1024':(MURPHY10,['11011','1101011'],1024)}
for name,(al,p,sz) in SPEC.items():
    fs=[featset(q,al,p) for q in S]; sk=fs if sz is None else [f[:sz] for f in fs]; M=np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n): M[i,j]=M[j,i]=exact_jaccard(sk[i],sk[j]) if sz is None else mash_jaccard(sk[i],sk[j],sz)
    np.save(f'results/sim_{name}.npy',M.astype(np.float32))
K=[1,2,3,5,10,20,30,50,100,200]; out={'k':K,'methods':{}}
for m in ['K3','MH3','RA-SP','RA-SP-X','MH3-1024','RA-SP-1024']:
    M=np.load(f'results/sim_{m}.npy').astype(np.float64); np.fill_diagonal(M,-np.inf)
    M=M+np.random.default_rng(0).uniform(0,1e-9,M.shape); order=np.argsort(-M,1); r={'acc':[],'acc_tw':[],'recall':[]}
    for k in K:
        cand=order[:,:k]; best=cand[np.arange(n),np.take_along_axis(Wn,cand,1).argmax(1)]; c=F[best]==F
        r['acc'].append(float(c.mean())); r['acc_tw'].append(float(c[tw].mean())); r['recall'].append(float((F[cand]==F[:,None]).any(1).mean()))
        if k==1: r['c1']=c
    out['methods'][m]=r
a,b=out['methods']['RA-SP']['c1'],out['methods']['RA-SP-X']['c1']
b01=int((~a&b).sum());b10=int((a&~b).sum()); out['B3_mcnemar']=[b01,b10,binomtest(b01,b01+b10).pvalue]
for r in out['methods'].values(): r.pop('c1')
json.dump(out,open('results/amend2.json','w'),indent=1)
for m,r in out['methods'].items(): print(m,' '.join(f'k{k}:{a:.4f}/{t:.3f}' for k,a,t in zip(K,r['acc'],r['acc_tw'])))
print('B3',out['B3_mcnemar'])
