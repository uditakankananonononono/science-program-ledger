import gzip,numpy as np,collections,sys
CH=['chr1','chr2','chr3','chr21','chr22']
don=collections.defaultdict(set)  # chrom -> set of (pos_of_G_0based, strand)
ex=collections.defaultdict(list)
with gzip.open('../data/gencode.v44.basic.annotation.gtf.gz','rt') as f:
    for l in f:
        if l[0]=='#': continue
        t=l.split('\t',9)
        if t[2]!='exon' or t[0] not in CH: continue
        tid=t[8].split('transcript_id "')[1].split('"')[0]
        ex[tid].append((t[0],int(t[3]),int(t[4]),t[6]))
for tid,es in ex.items():
    es.sort(key=lambda e:e[1])
    if len(es)<2: continue
    c,s=es[0][0],es[0][3]
    if s=='+':
        for e in es[:-1]: don[c].add((e[2],'+'))        # G at 0-based e[2] (1-based end+1)
    else:
        for e in es[1:]: don[c].add((e[1]-2,'-'))       # C of revcomp GT at 0-based start-2; G on minus at start-1(1b)
comp=str.maketrans('ACGT','TGCA')
def rd(c):
    with gzip.open(f'../data/{c}.fa.gz','rt') as f: return ''.join(x.strip() for x in f if x[0]!='>').upper()
rng=np.random.default_rng(29); out={}
for c in CH:
    g=rd(c); pos=[];neg=[]
    D=don[c]
    def win(p,s):
        if s=='+': w=g[p-3:p+6]
        else: w=g[p-5:p+4].translate(comp)[::-1]
        return w
    # minus strand: donor intron start 'GT' appears as 'AC' ending at 0-based start-1; G(minus) = 0-based start-2... handle: p=start-2 -> C at p? check
    for p,s in D:
        w=win(p,s)
        if len(w)==9 and set(w)<=set('ACGT'): pos.append(w)
    A=np.frombuffer(g.encode(),dtype=np.uint8)
    pp=np.flatnonzero((A[:-1]==71)&(A[1:]==84)); pm=np.flatnonzero((A[:-1]==65)&(A[1:]==67))+1
    del A
    k=600000 if c in('chr21','chr22') else 400000
    tot=len(pp)+len(pm); idx=rng.choice(tot,int(k*1.02),replace=False)
    for i in idx:
        x=(int(pp[i]),'+') if i<len(pp) else (int(pm[i-len(pp)]),'-')
        if x in D: continue
        w=win(*x)
        if len(w)==9 and set(w)<=set('ACGT'): neg.append(w)
    del pp,pm
    gt=collections.Counter(w[3:5] for w in pos)
    print(c,len(pos),len(neg),gt.most_common(4),flush=True)
    out[c]=(pos,neg)
import pickle;pickle.dump(out,open('../data/sites.pkl','wb'))
