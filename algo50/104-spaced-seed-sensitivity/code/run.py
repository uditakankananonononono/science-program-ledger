import numpy as np, json
LUT=np.full(256,255,np.uint8)
for i,c in enumerate('ACGT'): LUT[ord(c)]=i
def read(a):
    s=''.join(l.strip() for l in open(f'data/{a}.fa') if not l.startswith('>')).upper(); return LUT[np.frombuffer(s.encode(),np.uint8)]
L=80
def sim(g,n,seed):
    rs=np.random.RandomState(seed); D=np.full((n,L),-1,np.int64); R=np.zeros((n,L),np.uint8)
    for r in range(n):
        p=rs.randint(0,len(g)-3*L); i=0
        while i<L:
            u=rs.rand()
            if u<.02: p+=1; continue            # deletion: skip ref base
            if u<.04: R[r,i]=rs.randint(4); D[r,i]=-1; i+=1; continue  # insertion
            if u<.14: R[r,i]=(g[p]+1+rs.randint(3))%4; D[r,i]=-1; p+=1; i+=1; continue # substitution
            R[r,i]=g[p]; D[r,i]=p-i; p+=1; i+=1
    return R,D
def sens(pat,D):
    P=np.array([i for i,c in enumerate(pat) if c=='1']); span=len(pat); hit=np.zeros(len(D),bool)
    for o in range(L-span+1):
        S=D[:,o+P]; hit|=((S>=0).all(1))&((S==S[:,[0]]).all(1))
    return hit
def rand_pat(rs):
    n=rs.randint(14,27); inner=rs.choice(n-2,9,replace=False)+1; b=np.zeros(n,int); b[0]=b[-1]=1; b[inner]=1; return ''.join(map(str,b))
gd=[read('NC_001422.1'),read('NC_001416.1')]
R1,D1=sim(gd[0],750,1); R2,D2=sim(gd[1],750,2); Dd=np.vstack([D1,D2])
rs=np.random.RandomState(0); cand=[rand_pat(rs) for _ in range(600)]
sc=[(sens(p,Dd).mean(),-len(p),p) for p in cand]; best=max(sc); NEW=best[2]
PH='111010010100110111'; CT='1'*11
print('DEV',{k:round(float(sens(p,Dd).mean()),4) for k,p in (('new',NEW),('ph',PH),('contig',CT))},NEW,flush=True)
g=read('NC_000913.3'); Rt,Dt=sim(g,3000,5)
hn,hp,hc=sens(NEW,Dt),sens(PH,Dt),sens(CT,Dt)
# equivalence: direct string scan for contiguous seed on first 200 reads
def direct(R,D,n):
    ok=[]
    for r in range(n):
        h=False
        for o in range(L-11+1):
            seg=D[r,o:o+11]
            if (seg>=0).all() and (seg==seg[0]).all(): h=True;break
        ok.append(h)
    return np.array(ok)
assert (direct(Rt,Dt,200)==hc[:200]).all()
# off-target specificity (first 300 reads): count exact seed matches elsewhere in index
def offt(pat,R,n):
    P=np.array([i for i,c in enumerate(pat) if c=='1']); span=len(pat)
    key=np.zeros(len(g)-span+1,np.int64)
    for p in P: key=(key<<2)|g[p:p+len(key)]
    ks=np.sort(key); tot=0
    for r in range(n):
        for o in range(L-span+1):
            q=0
            for p in P: q=(q<<2)|int(R[r,o+p])
            tot+=np.searchsorted(ks,q,'right')-np.searchsorted(ks,q,'left')
    return tot/n
rs7=np.random.RandomState(7); N=len(hn); bs=[]
for _ in range(10000):
    i=rs7.randint(0,N,N); bs.append(hn[i].mean()-hp[i].mean())
lo,hi=np.percentile(bs,[2.5,97.5]); d=hn.mean()-hp.mean()
v='WIN' if d>=.01 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
out=dict(new=NEW,dev={'new':float(best[0])},holdout=dict(new=float(hn.mean()),ph=float(hp.mean()),contig=float(hc.mean())),diff_vs_ph=float(d),ci=[float(lo),float(hi)],verdict=v,offtarget={'new':offt(NEW,Rt,300),'ph':offt(PH,Rt,300),'contig':offt(CT,Rt,300)})
json.dump(out,open('results.json','w'),indent=1,default=float); print(json.dumps(out,default=float))
