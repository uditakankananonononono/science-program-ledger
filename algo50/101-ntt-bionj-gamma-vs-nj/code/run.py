import numpy as np, hashlib, tarfile, io, json, itertools
from Bio import Phylo
from Bio.Phylo.TreeConstruction import DistanceMatrix, DistanceTreeConstructor
assert hashlib.sha256(open('ntt.tar.gz','rb').read()).hexdigest()=='720d568e3d9b86a0f3fe065a3758b686bd9f68096c118273cda17069d13eff81'
t=tarfile.open('ntt.tar.gz'); fa=t.extractfile('ntt_sequences_trimal_automated1.phy').read(); tre=t.extractfile('ntt_c20.tre').read().decode()
assert hashlib.sha256(fa).hexdigest().startswith('f2fa1b07') and hashlib.sha256(tre.encode()).hexdigest().startswith('5d24de1c')
lines=fa.decode().splitlines(); hdr=lines[0].split(); assert hdr==['89','437']
names=[];seqs=[];ci=0
for l in lines[1:]:
    if not l.strip(): continue
    if len(names)<89: p=l.split(None,1); names.append(p[0]); seqs.append(p[1].replace(' ',''))
    else: seqs[ci%89]+=l.replace(' ','').strip(); ci+=1
AA='ACDEFGHIKLMNPQRSTVWY'; mp={c:i for i,c in enumerate(AA)}
X=np.array([[mp.get(c,-1) for c in s] for s in seqs],dtype=np.int8)
ref=Phylo.read(io.StringIO(tre),'newick'); tips=[c.name for c in ref.get_terminals()]
assert sorted(tips)==sorted(names) and X.shape==(89,437)
idx={n:i for i,n in enumerate(names)}
def ref_splits():
    out=[]
    for c in ref.get_nonterminals():
        s=frozenset(idx[x.name] for x in c.get_terminals())
        if 2<=len(s)<=87: out.append(s)
    return set(out)
RS=ref_splits()
def norm(s,taxa): # taxa: frozenset of all; unrooted normalisation: side containing min taxon excluded
    m=min(taxa); return s if m not in s else frozenset(taxa-s)
def prune(sub):
    sub=frozenset(sub); out=set()
    for s in RS:
        a=s&sub
        if 2<=len(a)<=len(sub)-2: out.add(norm(a,sub))
    return out
def dist(Xs,kind,a=1.0):
    n=len(Xs); P=np.full((n,n),0.9)
    for i in range(n):
        ok=(Xs[i]>=0)&(Xs>=0); m=ok.sum(1); mm=((Xs[i]!=Xs)&ok).sum(1)
        p=np.where(m>=30,mm/np.maximum(m,1),0.9); P[i]=np.minimum(p,0.9)
    np.fill_diagonal(P,0)
    if kind=='poisson': D=-np.log(1-P)
    elif kind=='kimura': D=-np.log(1-P-0.2*P**2)
    else: D=a*((1-P)**(-1/a)-1)
    return (D+D.T)/2
def nj_clusters(D,bionj=False):
    n=len(D); D=D.copy(); V=D.copy(); cl={i:frozenset([i]) for i in range(n)}; act=list(range(n)); out=[]
    while len(act)>3:
        A=np.array(act); sub=D[np.ix_(A,A)]; r=sub.sum(1); m=len(A)
        Q=(m-2)*sub-r[:,None]-r[None,:]; np.fill_diagonal(Q,np.inf)
        i,j=np.unravel_index(np.argmin(Q),Q.shape); a,b=A[i],A[j]
        dab=D[a,b]; dai=(dab+(r[i]-r[j])/(m-2))/2; dbi=dab-dai
        if bionj:
            vab=V[a,b]; lam=0.5
            if vab>0:
                oth=[k for k in act if k not in (a,b)]
                lam=0.5+(V[b,oth].sum()-V[a,oth].sum())/(2*(m-2)*vab)
                lam=min(1,max(0,lam))
        new=a
        for k in act:
            if k in (a,b): continue
            if bionj:
                dk=lam*(D[a,k]-dai)+(1-lam)*(D[b,k]-dbi); vk=lam*V[a,k]+(1-lam)*V[b,k]-lam*(1-lam)*V[a,b]
            else: dk=(D[a,k]+D[b,k]-dab)/2; vk=0
            D[new,k]=D[k,new]=dk; V[new,k]=V[k,new]=max(vk,0)
        cl[new]=cl[a]|cl[b]; out.append(cl[new]); act.remove(b)
    return out,[cl[k] for k in act]
def splits(D,bionj,sub):
    out,rest=nj_clusters(D,bionj); sub=frozenset(sub); res=set()
    # map local indices to global
    return out,rest
def est_splits(Xs,sub,D,bionj):
    cl,rest=nj_clusters(D,bionj); sub=list(sub); S=frozenset(sub); res=set()
    for c in cl:
        g=frozenset(sub[i] for i in c)
        if 2<=len(g)<=len(S)-2: res.add(norm(g,S))
    return res
def nrf(est,subs):
    r=prune(subs); return len(est^r)/max(1,len(est)+len(r))
# equivalence checks
rs=np.random.RandomState(5)
for _ in range(5):
    M=rs.rand(10,10)+0.5; M=(M+M.T)/2; np.fill_diagonal(M,0)
    mine=set(); cl,_=nj_clusters(M,False)
    S=frozenset(range(10)); mine={norm(c,S) for c in cl if 2<=len(c)<=8}
    dm=DistanceMatrix([str(i) for i in range(10)],[list(M[i,:i+1]) for i in range(10)])
    tr=DistanceTreeConstructor().nj(dm); bs=set()
    for c in tr.get_nonterminals():
        s=frozenset(int(x.name) for x in c.get_terminals())
        if 2<=len(s)<=8: bs.add(norm(s,S))
    assert mine==bs,'NJ equivalence'
# additive 12 taxon tree: caterpillar-ish random tree
def addmat(seed):
    r=np.random.RandomState(seed); n=12; adj={0:[],1:[]}; 
    edges=[(0,1,r.rand()+.2)]; nxt=n
    # build random tree by inserting leaves on edges
    for leaf in range(2,n):
        e=edges.pop(r.randint(len(edges))); u,v,w=e; mid=nxt; nxt+=1
        edges+= [(u,mid,w/2),(mid,v,w/2),(mid,leaf,r.rand()+.2)]
    N=nxt; G=np.full((N,N),np.inf); np.fill_diagonal(G,0)
    for u,v,w in edges: G[u,v]=G[v,u]=w
    for k in range(N): G=np.minimum(G,G[:,[k]]+G[[k],:])
    return G[:n,:n]
for sd in range(3):
    A=addmat(sd); a1,_=nj_clusters(A,False); a2,_=nj_clusters(A,True)
    S=frozenset(range(12)); s1={norm(c,S) for c in a1 if 2<=len(c)<=10}; s2={norm(c,S) for c in a2 if 2<=len(c)<=10}
    assert s1==s2,'BIONJ additive'
import os,sys
if os.environ.get('CHECK'): print('checks passed'); sys.exit()
cols=np.random.RandomState(11).permutation(437); DEVC,TESTC=cols[:218],cols[218:]
def reps(C,n,seed):
    r=np.random.RandomState(seed); out=[]
    for _ in range(n): out.append((np.sort(r.choice(89,40,replace=False)),r.choice(C,len(C),replace=True)))
    return out
def run(rp,cfgs):
    res={k:[] for k in cfgs}
    for sub,cc in rp:
        Xs=X[np.ix_(sub,cc)]; Dc={}
        for k,(kind,a,bio) in cfgs.items():
            key=(kind,a)
            if key not in Dc: Dc[key]=dist(Xs,kind,a)
            res[k].append(nrf(est_splits(Xs,sub,Dc[key],bio),sub))
    return {k:np.array(v) for k,v in res.items()}
AL=(0.5,1,2,5)
cf={'B1':('poisson',1,False),'B2':('kimura',1,False)}
for a in AL: cf[f'N{a}']=('gamma',a,True)
dv=run(reps(DEVC,100,21),cf); dm={k:float(v.mean()) for k,v in dv.items()}; print('DEV',dm,flush=True)
head='B1' if dm['B1']<=dm['B2'] else 'B2'; astar=min(AL,key=lambda a:(dm[f'N{a}'],-a))
cf2={'B1':cf['B1'],'B2':cf['B2'],'NEW':('gamma',astar,True),'NJ_gamma':('gamma',astar,False),'BIONJ_poisson':('poisson',1,True)}
tt=run(reps(TESTC,300,22),cf2)
d=tt[head]-tt['NEW']; rs=np.random.RandomState(7); bs=[d[rs.randint(0,300,300)].mean() for _ in range(10000)]
lo,hi=np.percentile(bs,[2.5,97.5]); rel=d.mean()/tt[head].mean(); v='WIN' if rel>=.05 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
res=dict(dev=dm,head=head,alpha=astar,alpha_at_edge=astar in (0.5,5),test_means={k:float(x.mean()) for k,x in tt.items()},diff=float(d.mean()),rel=float(rel),ci=[float(lo),float(hi)],verdict=v)
json.dump(res,open('results.json','w'),indent=1); print(json.dumps(res))
