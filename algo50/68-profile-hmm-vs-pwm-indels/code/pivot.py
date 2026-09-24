import numpy as np, json
rng=np.random.default_rng(41)
B='ACGT'
pref=rng.choice(list(B),18)
def instance(indel_r):
    out=[]
    for c in pref:
        b=c if rng.random()<0.7 else rng.choice([x for x in B if x!=c])
        if rng.random()<indel_r:
            if rng.random()<0.5: continue  # deletion
            out.append(rng.choice(list(B))); out.append(b)  # insertion before
        else: out.append(b)
    return ''.join(out)
train=[instance(0.0) for _ in range(60)]
counts=np.ones((18,4))*0.01
for s in train:
    for i,c in enumerate(s): counts[i,B.index(c)]+=1
pwm=np.log2(counts/counts.sum(axis=1,keepdims=True)/0.25)
def pwm_score(seq):
    best=-1e9
    for i in range(len(seq)-17):
        w=seq[i:i+18]
        s=sum(pwm[j,B.index(w[j])] for j in range(18))
        if s>best: best=s
    return best
# profile HMM viterbi (log2), states: M1..M12, I1..I12, D1..D12
eM=np.log2(counts/counts.sum(axis=1,keepdims=True))
eI=np.log2(np.full(4,0.25))
lTM=np.log2([[0.95,0.025,0.025],[0.9,0.1,0.0],[0.95,0.0,0.05]])  # rows from M,I,D to M,I,D
def hmm_score(seq):
    n=len(seq); L=18
    M=np.full((L+1,n+1),-np.inf); I=np.full((L+1,n+1),-np.inf); D=np.full((L+1,n+1),-np.inf)
    M[0,:]=0.0  # free start anywhere (local alignment mode)
    # begin -> M1/I1/D1 handled by initializing column scan
    best=-np.inf
    idx={c:k for k,c in enumerate(B)}
    for j in range(1,n+1):
        b=idx[seq[j-1]]
        for i in range(0,L+1):
            # insert state
            if i>=1:
                cand=[I[i,j-1]+lTM[1,1],M[i,j-1]+lTM[0,1]]
                I[i,j]=max(cand)+eI[b]
        for i in range(1,L+1):
            src=[]
            if i==1:
                src=[(M[0,j-1],0.0),(D[0,j-1] if D[0,j-1]>-np.inf else -np.inf,0.0)]
                M[i,j]=max(M[0,j-1],D[0,j-1] if j>0 else -np.inf)+eM[i-1,b]
            else:
                M[i,j]=max(M[i-1,j-1]+lTM[0,0],I[i-1,j-1]+lTM[1,0],D[i-1,j-1]+lTM[2,0])+eM[i-1,b]
            if i<=L:
                D[i,j]=max(M[i-1,j]+lTM[0,2],D[i-1,j]+lTM[2,2]) if i>1 else M[0,j]+lTM[0,2]
        best=max(best,M[L,j],I[L,j] if L>=1 else -np.inf)
    # null: iid log2 0.25 per base over best 12-window is implicit in odds; use raw score vs length-normalized null
    null=18*np.log2(0.25)
    return best-null
def auroc(pos,neg):
    pos=np.sort(np.array(pos)); neg=np.array(neg)
    return float(np.mean(np.searchsorted(pos,neg,side='left')/len(pos)*0 + (neg[:,None]<pos[None,:]).mean(axis=1)+0.5*(neg[:,None]==pos[None,:]).mean(axis=1)))
res={}
for r in (0.0,0.02,0.05,0.10):
    ps=[]; ns=[]; ph=[]; nh=[]
    for _ in range(150):
        bg=''.join(rng.choice(list(B),200))
        inst=instance(r)
        p=int(rng.integers(0,200-len(inst)))
        s=bg[:p]+inst+bg[p:]
        ps.append(pwm_score(s)); ph.append(hmm_score(s))
        bg2=''.join(rng.choice(list(B),200))
        ns.append(pwm_score(bg2)); nh.append(hmm_score(bg2))
    res[str(r)]=dict(pwm=auroc(ps,ns),hmm=auroc(ph,nh))
    print(r,res[str(r)],flush=True)
json.dump(res,open('results/pivot_metrics.json','w'),indent=1)
print('P1',res['0.0']['pwm']>=0.95 and abs(res['0.0']['pwm']-res['0.0']['hmm'])<=0.03)
gaps=[res[str(r)]['hmm']-res[str(r)]['pwm'] for r in (0.0,0.02,0.05,0.1)]
print('P2',all(b>=a-1e-9 for a,b in zip(gaps,gaps[1:])),gaps)
print('P3',res['0.1']['hmm']>=0.95 and res['0.1']['pwm']<=0.95)
