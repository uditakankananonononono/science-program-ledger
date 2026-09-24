import numpy as np, json
rng=np.random.default_rng(83)
# outbreak tree
cases=[(0,0,-1)]  # (id, infection_day, infector)
day=0; frontier=[0]; nextid=1
while len(cases)<42:
    newf=[]
    for c in frontier:
        for _ in range(rng.poisson(1.2)+ (1 if rng.random()<0.3 else 0)):
            if len(cases)>=42: break
            gi=int(np.clip(rng.normal(5,2),1,15))
            cases.append((nextid,cases[c][1]+gi,c)); newf.append(nextid); nextid+=1
    frontier=newf
    if not frontier: break
n=len(cases)
# genomes: sets of mutated positions over 30000
G=30000
genomes={0:set()}
for cid,dayi,inf in cases[1:]:
    dt=dayi-cases[inf][1]
    muts=set(genomes[inf])
    # substitutions accumulate ~0.068/day (25/year)
    k=rng.poisson(0.068*dt)
    for _ in range(k):
        pos=int(rng.integers(0,G))
        if pos in muts: muts.discard(pos)
        else: muts.add(pos)
    genomes[cid]=muts
# sampling day = infection + 0..15
samp={cid: dayi+int(rng.integers(0,16)) for cid,dayi,_ in cases}
pairs=[]
for i in range(n):
    for j in range(i+1,n):
        d=len(genomes[i]^genomes[j])
        pairs.append((i,j,d))
truth=set()
for cid,dayi,inf in cases[1:]:
    truth.add((min(cid,inf),max(cid,inf)))
def f1(T,timefilter=False):
    tp=fp=fn=0
    for i,j,d in pairs:
        pred=d<=T
        if timefilter and pred: pred = samp[i]<samp[j] or samp[j]<samp[i] and abs(samp[i]-samp[j])<=20
        if timefilter: pred = pred and abs(samp[i]-samp[j])<=20
        t=(i,j) in truth
        tp+=pred and t; fp+=pred and not t; fn+=(not pred) and t
    p=tp/max(tp+fp,1); r=tp/max(tp+fn,1)
    return p,r,(2*p*r/max(p+r,1e-9))
res={}
for T in range(0,9):
    p,r,f=f1(T); res[T]=dict(p=p,r=r,f=f)
    print(T,res[T],flush=True)
best=max(res,key=lambda t:res[t]['f'])
tf={T:f1(T,True)[2] for T in range(0,9)}
best_tf=max(tf,key=lambda t:tf[t])
res['best']=best; res['best_timefilter']=best_tf; res['f_timefilter']=tf[best_tf]
json.dump(res,open('results/results.json','w'),indent=1)
print('best T',best,'F1',res[best]['f'],'timefilter best',best_tf,tf[best_tf])
print('G1',res[best]['f']>=0.60,'G2',best in (1,2,3),'G3',tf[best_tf]>=res[best]['f']+0.05,'G4',res[best]['p']>=0.70)
