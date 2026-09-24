import random, json
rng=random.Random(1)
def edit(a,b,k=None):
    n,m=len(a),len(b); INF=float('inf')
    prev=list(range(m+1))
    for i in range(1,n+1):
        lo=1 if k is None else max(1,i-k); hi=m if k is None else min(m,i+k)
        cur=[INF]*(m+1)
        if k is None or i-k<=0: cur[0]=i
        ai=a[i-1]
        for j in range(lo,hi+1):
            cur[j]=min(prev[j]+1,cur[j-1]+1,prev[j-1]+(ai!=b[j-1]))
        prev=cur
    return prev[m]
def band_P(a,b,k=8):
    while True:
        d=edit(a,b,k)
        if k>=d or k>=max(len(a),len(b)): return d,k
        k*=2
def mut(a,d):
    b=list(a)
    for _ in range(int(len(a)*d)):
        op=rng.random(); p=rng.randrange(len(b))
        if op<0.7: b[p]=rng.choice('ACGT')
        elif op<0.85 and len(b)>10: del b[p]
        else: b.insert(p,rng.choice('ACGT'))
    return ''.join(b)
tot=ok=0; ratios=[]
cases=[]
for d in (0.05,0.1,0.2,0.3):
    for _ in range(60):
        a=''.join(rng.choice('ACGT') for _ in range(400)); cases.append((a,mut(a,d)))
for _ in range(60):
    cases.append((''.join(rng.choice('ACGT') for _ in range(400)),''.join(rng.choice('ACGT') for _ in range(400))))
for a,b in cases:
    df=edit(a,b); dp,k=band_P(a,b)
    tot+=1; ok+=dp==df; ratios.append(k/max(df,1))
json.dump(dict(match=ok/tot,n=tot,median_k_over_d=sorted(ratios)[len(ratios)//2]),open('results/pivot_metrics.json','w'))
print('match',ok,'/',tot,'median k/d',sorted(ratios)[len(ratios)//2])
