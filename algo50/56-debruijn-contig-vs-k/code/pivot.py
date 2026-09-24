import numpy as np, json
from collections import defaultdict
rng=np.random.default_rng(11)
B='ACGT'
G=120000
base=''.join(rng.choice(list(B),G))
reps=[200,400,800,1600,3200,6400,300,500]
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
arr=np.frombuffer(g.encode(),dtype=np.uint8).astype(np.uint64)
U=np.uint64
def unitigs_hashed(k):
    n=len(g)-k+1
    # rolling hash of (k-1)-mer
    pw=U(pow(5,k-2,1<<64))
    hh=U(0)
    for i in range(k-1): hh=hh*U(5)+arr[i]
    pos_of={}; adj=defaultdict(set); radj=defaultdict(set)
    hashes=np.empty(n+1,dtype=np.uint64)
    for i in range(n+1):
        if i>0:
            hh=(hh - arr[i-1]*pw)*U(5) + arr[i+k-2]
        hashes[i]=hh
    for i in range(n):
        a=hashes[i]; b=hashes[i+1]
        pos_of.setdefault(a,i)
        adj[a].add(arr[i+k-1]); radj[b].add(arr[i])
    nodes=set(pos_of)|set(radj)
    outd={x:len(adj[x]) for x in nodes}; ind={x:len(radj[x]) for x in nodes}
    unitigs=[]
    for x in nodes:
        if outd[x]!=1 or ind[x]!=1:
            for c in adj[x]:
                # walk from position of x
                p=pos_of[x]; L=k; cur=x
                while True:
                    succ=adj[cur]
                    # move: cur -> hash of next (k-1)-mer = hashes[pos+1] where pos=pos_of[cur]
                    pc=pos_of[cur]
                    nh=hashes[pc+1]
                    cur=nh
                    if ind[cur]==1 and outd[cur]==1:
                        L+=1
                    else:
                        break
                unitigs.append(L)
    return unitigs
res={}
for k in (15,51,99,250,600,1500,7000):
    u=unitigs_hashed(k)
    lens=sorted(u,reverse=True); tot=sum(lens); acc=0; n50=0
    for L in lens:
        acc+=L
        if acc>=tot/2: n50=L; break
    exp_unres=sum(1 for _,R in src if R>=k)
    # unresolved measured: repeats whose interior (k-1)-mer multiplicity >1 -> infer from graph: count repeats with R>=k that are NOT resolved. Direct: check k-mer multiplicity via hashes
    # simpler: expected from construction; verify by checking interior multiplicity
    n=len(g)-k+1
    from collections import Counter
    kc=Counter(); hh=U(0)
    pw=U(pow(5,k-1,1<<64)); hh=U(0)
    for i in range(k): hh=hh*U(5)+arr[i]
    kc[hh]+=1
    for i in range(1,n):
        hh=(hh - arr[i-1]*pw)*U(5) + arr[i+k-1]
        kc[hh]+=1
    unres=0
    for (a,R),(b,R2) in zip(src,dst):
        if R>=k:
            h2=U(0)
            st=a+max(0,(R-k)//2)
            for j in range(st,st+k): h2=h2*U(5)+arr[j]
            if kc[h2]>1: unres+=1
    collapsed=sum(R for _,R in src)
    res[k]=dict(n50=n50,n_unitigs=len(u),cov_corr=tot/(len(g)-collapsed),unresolved=unres,expected_unresolved=exp_unres)
    print(k,res[k],flush=True)
json.dump(res,open('results/pivot_metrics.json','w'),indent=1)
r=res
P1=all(r[k]['unresolved']==r[k]['expected_unresolved'] for k in r)
P2=all(r[b]['n50']>r[a]['n50'] for a,b in ((99,250),(250,600),(600,1500),(1500,7000)))
P3=(r[7000]['n_unitigs']==1)
print('P1',P1,'P2',P2,'P3',P3)
