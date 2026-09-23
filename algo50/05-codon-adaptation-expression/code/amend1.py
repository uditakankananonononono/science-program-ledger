import json,numpy as np
exec(open('code/run.py').read().split("G=DS['Ghaemmaghami']")[0])
G=DS['Ghaemmaghami']; gpos=np.array([g in G for g in ids]); gy=np.array([G.get(g,np.nan) for g in ids])
lw=weights(ref)
def boot(a,b,y,B=2000):
    n=len(y); o=[]
    for _ in range(B):
        i=rng.integers(0,n,n); o.append(spearmanr(a[i],y[i])[0]-spearmanr(b[i],y[i])[0])
    return [float(np.percentile(o,2.5)),float(np.percentile(o,97.5))]
L=np.log10(C.sum(1)*3)[:,None]
AAs=sorted(set(CT.forward_table.values())); A=np.array([[sum(CT.forward_table[c]==a for c in genes[g][1:]) for a in AAs] for g in ids],float); A/=A.sum(1,keepdims=True)
def cai_sub(g):
    v=[lw[ix[c]] for c in genes[g][1:50] if c in ix]; return np.mean(v)
H=(np.array([cai_sub(g) for g in ids])-scCAI)[:,None]
B={'R':rel,'L':L,'A':A,'H':H}
def cvpred(X):
    p=np.zeros(N)
    for tr,te in KFold(5,shuffle=True,random_state=0).split(np.arange(N)):
        t=tr[gpos[tr]]; mu=X[t].mean(0); sd=X[t].std(0)+1e-9
        m=RidgeCV(alphas=np.logspace(-3,3,13)).fit((X[t]-mu)/sd,gy[t]); p[te]=m.predict((X[te]-mu)/sd)
    return p
def full(X):
    mu=X[gpos].mean(0); sd=X[gpos].std(0)+1e-9
    return RidgeCV(alphas=np.logspace(-3,3,13)).fit((X[gpos]-mu)/sd,gy[gpos]).predict((X-mu)/sd)
models={'S2':'RLAH','S2-R':'LAH','S2-L':'RAH','S2-A':'RLH','S2-H':'RLA','R':'R','L':'L','A':'A','H':'H','R+L':'RL'}
P={k:cvpred(np.hstack([B[b] for b in v])) for k,v in models.items()}
S2full=full(np.hstack([B[b] for b in 'RLAH']))
out={}
for dn in ['Ghaemmaghami','Kulak','Mueller']:
    D=DS[dn]; m=np.array([g in D for g in ids]); y=np.array([D[g] for g in ids if g in D])
    r={k:float(spearmanr(v[m],y)[0]) for k,v in P.items()}; r['CAI-RP']=float(spearmanr(caiRP[m],y)[0])
    r['S2_minus_CAIRP_CI']=boot(P['S2'][m],caiRP[m],y)
    if dn!='Ghaemmaghami':
        mm=m&~gpos; yy=np.array([D[g] for g,k in zip(ids,mm) if k])
        r['clean_n']=int(mm.sum()); r['clean_S2']=float(spearmanr(S2full[mm],yy)[0]); r['clean_CAI-RP']=float(spearmanr(caiRP[mm],yy)[0])
    out[dn]=r
json.dump(out,open('results/amend1.json','w'),indent=1); print(json.dumps(out,indent=1))
