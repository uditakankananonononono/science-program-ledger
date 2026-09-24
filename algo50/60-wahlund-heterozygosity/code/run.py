import numpy as np, json
from scipy.stats import rankdata
rng=np.random.default_rng(17)
res={}
for w in (0.5,0.3):
    for d in (0.1,0.3,0.5,0.7):
        fis_s=[]; fis_t=[]; ratio=[]
        for _ in range(1000):
            pA=rng.uniform(0.15,0.25); pB=pA+d
            nA=int(500*w); nB=500-nA
            gA=(rng.random((nA,2))<pA).sum(axis=1)
            gB=(rng.random((nB,2))<pB).sum(axis=1)
            g=np.concatenate([gA,gB])
            Ho=(g==1).mean()
            pq=(gA.sum()+gB.sum())/(2*500)
            He=2*pq*(1-pq)
            fis=1-Ho/He
            ft=w*(1-w)*d*d/(pq*(1-pq))
            fis_s.append(fis); fis_t.append(ft); ratio.append(Ho/He)
        res[f'w{w}_d{d}']=dict(fis_sim=float(np.mean(fis_s)),fis_theory=float(np.mean(fis_t)),ratio=float(np.mean(ratio)))
        print(w,d,res[f'w{w}_d{d}'],flush=True)
# control: single population, no structure
fis_c=[]
for _ in range(1000):
    p=rng.uniform(0.35,0.45)
    g=(rng.random((500,2))<p).sum(axis=1)
    Ho=(g==1).mean(); He=2*p*(1-p)
    fis_c.append(1-Ho/He)
ctrl=float(np.mean(fis_c))
res['control']=ctrl
print('control F_IS',ctrl,flush=True)
json.dump(res,open('results/results.json','w'),indent=1)
cells=[k for k in res if k.startswith('w')]
G1=all(abs(res[k]['fis_sim']-res[k]['fis_theory'])<=0.02 for k in cells)
ds=[0.1,0.3,0.5,0.7]
G2=(rankdata([res[f'w0.5_d{d}']['fis_sim'] for d in ds])==[1,2,3,4]).all()
G3=res['w0.5_d0.5']['ratio']<=0.75
G4=abs(ctrl)<=0.02
print('G1',G1,'G2',bool(G2),'G3',G3,'G4',G4)
