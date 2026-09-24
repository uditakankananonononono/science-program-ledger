import numpy as np, json, random
rng=np.random.default_rng(61); pyrand=random.Random(61)
B='ACGT'
# families: family consensus 500bp; targets = copies with 40% positions resampled within shared motif pool
targets=[]; kmer_sets=[]
KF=25
for f in range(25):
    cons=''.join(rng.choice(list(B),500))
    for i in range(8):
        t=list(cons)
        # 40% of positions re-drawn: 60% shared within family
        for p in range(500):
            if rng.random()<0.4: t[p]=rng.choice(list(B))
        t=''.join(t); targets.append(t)
        kmer_sets.append({t[j:j+KF] for j in range(500-KF+1)})
allkmers={}
for i,ks in enumerate(kmer_sets):
    for k in ks: allkmers.setdefault(k,set()).add(i)
print('targets',len(targets),'distinct kmers',len(allkmers),flush=True)
# greedy
covered=set(); greedy=[]
kmap={k:set(v) for k,v in allkmers.items()}
remaining=dict(kmap)
while len(covered)<200:
    best=None; bestc=-1
    for k,v in remaining.items():
        c=len(v-covered)
        if c>bestc: bestc=c; best=k
    if bestc<=0: break
    greedy.append(best); covered|=kmap[best]; del remaining[best]
print('greedy',len(greedy),'covered',len(covered),flush=True)
# random
rs=[]
for _ in range(60):
    ks=list(allkmers); cov=set(); n=0
    order=pyrand.sample(ks,len(ks))
    for k in order:
        if len(cov)>=200: break
        if allkmers[k]-cov: cov|=allkmers[k]; n+=1
    rs.append(n)
# valid LB: pairwise-disjoint witness set
wit=[]
used=set()
order=sorted(range(200),key=lambda i:len(kmer_sets[i]))
for i in order:
    if not (kmer_sets[i]&used):
        wit.append(i); used|=kmer_sets[i]
LB=len(wit)
res=dict(greedy=len(greedy),random_med=float(np.median(rs)),LB=LB,
         ratio=len(greedy)/LB,ln_bound=(1+np.log(200))*LB)
json.dump(res,open('results/results.json','w'),indent=1)
print(res)
print('G1',len(greedy)<=(1+np.log(200))*LB,'G2',len(greedy)/LB<=2.0,'G3',np.median(rs)>=1.5*len(greedy),'G4',len(covered)==200)
