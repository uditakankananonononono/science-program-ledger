import json,time,numpy as np,sys
sys.path.insert(0,'code'); from sketch import *
from scipy.stats import binomtest
from Bio import Align
from Bio.Align import substitution_matrices
d=json.load(open('data/set.json')); S=[x['seq'] for x in d]; F=np.array([x['fam'] for x in d]); n=len(S)
# SW matrix
W=np.zeros((n,n),np.float32)
for i in range(n):
    r=np.load(f'results/sw_rows/{i}.npy'); W[i,i:]=r; W[i:,i]=r
self_=np.diag(W).copy(); Wn=W/np.minimum.outer(self_,self_)
# twilight: best same-family % identity
al=Align.PairwiseAligner(mode='local',substitution_matrix=substitution_matrices.load('BLOSUM62'),open_gap_score=-11,extend_gap_score=-1)
def pid(a,b):
    aln=al.align(a,b)[0]; c=aln.counts(); cols=c.identities+c.mismatches+c.gaps
    return 100*c.identities/cols if cols else 0
bestid=np.zeros(n)
for i in range(n):
    same=[j for j in range(n) if j!=i and F[j]==F[i]]
    j=max(same,key=lambda j:W[i,j]); bestid[i]=pid(S[i],S[j])
tw=bestid<40
def loo(M):
    M=M.copy(); np.fill_diagonal(M,-np.inf); return F[M.argmax(1)]==F
methods={}
methods['SW']=(loo(Wn),None)
SPEC={'K3':(PLAIN,['111'],None),'MH3':(PLAIN,['111'],256),'RA-C4':(MURPHY10,['1111'],256),'RA-SP':(MURPHY10,['11011','1101011'],256)}
timing={}
for name,(alpha,pats,s) in SPEC.items():
    t=time.time(); fs=[featset(q,alpha,pats) for q in S]; sk=fs if s is None else [bottom(f,s) for f in fs]
    M=np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            M[i,j]=M[j,i]=exact_jaccard(sk[i],sk[j]) if s is None else mash_jaccard(sk[i],sk[j],s)
    timing[name]=time.time()-t; methods[name]=(loo(M),None)
    np.save(f'results/sim_{name}.npy',M.astype(np.float32))
res={'n':n,'n_fam':len(set(F)),'n_twilight':int(tw.sum()),'bestid_median':float(np.median(bestid)),'acc':{},'acc_twilight':{},'acc_nontwilight':{},'time_s':timing}
for k,(c,_) in methods.items():
    res['acc'][k]=float(c.mean()); res['acc_twilight'][k]=float(c[tw].mean()); res['acc_nontwilight'][k]=float(c[~tw].mean())
def mcn(a,b):
    b01=int((~a&b).sum()); b10=int((a&~b).sum()); return b01,b10,binomtest(b01,b01+b10).pvalue if b01+b10 else 1.0
a,b=methods['MH3'][0],methods['RA-SP'][0]
res['mcnemar_RASP_vs_MH3']=mcn(a,b); res['mcnemar_RASP_vs_MH3_twilight']=mcn(a[tw],b[tw])
res['mcnemar_RASP_vs_RAC4']=mcn(methods['RA-C4'][0],b)
np.save('results/bestid.npy',bestid); json.dump(res,open('results/results.json','w'),indent=1); print(json.dumps(res,indent=1))
