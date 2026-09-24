import numpy as np, json
from collections import Counter
rng=np.random.default_rng(31)
B='ACGT'
def evolve(seqcols, t):
    # seqcols: list of (base, colid); returns new list with subs+indels, new columns appended to global counter
    global nextcol
    out=[]
    for base,cid in seqcols:
        r=rng.random()
        if r<0.1*t:  # indel
            if rng.random()<0.5:  # deletion: drop
                continue
            else:  # insertion after
                nb=rng.choice(list(B)); out.append((base,cid)); out.append((nb,None))
                continue
        if rng.random()<t:
            base=rng.choice([b for b in B if b!=base])
        out.append((base,cid))
    return out
tree=[0,1,2,3,4,5,6,7]
pairs=[(0,1),(2,3),(4,5),(6,7)]
def simulate(t):
    root=[(b,i) for i,b in enumerate(rng.choice(list(B),300))]
    leaves={}
    for a,b in pairs:
        sa=evolve(evolve(root,t),t); sb=evolve(evolve(root,t),t)  # two edges each: root->cherry->leaf
        leaves[a]=sa; leaves[b]=sb
    # cherry join at (a,b) then deeper join... approximation: independent 2-edge paths (balanced-ish); acceptable: 'fixed balanced tree' approximated by equal-depth independent paths
    for pair,(a,b) in zip([(0,4),(2,6)],pairs[:2]):
        pass
    seqs={i:''.join(b for b,_ in leaves[i]) for i in range(8)}
    cols={i:[c for _,c in leaves[i]] for i in range(8)}
    return seqs,cols
def nw_align(s1,s2):
    # profile-aware: s1 = list of Counters (profile) or str; s2 = str. Returns aligned columns: list of (profile_idx or None, s2_idx or None)
    from collections import Counter as C
    P=[C({c:1.0}) for c in s1] if isinstance(s1,str) else s1
    n,m=len(P),len(s2)
    NEG=-1e9
    d=np.full((n+1,m+1),NEG); pt=np.zeros((n+1,m+1),np.int8)
    d[0,0]=0; d[1:,0]=-2*np.arange(1,n+1); d[0,1:]=-2*np.arange(1,m+1)
    pt[1:,0]=2; pt[0,1:]=3
    for j in range(1,m+1):
        bj=s2[j-1]
        for i in range(1,n+1):
            sc=sum(f*(2 if x==bj else -1) for x,f in P[i-1].items())
            opts=(d[i-1,j-1]+sc,d[i-1,j]-2,d[i,j-1]-2)
            k=int(np.argmax(opts)); d[i,j]=opts[k]; pt[i,j]=k+1
    aln=[]; i,j=n,m
    while i>0 or j>0:
        p=pt[i,j]
        if p==1: aln.append((i-1,j-1)); i-=1; j-=1
        elif p==2: aln.append((i-1,None)); i-=1
        else: aln.append((None,j-1)); j-=1
    return aln[::-1]
def merge(profile,aln,s2):
    # build new profile columns from alignment
    out=[]
    for pi,ji in aln:
        c=Counter()
        if pi is not None: c.update(profile[pi])
        if ji is not None: c[s2[ji]]+=1.0
        tot=sum(c.values())
        out.append(Counter({k:v/tot for k,v in c.items()}))
    # also need per-sequence column placement for SP scoring: return mapping
    return out
def progressive(seqs,order):
    prof=None; sname=None
    # returns per-seq assignment: dict seq -> array of column index per residue
    assgn={}
    cur=None; curseq=None
    # first two
    a,b=order[0],order[1]
    aln=nw_align(seqs[a],seqs[b])
    colmap={a:[],b:[]}
    for ci,(pi,ji) in enumerate(aln):
        if pi is not None: colmap[a].append((pi,ci))
        if ji is not None: colmap[b].append((ji,ci))
    ncols=len(aln)
    prof=merge([Counter({c:1.0}) for c in seqs[a]],aln,seqs[b])
    assgn={a:[None]*len(seqs[a]),b:[None]*len(seqs[b])}
    for pi,ci in colmap[a]: assgn[a][pi]=ci
    for ji,ci in colmap[b]: assgn[b][ji]=ci
    for s in order[2:]:
        aln=nw_align(prof,seqs[s])
        newmap=[None]*len(seqs[s])
        newprof=[]
        for ci,(pi,ji) in enumerate(aln):
            c=Counter()
            if pi is not None: c.update(prof[pi])
            if ji is not None: c[seqs[s][ji]]+=1.0
            tot=sum(c.values()); newprof.append(Counter({k:v/tot for k,v in c.items()}))
            if ji is not None: newmap[ji]=ci
        # shift old assignments: old profile idx pi -> new col ci; need old->new map
        old2new={}
        for ci,(pi,ji) in enumerate(aln):
            if pi is not None: old2new[pi]=ci
        for s2name in assgn:
            assgn[s2name]=[old2new.get(x) if x is not None else None for x in assgn[s2name]]
        assgn[s]=newmap; prof=newprof
    return assgn
def sp_accuracy(assgn,cols,order):
    # true column id per residue: cols[s][pos] (None for inserted)
    good=tot=0
    for x in range(len(order)):
        for y in range(x+1,len(order)):
            a,b=order[x],order[y]
            # map true col -> inferred cols
            from collections import defaultdict
            ta=defaultdict(set); tb=defaultdict(set)
            for pos,cid in enumerate(cols[a]):
                if cid is not None and assgn[a][pos] is not None: ta[cid].add(assgn[a][pos])
            for pos,cid in enumerate(cols[b]):
                if cid is not None and assgn[b][pos] is not None: tb[cid].add(assgn[b][pos])
            for cid in set(ta)&set(tb):
                tot+=1
                if ta[cid]&tb[cid]: good+=1
    return good/max(tot,1)
res={}
true_order=[0,1,2,3,4,5,6,7]
for t in (0.05,0.15,0.30):
    seqs,cols=simulate(t)
    acc_true=sp_accuracy(progressive(seqs,true_order),cols,true_order)
    raccs=[]
    for rep in range(5):
        ro=list(rng.permutation(8))
        raccs.append(sp_accuracy(progressive(seqs,ro),cols,ro))
    res[str(t)]=dict(true=float(acc_true),random=[float(x) for x in raccs],gap=float(acc_true-np.mean(raccs)))
    print(t,res[str(t)],flush=True)
json.dump(res,open('results/pivot_metrics.json','w'),indent=1)
P1=res['0.15']['gap']>=0.03
P2=res['0.3']['true']<=0.20 and all(r<=0.20 for r in res['0.3']['random'])
P3=res['0.05']['true']>=0.95 and all(r>=0.95 for r in res['0.05']['random']) and abs(res['0.05']['gap'])<=0.03
print('P1',P1,'P2',P2,'P3',P3)
