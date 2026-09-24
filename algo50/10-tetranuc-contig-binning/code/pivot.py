import json
import numpy as np
from Bio import SeqIO
from itertools import product
comp=str.maketrans('ACGT','TGCA')
def genome_of(acc):
    return ''.join(str(r.seq) for r in SeqIO.parse(f'data/{acc}.gb','gb')).upper()
G={'ecoli':'NC_000913.3','bsub':'NC_000964.3','mtb':'NC_000962.3','shigella':'NC_004741'}
genomes={k:genome_of(v) for k,v in G.items()}
def canon_kmers(k):
    out=[]
    for km in product('ACGT',repeat=k):
        s=''.join(km); rc=s.translate(comp)[::-1]
        if s<=rc: out.append(s)
    return out
def zvec(seq,k,kms):
    idx={m:i for i,m in enumerate(kms)}
    v=np.zeros(len(kms))
    for i in range(len(seq)-k+1):
        s=seq[i:i+k]
        if set(s)-set('ACGT'): continue
        rc=s.translate(comp)[::-1]
        v[idx[min(s,rc)]]+=1
    f={b:seq.count(b)/len(seq) for b in 'ACGT'}
    pe=np.array([np.prod([f[b] for b in m])+np.prod([f[b] for b in m.translate(comp)[::-1]]) for m in kms])
    exp=pe*v.sum()
    return (v-exp)/np.sqrt(exp+1e-9)
kms={k:canon_kmers(k) for k in (2,3,4)}
contigs={}
for name,g in genomes.items():
    cs=[g[i:i+5000] for i in range(0,len(g)-5000+1,5000)]
    contigs[name]=(cs[0::2],cs[1::2])
res={}
for meth in ('GC','K2','K3','K4'):
    cents={}
    for name,(A,B) in contigs.items():
        if meth=='GC':
            cents[name]=np.mean([(s.count('G')+s.count('C'))/len(s) for s in A])
        else:
            k=int(meth[1]); cents[name]=np.mean([zvec(s,k,kms[k]) for s in A],axis=0)
    c=t=0
    for name,(A,B) in contigs.items():
        for s in B:
            if meth=='GC':
                x=(s.count('G')+s.count('C'))/len(s)
                pred=min(cents,key=lambda cc:abs(cents[cc]-x))
            else:
                k=int(meth[1]); z=zvec(s,k,kms[k])
                pred=max(cents,key=lambda cc:np.corrcoef(z,cents[cc])[0,1])
            c+=pred==name;t+=1
    res[meth]=c/t
print(json.dumps(res,indent=1))
json.dump(res,open('results/pivot_metrics.json','w'),indent=1)
print('P1 GC<=0.75:',res['GC'])
print('P2 K4>=GC+0.15:',res['K4'],res['GC'])
print('P3 K4>=0.90:',res['K4'])
