import numpy as np, json
# simpler direct implementations
def make_tree(rng,n,clock):
    # coalescent for clock; random joining with exp lengths for non-clock base
    active=list(range(n)); t={i:0.0 for i in active}; nextid=n; edges=[]
    inc=sorted(rng.exponential(1.0,n-1))
    hprev=0.0
    for step in range(n-1):
        i,j=sorted(rng.choice(len(active),2,replace=False))
        a,b=active[i],active[j]
        if clock:
            h=inc[step]; l1=h-t[a]; l2=h-t[b]; 
        else:
            l1=rng.exponential(0.2); l2=rng.exponential(0.2)
        edges.append((a,nextid,l1)); edges.append((b,nextid,l2))
        t[nextid]=t[a]+l1
        active=[x for k,x in enumerate(active) if k not in (i,j)]+[nextid]
        nextid+=1
    root=active[0]
    # scale to mean root-to-tip ~0.25 (clock) or as-is
    if clock:
        tot=t[root]; sc=0.25/tot
        edges=[(c,p,l*sc) for c,p,l in edges]
    return edges,root
def ratevar(edges,rng,sigma=0.5):
    return [(c,p,l*np.exp(rng.normal(0,sigma))) for c,p,l in edges]
def evolve(edges,root,rng,n,L):
    children={}
    for c,p,l in edges: children.setdefault(p,[]).append((c,l))
    seqs={root:rng.integers(0,4,L)}
    stack=[root]
    while stack:
        p=stack.pop()
        for c,l in children.get(p,[]):
            s=seqs[p].copy()
            prob=0.75*(1-np.exp(-4/3*l))
            mut=rng.random(L)<prob
            s[mut]=rng.integers(0,4,mut.sum())
            seqs[c]=s; stack.append(c)
    return np.array([seqs[i] for i in range(n)])
def jc69(S):
    n=len(S); D=np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            p=(S[i]!=S[j]).mean()
            p=min(p,0.749)
            D[i,j]=D[j,i]=-0.75*np.log(1-4/3*p)
    return D
def upgma(D):
    n=len(D); active=list(range(n)); size={i:1 for i in active}
    dist={(i,j):D[i,j] for i in range(n) for j in range(i+1,n)}
    nextid=n; edges=[]
    def key(a,b): return (min(a,b),max(a,b))
    while len(active)>1:
        best=None;ba=bb=None
        for x in range(len(active)):
            for y in range(x+1,len(active)):
                a,b=active[x],active[y]; d=dist[key(a,b)]
                if best is None or d<best: best=d; ba,bb=a,b
        edges.append((ba,nextid)); edges.append((bb,nextid))
        for a in active:
            if a in (ba,bb): continue
            dist[key(a,nextid)]=(dist[key(a,ba)]*size[ba]+dist[key(a,bb)]*size[bb])/(size[ba]+size[bb])
        size[nextid]=size[ba]+size[bb]
        active=[a for a in active if a not in (ba,bb)]+[nextid]
        nextid+=1
    return edges,nextid-1
def nj(D0):
    n=len(D0); D=D0.copy()
    ids=list(range(n)); Dd={(i,j):D[i,j] for i in range(n) for j in range(n)}
    nextid=n; edges=[]; active=list(range(n))
    def d(a,b): return Dd[(min(a,b),max(a,b))] if a!=b else 0.0
    while len(active)>2:
        m=len(active)
        r={a:sum(d(a,b) for b in active) for a in active}
        best=None; ba=bb=None
        for x in range(m):
            for y in range(x+1,m):
                a,b=active[x],active[y]
                q=(m-2)*d(a,b)-r[a]-r[b]
                if best is None or q<best: best=q;ba,bb=a,b
        for a in active:
            if a in (ba,bb): continue
            Dd[(min(a,nextid),max(a,nextid))]=(d(a,ba)+d(a,bb)-d(ba,bb))/2
        edges.append((ba,nextid)); edges.append((bb,nextid))
        active=[a for a in active if a not in (ba,bb)]+[nextid]
        nextid+=1
    edges.append((active[0],active[1]))  # final pair edge (as undirected)
    return edges
def splits_from_edges(edges,n,rooted_final_pair=True):
    # build undirected adjacency, get internal splits
    adj={}
    for a,b in edges:
        adj.setdefault(a,set()).add(b); adj.setdefault(b,set()).add(a)
    splits=set()
    internal=[x for x in adj if x>=n]
    # for each internal edge: removing edge splits taxa; enumerate edges between internal nodes
    seen=set()
    def reach(src,blocked):
        out=set(); st=[src]
        while st:
            x=st.pop()
            for y in adj[x]:
                if y==blocked or y in out: continue
                out.add(y); st.append(y)
        return out
    for a in internal:
        for b in adj[a]:
            if b<n: continue
            e=(min(a,b),max(a,b))
            if e in seen: continue
            seen.add(e)
            comp=reach(a,b)
            taxa=frozenset(x for x in comp if x<n)
            other=frozenset(range(n))-taxa
            splits.add(min(taxa,other,key=len))
    return splits
def nrf(true_edges,inf_edges,n):
    st=splits_from_edges(true_edges,n); si=splits_from_edges(inf_edges,n)
    if not st and not si: return 0.0
    return len(st^si)/max(1,(len(st)+len(si)))
rng=np.random.default_rng(1)
res={'CLOCK':[],'RATEVAR':[]}
n=32; L=1000; REPS=100
for rep in range(REPS):
    r=np.random.default_rng(1000+rep)
    edges,root=make_tree(r,n,True)
    for regime,ed in (('CLOCK',edges),('RATEVAR',ratevar(edges,r))):
        S=evolve(ed,root,r,n,L)
        D=jc69(S)
        ue,_=upgma(D); ne=nj(D)
        ted=[(c,p) for c,p,l in ed]
        res[regime].append((nrf(ted,ue,n),nrf(ted,ne,n)))
    if rep%20==0: print('rep',rep)
out={}
for reg in res:
    a=np.array(res[reg])
    out[reg]={'UPGMA':float(a[:,0].mean()),'NJ':float(a[:,1].mean())}
print(json.dumps(out,indent=1))
json.dump(out,open('results/results.json','w'),indent=1)
print('G1 RATEVAR NJ <= UPGMA-0.05:',out['RATEVAR']['NJ'],out['RATEVAR']['UPGMA'])
print('G2 CLOCK NJ <= UPGMA+0.05:',out['CLOCK']['NJ'],out['CLOCK']['UPGMA'])
print('G3 ratevar-upgma >= clock-upgma+0.05:',out['RATEVAR']['UPGMA'],out['CLOCK']['UPGMA'])
print('G4 NJ ratevar <= 0.25:',out['RATEVAR']['NJ'])
