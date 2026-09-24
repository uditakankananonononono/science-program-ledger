import numpy as np, json
rng=np.random.default_rng(71)
def gen(r):
    anchors=[]; n_true=30
    xs=np.sort(rng.uniform(0,2000,n_true))
    shift=int(rng.integers(0,n_true-3))
    for i,x in enumerate(xs):
        y=x+rng.normal(0,20)+(300 if i>=shift and i<shift+3 else 0)
        anchors.append((x,y,float(rng.integers(18,26)),True))
    n_sp=int(n_true*r)
    for _ in range(n_sp):
        anchors.append((rng.uniform(0,2000),rng.uniform(0,2000),float(rng.integers(15,26)),False))
    return anchors
def dp_chain(anchors):
    A=sorted(anchors)
    n=len(A); dp=[a[2] for a in A]; back=[-1]*n
    for i in range(n):
        for j in range(i):
            dx=A[i][0]-A[j][0]; dy=A[i][1]-A[j][1]
            if dx>0 and dy>0:
                pen=0.02*max(0,abs(dx-dy)-50)
                v=dp[j]-pen+A[i][2]
                if v>dp[i]: dp[i]=v; back[i]=j
    i=int(np.argmax(dp)); chain=[]
    while i>=0: chain.append(A[i]); i=back[i]
    return chain
def greedy_chain(anchors):
    A=sorted(anchors,key=lambda a:-a[2])
    acc=[]
    for a in A:
        if all((a[0]-b[0])*(a[1]-b[1])>0 or (a[0]==b[0] and a[1]==b[1]) for b in acc) or not acc:
            # colinear vs all accepted: must be strictly increasing relative to each
            if all((a[0]>b[0] and a[1]>b[1]) or (a[0]<b[0] and a[1]<b[1]) for b in acc):
                acc.append(a)
    return acc
res={}
for r in (0.0,0.2,0.5,1.0):
    drec=[]; dpre=[]; grec=[]; gpre=[]
    for _ in range(200):
        anchors=gen(r)
        dc=dp_chain(anchors); gc=greedy_chain(anchors)
        drec.append(np.mean([a[3] for a in dc]) if dc else 0)
        n_true=sum(1 for a in anchors if a[3])
        drec[-1]=sum(1 for a in dc if a[3])/n_true
        dpre.append(np.mean([a[3] for a in dc]) if dc else 1)
        grec.append(sum(1 for a in gc if a[3])/n_true)
        gpre.append(np.mean([a[3] for a in gc]) if gc else 1)
    res[str(r)]=dict(dp_rec=float(np.mean(drec)),dp_pre=float(np.mean(dpre)),g_rec=float(np.mean(grec)),g_pre=float(np.mean(gpre)))
    print(r,res[str(r)],flush=True)
json.dump(res,open('results/results.json','w'),indent=1)
print('G1',all(res[str(r)]['dp_rec']>=0.90 for r in (0.0,0.2,0.5)))
print('G2',all(res[str(r)]['dp_pre']>=0.95 for r in (0.0,0.2,0.5)))
print('G3',any(res[str(r)]['g_rec']<=res[str(r)]['dp_rec']-0.05 for r in (0.5,1.0)))
print('G4',res['1.0']['dp_rec']>=0.75)
