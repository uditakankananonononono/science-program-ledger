import numpy as np, json
rng=np.random.default_rng(5)
L=20000
ref=rng.integers(0,4,L)
res={}
for cov in (3,5,8,15,30):
    Q=rng.choice([10,20,30,40],size=(cov,L))
    e=10.0**(-Q/10.0)
    err=rng.random((cov,L))<e
    wrong_base=(ref[None,:]+rng.integers(1,4,(cov,L)))%4
    obs=np.where(err,wrong_base,ref[None,:])
    # majority
    maj=np.array([np.bincount(obs[:,i],minlength=4).argmax() for i in range(L)])
    # quality-weighted log-likelihood
    ll=np.zeros((4,L))
    li=np.log(1-e); le=np.log(e/3)
    for b in range(4):
        m=obs==b
        ll[b]=np.where(m,li,le).sum(axis=0)
    qw=ll.argmax(axis=0)
    em=(maj!=ref).mean(); eq=(qw!=ref).mean()
    res[cov]=dict(maj=float(em),qw=float(eq),ratio=float(eq/em) if em>0 else 0.0)
    print(cov,res[cov],flush=True)
json.dump(res,open('results/results.json','w'),indent=1)
r=res
print('G1',all(r[c]['qw']<=r[c]['maj'] for c in r))
print('G2',r[3]['ratio']<=0.60,r[3])
print('G3',r[30]['maj']<1e-4 and r[30]['qw']<1e-4)
print('G4',r[8]['qw']<=r[15]['maj'])
