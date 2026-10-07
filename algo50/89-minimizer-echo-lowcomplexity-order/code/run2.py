import numpy as np, json
from numpy.lib.stride_tricks import sliding_window_view as swv
K,W=15,10
def read(p):
    s=''.join(l.strip() for l in open(p) if not l.startswith('>')).upper()
    return np.frombuffer(s.encode(),dtype=np.uint8)
LUT=np.full(256,255,np.uint8)
for i,c in enumerate('ACGT'): LUT[ord(c)]=i
def kmers(a):
    x=LUT[a].astype(np.uint64); n=len(x)-K+1; v=np.zeros(n,np.uint64)
    for i in range(K): v=(v<<np.uint64(2))|x[i:i+n]
    return v,x
def sm(v):
    with np.errstate(over='ignore'):
        z=v+np.uint64(0x9E3779B97F4A7C15)
        z=(z^(z>>np.uint64(30)))*np.uint64(0xBF58476D1CE4E5B9)
        z=(z^(z>>np.uint64(27)))*np.uint64(0x94D049BB133111EB)
        return z^(z>>np.uint64(31))

def lowc(v,x,h,dd):
    n=len(v); lc=np.zeros(n,bool)
    if h<=K:
        eq=(x[1:]==x[:-1]).astype(np.int32); ce=np.concatenate([[0],np.cumsum(eq)])
        # kmer i has a run of >=h iff some window of h-1 consecutive equalities all true inside kmer: use sliding sum
        m=h-1; win=ce[m:]-ce[:-m]  # win[j]=sum eq[j:j+m]
        runstart=(win==m)  # len len(x)-m
        cs=np.concatenate([[0],np.cumsum(runstart)])
        i=np.arange(n); lc|=(cs[i+K-h+1]-cs[i])>0
    if dd>0:
        d=np.zeros((n,16),bool)
        for j in range(K-1):
            di=x[j:j+n].astype(np.int64)*4+x[j+1:j+1+n].astype(np.int64); d[np.arange(n),di]=True
        lc|=d.sum(1)<=dd
    return lc
def rank(v,x,h,dd):
    r=sm(v)>>np.uint64(1)
    if h<=K or dd>0: r=r+(lowc(v,x,h,dd).astype(np.uint64)<<np.uint64(63))
    return r
def sel(r):
    win=swv(r,W); return np.arange(len(win))+win.argmin(1)
def mutate(a,seed):
    rs=np.random.RandomState(seed); b=a.copy(); m=rs.rand(len(a))<0.05
    alts=np.frombuffer(b'ACGT',np.uint8)
    for i in np.where(m)[0]:
        c=[z for z in alts if z!=b[i]]; b[i]=c[rs.randint(3)]
    return b
def measure(name,cells):
    a=read(f'data/{name}.fa'); v,x=kmers(a); res={}
    muts=[kmers(mutate(a,sd)) for sd in range(10)]
    for (h,dd) in cells:
        r=rank(v,x,h,dd); so=np.unique(sel(r)); cons=[]
        for vm,xm in muts: cons.append(np.isin(so,np.unique(sel(rank(vm,xm,h,dd)))).mean())
        res[(h,dd)]=(len(so)/len(v),float(np.mean(cons)))
    return res
if __name__=='__main__':
    import itertools
    cells=[(h,d) for h in (6,8,10,99) for d in (0,2,3,4)]
    # check: (5,4) here is v1's gate; ensure equivalence on phiX
    dev={n:measure(n,cells) for n in ('NC_001422.1','NC_001416.1')}
    base={n:dev[n][(99,0)] for n in dev}
    J={}
    for c in cells:
        J[c]=np.mean([(dev[n][c][1]-base[n][1])/base[n][1]-(dev[n][c][0]-base[n][0])/base[n][0] for n in dev])
    order=sorted(cells,key=lambda c:(-round(J[c],12),-(c[0]),c[1]))
    best=order[0]; print('DEV J',{str(c):round(J[c],4) for c in cells},'best',best,flush=True)
    out=dict(best=list(best),J={str(c):J[c] for c in cells})
    for n in ('NC_000964.3','NC_000913.3'):
        r=measure(n,[(99,0),best]); B=r[(99,0)];E=r[best]
        dg=E[0]<=B[0]*.97; cg=E[1]>=B[1]+.01; bad=E[0]>B[0]*1.03 or E[1]<B[1]-.01
        vd='WIN' if (dg or cg) and not bad else ('NEGATIVE' if bad else 'NULL')
        if best==(99,0): vd='NULL'
        out[n]=dict(base=B,echo2=E,verdict=vd,role='HOLDOUT' if n=='NC_000964.3' else 'second-look'); print(n,out[n],flush=True)
    json.dump(out,open('results_v2.json','w'),indent=1,default=float)
