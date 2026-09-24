import numpy as np, json
rng=np.random.default_rng(11)
B='ACGT'
G=120000
base=''.join(rng.choice(list(B),G))
reps=[200,400,800,1600,3200,6400,300,500]
# implant second copies; record repeat regions
g=list(base)
src=[]; dst=[]
used=np.zeros(G+7000,bool)
def free(n):
    while True:
        p=rng.integers(0,G-n)
        if not used[p:p+n].any(): used[p:p+n]=True; return p
for R in reps:
    a=free(R); b=free(R)
    g[b:b+R]=g[a:a+R]; src.append((a,R)); dst.append((b,R))
g=''.join(g)
def n50(lens):
    lens=sorted(lens,reverse=True); tot=sum(lens); acc=0
    for L in lens:
        acc+=L
        if acc>=tot/2: return L
def dbg_unitigs(g,k):
    from collections import defaultdict
    adj=defaultdict(set); radj=defaultdict(set)
    for i in range(len(g)-k+1):
        a,b=g[i:i+k-1],g[i+1:i+k]
        adj[a].add(b); radj[b].add(a)
    nodes=set(adj)|set(radj)
    outd={n:len(adj[n]) for n in nodes}; ind={n:len(radj[n]) for n in nodes}
    unitigs=[]
    for n in nodes:
        if outd[n]!=1 or ind[n]!=1:
            for m in adj[n]:
                L=k; cur=m
                while ind[cur]==1 and outd[cur]==1:
                    L+=1; cur=next(iter(adj[cur]))
                unitigs.append(L)
    # pure cycles (no branching anywhere on the cycle)
    return unitigs,outd,ind,adj
res={}
for k in (15,21,31,51,75,99):
    unitigs,outd,ind,adj=dbg_unitigs(g,k)
    nn=n50(unitigs) if unitigs else 0
    cov=sum(unitigs)/len(g) if unitigs else 0
    # branch detection per repeat: a repeat R unresolved if any k-mer interior occurs twice
    # cheaper: count k-mers with multiplicity>1 located in repeat interiors
    from collections import Counter
    kc=Counter(g[i:i+k] for i in range(len(g)-k+1))
    unresolved=0
    for (a,R),(b,R2) in zip(src,dst):
        if R>=k:
            # interior k-mer fully inside repeat appears at both copies
            mid=g[a+R//2:a+R//2+k]
            if kc[mid]>1: unresolved+=1
    res[k]=dict(n50=nn,n_unitigs=len(unitigs),cov=cov,unresolved=unresolved,
                expected_unresolved=sum(1 for _,R in src if R>=k))
    print(k,res[k],flush=True)
json.dump(res,open('results/results.json','w'),indent=1)
r=res
g1=all(r[b]['n50']>=0.9*r[a]['n50'] for a,b in zip((15,21,31,51,75),(21,31,51,75,99)))
g2=all(r[k]['unresolved']>=0.9*r[k]['expected_unresolved'] for k in (15,21,31,51) if r[k]['expected_unresolved']>0)
g3=r[15]['n50']<=0.2*r[99]['n50']
g4=all(r[k]['cov']>=0.99 for k in r)
print('G1',g1,'G2',g2,'G3',g3,'G4',g4)
