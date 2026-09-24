import numpy as np, json
rng=np.random.default_rng(73)
def gen(r):
    anchors=[]; n_true=30
    xs=np.sort(rng.uniform(0,2000,n_true))
    shift=int(rng.integers(0,n_true-3))
    for i,x in enumerate(xs):
        sh=(shift<=i<shift+3)
        y=x+rng.normal(0,20)+(300 if sh else 0)
        anchors.append((x,y,float(rng.integers(18,26)),'shift' if sh else True))
    for _ in range(int(n_true*r)):
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
        if all((a[0]>b[0] and a[1]>b[1]) or (a[0]<b[0] and a[1]<b[1]) for b in acc):
            acc.append(a)
    return acc
res={}
for r in (0.0,0.2,0.5,1.0):
    drec=[]; dpre=[]; grec=[]; gpre=[]; shrej=[]
    for _ in range(200):
        anchors=gen(r)
        dc=dp_chain(anchors); gc=greedy_chain(anchors)
        n_true=sum(1 for a in anchors if a[3]==True)
        drec.append(sum(1 for a in dc if a[3]==True)/n_true)
        dpre.append(np.mean([a[3]!=False for a in dc]) if dc else 1)
        grec.append(sum(1 for a in gc if a[3]==True)/n_true)
        gpre.append(np.mean([a[3]==True for a in gc]) if gc else 1)
        shrej.append(sum(1 for a in dc if a[3]=='shift')==0)
    res[str(r)]=dict(dp_rec=float(np.mean(drec)),dp_pre=float(np.mean(dpre)),
                     g_rec=float(np.mean(grec)),g_pre=float(np.mean(gpre)),
                     shift_rejected=float(np.mean(shrej)))
    print(r,res[str(r)],flush=True)
json.dump(res,open('results/pivot_metrics.json','w'),indent=1)
print('P1',all(res[str(r)]['dp_rec']>=0.90 for r in (0.0,0.2,0.5)))
print('P2',all(res[str(r)]['shift_rejected']>=0.80 for r in (0.0,0.2,0.5)))
print('P3',all(res[str(r)]['g_rec']<=res[str(r)]['dp_rec']-0.05 for r in (0.5,1.0)))
