#!/usr/bin/env python3
"""P23-01: Is it quantum or memory? Fair model-zoo comparison on the Kaznatcheev 2019
GameAssay data (github.com/kaznatcheev/GameAssay, Processed/*.npy, 4h reads, 31 sessions).
Models: (1) classical replicator (linear gain), (2) classical + leaky-integrator memory,
(3) Lindblad quantum model with memory drive + dephasing, (4) dephased quantum.
LOO prediction error over wells per environment; bootstrap CIs over wells.
Gates: G1 quantum advantage vs classical within parent-reported 10-20%;
G2 memory-classical gap closure >=70% (memory) / <=30% (quantum); G3 dephased ablation."""
import numpy as np, json, sys
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

D='data'
green=np.load(f'{D}/green_all.npy'); red=np.load(f'{D}/red_all.npy')
T=4*np.arange(green.shape[0]).astype(float)  # hours
# well layout (from DataLoad.py): 14x22, conditions by row pairs, propP grid
import re as _re
_lay=open('tool/layout.py').read()
ns={'np':np}
for _n in ('propP','drugV','fibroV'):
    _m=_re.search(_n+r' = np.array\(\[.*?\]\)\n', _lay, _re.S)
    exec(_n+'='+_m.group(0).split('=',1)[1].strip(), ns)
propP,drugV,fibroV=ns['propP'],ns['drugV'],ns['fibroV']
wells={c:[] for c in range(4)}
for r in range(14):
    for c in range(22):
        p=propP[r][c]
        if np.isnan(p) or p<=0 or p>=1: continue
        g=green[:,r,c]; rd=red[:,r,c]; tot=g+rd
        ok=np.isfinite(tot)&(tot>500)
        if ok.sum()<10: continue
        cond=int(drugV[r][c])*2+int(fibroV[r][c])
        wells[cond].append((T[ok],(g[ok]/tot[ok]).clip(1e-4,1-1e-4)))
for k in wells: wells[k]=wells[k][:16]
print({k:len(v) for k,v in wells.items()},flush=True)

def sim_classical(th,t,x0):
    s,b=th
    def f(t,x): return x*(1-x)*(s*x+b)
    return solve_ivp(f,(t[0],t[-1]),[x0],t_eval=t,rtol=1e-6).y[0]
def sim_memory(th,t,x0):
    s,b,tau=th; tau=max(tau,1.0)
    dt=np.diff(t,prepend=t[0])
    xs=[x0]; m=x0
    for i in range(1,len(t)):
        x=xs[-1]
        k1=x*(1-x)*(s*m+b)
        xn=min(max(x+k1*dt[i],1e-5),1-1e-5)
        m=m+(x-m)*dt[i]/tau
        xs.append(xn)
    return np.array(xs)
def lindblad_traj(th,t,x0,dephase=False):
    k,Delta,gam,tau=th
    if dephase: gam=50.0
    dt=np.diff(t,prepend=t[0])
    # state: rho00, coherence u=Re rho01, v=Im rho01
    x=x0; u=0.0; v=0.0; m=x0
    out=[x]
    for i in range(1,len(t)):
        Om=k*m
        # H = Delta/2 sz + Om sx ; dissipator: dephasing gam on sz + amplitude drive toward game flow
        dx= 2*Om*v
        du= -Delta*v - gam*u/2
        dv= Delta*u + Om*(1-2*x) - gam*v/2
        x=min(max(x+dx*dt[i],1e-5),1-1e-5); u+=du*dt[i]; v+=dv*dt[i]
        m=m+(x-m)*dt[i]/tau
        out.append(x)
    return np.array(out)
def sim_quantum(th,t,x0): return lindblad_traj(th,t,x0,False)
def sim_dephased(th,t,x0): return lindblad_traj(th,t,x0,True)

MODELS={'classical':(sim_classical,np.array([0.0,0.0]),[(-0.05,0.05),(-0.05,0.05)]),
        'memory':(sim_memory,np.array([0.0,0.0,24.0]),[(-0.05,0.05),(-0.05,0.05),(2.0,120.0)]),
        'quantum':(sim_quantum,np.array([0.02,0.005,1.0,24.0]),[(1e-4,0.2),(1e-4,0.1),(1e-3,20.0),(2.0,120.0)]),
        'dephased':(sim_dephased,np.array([0.02,0.005,1.0,24.0]),[(1e-4,0.2),(1e-4,0.1),(1e-3,20.0),(2.0,120.0)])}

def fit(model,train):
    sim,x0th,bounds=MODELS[model]
    def resid(th):
        r=[]
        for t,x in train:
            pred=sim(th,t,x[0])
            r.append(pred-x)
        return np.concatenate(r)
    lo=np.array([b[0] for b in bounds]); hi=np.array([b[1] for b in bounds])
    res=least_squares(resid,np.clip(x0th,lo+1e-9,hi-1e-9),bounds=(lo,hi),max_nfev=40)
    return res.x

out={'n_wells':{str(k):len(v) for k,v in wells.items()},'env_names':{'0':'no drug, no fibro','1':'no drug, fibro','2':'drug, no fibro','3':'drug, fibro'}}
errs={m:{c:[] for c in wells} for m in MODELS}
for cond,ws in wells.items():
    for i in range(len(ws)):
        train=ws[:i]+ws[i+1:]; test=ws[i]
        for m in MODELS:
            th=fit(m,train)
            pred=MODELS[m][0](th,test[0],test[1][0])
            errs[m][cond].append(float(np.mean((pred-test[1])**2)))
    print(f'cond {cond}: '+' '.join(f'{m}={np.mean(errs[m][cond]):.5f}' for m in MODELS),flush=True)

# pooled LOO MSE per model; bootstrap over wells
pool={m:np.array([e for c in errs[m] for e in errs[m][c]]) for m in MODELS}
rng=np.random.RandomState(0); B=2000
def boot(a):
    return np.percentile([rng.choice(a,len(a)).mean() for _ in range(B)],[2.5,97.5]).tolist()
out['loo_mse']={m:{'mean':float(pool[m].mean()),'ci95':boot(pool[m]),'per_well':pool[m].tolist()} for m in MODELS}
qc=pool['classical'].mean(); qq=pool['quantum'].mean(); mq=pool['memory'].mean()
adv=(qc-qq)/qc
gap=(qc-mq)/max(qc-qq,1e-12)
out['G1_quantum_advantage_over_classical']=float(adv)
out['G2_gap_closed_by_memory_classical']=float(gap)
out['G3_dephased_vs_quantum_mse_ratio']=float(pool['dephased'].mean()/qq)
out['gates']={'G1':'PASS' if 0.10<=adv<=0.20 else 'DOCUMENTED-DISCREPANCY',
              'G2':'memory supported (>=0.70)' if gap>=0.70 else ('quantum supported (<=0.30)' if gap<=0.30 else 'mixed'),
              'G3':'reported'}
json.dump(out,open(sys.argv[1],'w'),indent=1)
print(json.dumps({k:v for k,v in out.items() if k!='loo_mse'},indent=1))
