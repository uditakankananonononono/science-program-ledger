import json, random
import numpy as np
data=json.load(open('data/eval.json'))
PAIR={'GC','CG','AU','UA','GU','UG'}
def ptype(a,b):
    s=a+b
    return {'GC':'GC','CG':'GC','AU':'AU','UA':'AU','GU':'GU','UG':'GU'}[s]
def fold(seq,method):
    n=len(seq)
    can=np.zeros((n,n),bool)
    for i in range(n):
        for j in range(i+4,n):
            if seq[i]+seq[j] in PAIR: can[i,j]=True
    if method in ('NUSS','WC'):
        F=np.zeros((n+1,n+1)); 
        for i in range(n-1,-1,-1):
            for j in range(i+1,n):
                best=F[i+1,j] if F[i+1,j]>=F[i,j-1] else F[i,j-1]
                if can[i,j] and not (method=='WC' and seq[i]+seq[j] in ('GU','UG')):
                    v=1+F[i+1,j-1]
                    if v>best: best=v
                for k in range(i+1,j):
                    v=F[i,k]+F[k+1,j]
                    if v>best: best=v
                F[i,j]=best
        pairs=[]; stack=[(0,n-1)]
        while stack:
            i,j=stack.pop()
            if i>=j: continue
            if F[i,j]==F[i+1,j]: stack.append((i+1,j))
            elif F[i,j]==F[i,j-1]: stack.append((i,j-1))
            elif can[i,j] and not (method=='WC' and seq[i]+seq[j] in ('GU','UG')) and F[i,j]==1+F[i+1,j-1]:
                pairs.append((i,j)); stack.append((i+1,j-1))
            else:
                for k in range(i+1,j):
                    if F[i,j]==F[i,k]+F[k+1,j]:
                        stack.append((i,k)); stack.append((k+1,j)); break
        return set(pairs)
    # ENERGY
    PE={'GC':-3.0,'AU':-2.0,'GU':-1.0}
    def stackE(o,i2):
        if o=='GC': return -3.0 if i2=='GC' else -2.5
        if o=='AU': return {'GC':-2.0,'AU':-1.5,'GU':-1.0}[i2]
        return -0.5
    INF=float('inf')
    W=np.zeros((n+1,n+1)); V=np.full((n+1,n+1),INF)
    for i in range(n-1,-1,-1):
        for j in range(i+1,n):
            w=min(W[i+1,j],W[i,j-1])
            for k in range(i+1,j):
                v=W[i,k]+W[k+1,j]
                if v<w: w=v
            if can[i,j]:
                l=j-i-1
                v=PE[ptype(seq[i],seq[j])]+4.0+0.5*l  # hairpin
                if W[i+1,j-1]<v-PE[ptype(seq[i],seq[j])]:
                    v=PE[ptype(seq[i],seq[j])]+W[i+1,j-1]
                if can[i+1,j-1]:
                    vs=PE[ptype(seq[i],seq[j])]+stackE(ptype(seq[i],seq[j]),ptype(seq[i+1],seq[j-1]))+V[i+1,j-1]
                    if vs<v: v=vs
                V[i,j]=v
                if v<w: w=v
            W[i,j]=w
    pairs=[]; stack=[('W',0,n-1)]
    while stack:
        t,i,j=stack.pop()
        if i>=j: continue
        if t=='W':
            w=W[i,j]
            if w==W[i+1,j]: stack.append(('W',i+1,j))
            elif w==W[i,j-1]: stack.append(('W',i,j-1))
            elif can[i,j] and w==V[i,j]: stack.append(('V',i,j))
            else:
                for k in range(i+1,j):
                    if w==W[i,k]+W[k+1,j]:
                        stack.append(('W',i,k)); stack.append(('W',k+1,j)); break
        else:
            pairs.append((i,j))
            pt=ptype(seq[i],seq[j]); l=j-i-1
            v=V[i,j]-PE[pt]
            if abs(v-(4.0+0.5*l))<1e-9: continue
            if can[i+1,j-1] and abs(v-(stackE(pt,ptype(seq[i+1],seq[j-1]))+V[i+1,j-1]))<1e-9:
                stack.append(('V',i+1,j-1))
            else: stack.append(('W',i+1,j-1))
    return set(pairs)
def prf(pred,ref):
    ref=set(map(tuple,ref))
    tp=len(pred&ref)
    p=tp/len(pred) if pred else 0.0; r=tp/len(ref) if ref else 0.0
    f=2*p*r/(p+r) if p+r else 0.0
    return p,r,f
res={}
for fam in ('RF00005','RF00001'):
    rows=data[fam]
    m={x:[] for x in ('NUSS','WC','ENERGY')}
    for row in rows:
        seq=row['seq']
        for meth in m:
            m[meth].append(prf(fold(seq,meth),row['ref'])[2])
    res[fam]={k:float(np.mean(v)) for k,v in m.items()}
    print(fam,res[fam])
# specificity control: dinucleotide shuffle of tRNAs
rng=random.Random(1)
def dinuc_shuffle(s):
    # simple Eulerian-ish: swap-based preserving dinucleotides approximately via Altschul-Erickson is overkill;
    # use chunk permutation of dinucleotide blocks at random cut points (documented approximation)
    blocks=[s[i:i+2] for i in range(0,len(s)-1,2)]
    tail=s[-1] if len(s)%2 else ''
    rng.shuffle(blocks)
    return ''.join(blocks)+tail
real=[]; shuf=[]
for row in data['RF00005']:
    real.append(len(fold(row['seq'],'ENERGY')))
    shuf.append(len(fold(dinuc_shuffle(row['seq']),'ENERGY')))
res['specificity']={'real_median':float(np.median(real)),'shuf_median':float(np.median(shuf))}
print(res['specificity'])
json.dump(res,open('results/results.json','w'),indent=1)
print('G1',res['RF00005']['ENERGY']-res['RF00005']['NUSS'])
print('G2',res['RF00001']['ENERGY']-res['RF00001']['NUSS'])
