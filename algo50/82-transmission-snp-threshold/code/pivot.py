import numpy as np, json
rng=np.random.default_rng(83)
cases=[(0,0,-1)]; day=0; frontier=[0]; nextid=1
while len(cases)<42:
    newf=[]
    for c in frontier:
        for _ in range(rng.poisson(1.2)+(1 if rng.random()<0.3 else 0)):
            if len(cases)>=42: break
            gi=int(np.clip(rng.normal(5,2),1,15))
            cases.append((nextid,cases[c][1]+gi,c)); newf.append(nextid); nextid+=1
    frontier=newf
    if not frontier: break
n=len(cases)
G=30000
genomes={0:set()}
for cid,dayi,inf in cases[1:]:
    dt=dayi-cases[inf][1]
    muts=set(genomes[inf])
    for _ in range(rng.poisson(0.068*dt)):
        pos=int(rng.integers(0,G))
        if pos in muts: muts.discard(pos)
        else: muts.add(pos)
    genomes[cid]=muts
parent={cid:inf for cid,_,inf in cases[1:]}
def steps(i,j):
    # distance on tree
    di={}; d=0; x=i
    while x!=-1: di[x]=d; d+=1; x=parent.get(x,-1)
    d=0; x=j
    while x not in di: d+=1; x=parent.get(x,-1)
    return di[x]+d
truth=set()
for i in range(n):
    for j in range(i+1,n):
        if steps(i,j)<=2: truth.add((i,j))
pairs=[]
for i in range(n):
    for j in range(i+1,n):
        pairs.append((i,j,len(genomes[i]^genomes[j])))
res={}
for T in range(0,9):
    tp=fp=fn=0
    for i,j,d in pairs:
        pred=d<=T; t=(i,j) in truth
        tp+=pred and t; fp+=pred and not t; fn+=(not pred) and t
    p=tp/max(tp+fp,1); r=tp/max(tp+fn,1)
    res[T]=dict(p=p,r=r,f=2*p*r/max(p+r,1e-9))
    print(T,res[T],flush=True)
best=max(res,key=lambda t:res[t]['f'])
json.dump(res,open('results/pivot_metrics.json','w'),indent=1)
print('best T',best,'F1',res[best]['f'])
print('P1',res[best]['f']>=0.70,'P2',res[best]['p']>=0.80,'P3',best in (1,2,3))
