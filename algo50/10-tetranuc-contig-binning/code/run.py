import json, hashlib, time
import numpy as np
from Bio import SeqIO
from itertools import product
def genome_of(acc):
    return ''.join(str(r.seq) for r in SeqIO.parse(f'data/{acc}.gb','gb')).upper()
G={'ecoli':'NC_000913.3','bsub':'NC_000964.3','mtb':'NC_000962.3'}
genomes={k:genome_of(v) for k,v in G.items()}
comp=str.maketrans('ACGT','TGCA')
def canon_kmers(k):
    out=[]
    for km in product('ACGT',repeat=k):
        s=''.join(km); rc=s.translate(comp)[::-1]
        if s<=rc: out.append(s)
    return out
def kvec(seq,k,kms):
    idx={m:i for i,m in enumerate(kms)}
    v=np.zeros(len(kms))
    rc_all=str.maketrans('ACGT','TGCA')
    for i in range(len(seq)-k+1):
        s=seq[i:i+k]
        if set(s)-set('ACGT'): continue
        rc=s.translate(rc_all)[::-1]
        v[idx[min(s,rc)]]+=1
    return v
def zvec(seq,k,kms):
    v=kvec(seq,k,kms)
    # expected from mononucleotide product
    f={b:seq.count(b)/len(seq) for b in 'ACGT'}
    e=np.array([np.prod([f[b] for b in m])* (seq.count(m)+seq.count(m.translate(comp)[::-1]) if m!=m.translate(comp)[::-1] else seq.count(m)) for m in kms])
    # simpler: expected fraction under mono model, scaled to total count
    pexp=np.array([np.prod([f[b] for b in m]) for m in kms])
    # account for canonical merging: p(m)+p(rc)
    prc=np.array([np.prod([f[b] for b in m.translate(comp)[::-1]]) for m in kms])
    pe=pexp+prc
    tot=v.sum()
    exp=pe*tot
    return (v-exp)/np.sqrt(exp+1e-9)
def acc_at(kms_by,k,len_contig):
    contigs={}
    for name,g in genomes.items():
        cs=[g[i:i+len_contig] for i in range(0,len(g)-len_contig+1,len_contig)]
        A=cs[0::2]; B=cs[1::2]
        contigs[name]=(A,B)
    accs={}
    for meth in ['GC']+list(kms_by.keys()):
        correct=tot=0
        cents={}
        for name,(A,B) in contigs.items():
            if meth=='GC':
                cents[name]=np.mean([ (s.count('G')+s.count('C'))/len(s) for s in A])
            else:
                k=kms_by[meth][0]; kms=kms_by[meth][1]
                cents[name]=np.mean([zvec(s,k,kms) for s in A],axis=0)
        for name,(A,B) in contigs.items():
            for s in B:
                if meth=='GC':
                    x=(s.count('G')+s.count('C'))/len(s)
                    pred=min(cents,key=lambda c:abs(cents[c]-x))
                else:
                    k=kms_by[meth][0]; kms=kms_by[meth][1]
                    z=zvec(s,k,kms)
                    pred=max(cents,key=lambda c: np.corrcoef(z,cents[c])[0,1])
                correct+=pred==name; tot+=1
        accs[meth]=correct/tot
    return accs
kms={2:canon_kmers(2),3:canon_kmers(3),4:canon_kmers(4)}
kb={'K2':(2,kms[2]),'K3':(3,kms[3]),'K4':(4,kms[4])}
out={'5kb':acc_at(kb,4,5000),'1kb':acc_at(kb,4,1000)}
print(json.dumps(out,indent=1))
json.dump(out,open('results/results.json','w'),indent=1)
a=out['5kb']
print('G1 K4 >= GC+0.30:',a['K4'],a['GC'])
print('G2 K4 >= K2+0.10:',a['K4'],a['K2'])
print('G3 1kb K4 >= 0.70:',out['1kb']['K4'])
with open('data/SHA256_raw.txt','w') as f:
    for fn in ('NC_000913.3.gb','NC_000964.3.gb','NC_000962.3.gb'):
        f.write(hashlib.sha256(open('data/'+fn,'rb').read()).hexdigest()+'  '+fn+'\n')
open('data/retrieved_at.txt','w').write(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())+' (files copied from algo50/04 downloads, same accessions)')
