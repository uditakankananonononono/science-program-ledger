import numpy as np, itertools, json
rng=np.random.default_rng(13)
def emit_probs(delta):
    # state 0 prefers A/T, state 1 prefers G/C; mixture: preferred pair gets 0.25+delta/2 each, other pair 0.25-delta/2
    e=np.full((2,4),0.25-delta/2)
    e[0,0]=e[0,3]=0.25+delta/2  # A,T
    e[1,1]=e[1,2]=0.25+delta/2  # C,G
    return e
def fb(obs,E,T):
    n=len(obs); B=E[:,obs]  # 2 x n
    F=np.zeros((2,n)); Bk=np.zeros((2,n))
    f=np.array([0.5,0.5])*B[:,0]; f/=f.sum(); F[:,0]=f
    for t in range(1,n):
        f=(f@T)*B[:,t]; f/=f.sum(); F[:,t]=f
    b=np.ones(2); b/=b.sum(); Bk[:,-1]=b
    for t in range(n-2,-1,-1):
        b=T@(B[:,t+1]*b); b/=b.sum(); Bk[:,t]=b
    P=F*Bk; P/=P.sum(axis=0,keepdims=True)
    return P
def vit(obs,E,T):
    n=len(obs); lE=np.log(E); lT=np.log(T)
    d=np.log([0.5,0.5])+lE[:,obs[0]]; bp=np.zeros((2,n),int)
    for t in range(1,n):
        c=d[:,None]+lT
        bp[:,t]=c.argmax(axis=0)
        d=c.max(axis=0)+lE[:,obs[t]]
    path=np.zeros(n,int); path[-1]=d.argmax()
    for t in range(n-2,-1,-1): path[t]=bp[path[t+1],t+1]
    return path
# G1: brute-force check
E=emit_probs(0.15); T=np.array([[0.9,0.1],[0.1,0.9]])
ok=True
for _ in range(50):
    obs=rng.integers(0,4,8)
    P=fb(obs,E,T)
    # brute force posterior of state at t=3
    num=np.zeros(2); tot=0.0
    for states in itertools.product((0,1),repeat=8):
        pr=0.5
        for t in range(8):
            pr*=E[states[t],obs[t]]
            if t<7: pr*=T[states[t],states[t+1]]
        num[states[3]]+=pr; tot+=pr
    if abs(num[0]/tot-P[0,3])>1e-8: ok=False
print('G1',ok,flush=True)
res={'G1':ok}
for delta in (0.05,0.15,0.30):
    for stay in (0.90,0.99):
        E=emit_probs(delta); T=np.array([[stay,1-stay],[1-stay,stay]])
        accV=accM=dis=0; N=60
        for _ in range(N):
            states=np.zeros(2000,int); states[0]=rng.integers(0,2)
            for t in range(1,2000):
                states[t]=states[t-1] if rng.random()<stay else 1-states[t-1]
            obs=np.array([rng.choice(4,p=E[s]) for s in states])
            v=vit(obs,E,T); P=fb(obs,E,T); m=P.argmax(axis=0)
            accV+=(v==states).mean(); accM+=(m==states).mean(); dis+=(v!=m).mean()
        res[f'd{delta}_s{stay}']=dict(vit=accV/N,mpm=accM/N,disagree=dis/N)
        print(delta,stay,res[f'd{delta}_s{stay}'],flush=True)
json.dump(res,open('results/results.json','w'),indent=1)
hard=res['d0.05_s0.9']
print('G2',hard['disagree']>=0.005)
acc_all=[(k,v['vit'],v['mpm']) for k,v in res.items() if k!='G1']
print('G3 vit>=mpm-0.005 all:',all(v>=m-0.005 for _,v,m in acc_all),'| mpm>=vit-0.005 all:',all(m>=v-0.005 for _,v,m in acc_all))
print('G4',res['d0.3_s0.9']['vit']>=0.98 and res['d0.3_s0.9']['mpm']>=0.98)
