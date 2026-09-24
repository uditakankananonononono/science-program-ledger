import numpy as np, json
rng=np.random.default_rng(59)
B='ACGT'
seeds={'contig8':[1]*8,'spaced8':[1,1,0,1,0,0,1,1,0,1,1,0,1,0,1,1,0,1,1],  # 10 ones of 19? count below
       'contig12':[1]*12}
seeds['spaced8']=[1,1,0,1,1,0,1,1]  # weight 6? fix: explicit weight-8 spaced, span 11
seeds['spaced8']=[1,1,0,1,0,1,1,0,1,1,1]
w8=sum(seeds['spaced8'])
assert w8==8, w8
def hit(a,b,pat):
    L=len(pat); care=[i for i,x in enumerate(pat) if x]
    for i in range(len(a)-L+1):
        if all(a[i+j]==b[i+j] for j in care): return True
    return False
res={}
for q in (0.60,0.65,0.70,0.75):
    row={}
    for name,pat in seeds.items():
        h=0; N=1000
        for _ in range(N):
            a=''.join(rng.choice(list(B),60))
            b=''.join(c if rng.random()<q else rng.choice([x for x in B if x!=c]) for c in a)
            h+=hit(a,b,pat)
        row[name]=h/N
    res[str(q)]=row
    print(q,row,flush=True)
# background
bg={}
for name,pat in seeds.items():
    h=0; N=400
    for _ in range(N):
        a=''.join(rng.choice(list(B),60)); b=''.join(rng.choice(list(B),200))
        h+=hit(a,b,pat)
    bg[name]=h/N
res['bg']=bg
print('bg',bg,'weights',{k:sum(v) for k,v in seeds.items()},flush=True)
json.dump(res,open('results/pivot_metrics.json','w'),indent=1)
P1=res['0.7']['spaced8']>=res['0.7']['contig8']+0.05
P2=res['0.7']['contig12']<=res['0.7']['spaced8']-0.15
th={n:1-(1-4**(-sum(p)))**(60-len(p)+1) for n,p in seeds.items()}
P3=all(1/3<=bg[n]/th[n]<=3 for n in ('contig8','spaced8'))
P4=all(all(res[str(a)][n]<=res[str(b)][n]+1e-9 for a,b in zip((0.6,0.65,0.7),(0.65,0.7,0.75))) for n in seeds)
print('P1',P1,'P2',P2,'P3',P3,th,'P4',P4)
