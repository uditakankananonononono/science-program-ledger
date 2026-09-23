import pickle,numpy as np,json,sys
from sklearn.metrics import roc_auc_score
sys.setrecursionlimit(10000)
d=pickle.load(open('../data/prep.pkl','rb')); par,ns,ann,IC=d['par'],d['ns'],d['ann'],d['IC']
anc={}
def A(t):
    if t in anc: return anc[t]
    s={t}
    for p in par.get(t,()): s|=A(p)
    anc[t]=frozenset(s); return anc[t]
O={'BP':'biological_process','MF':'molecular_function','CC':'cellular_component'}
prof={}
def P(g,o):
    k=(g,o)
    if k not in prof:
        ts=[t for t in ann.get(g,()) if ns[t]==O[o]]
        full=set().union(*[A(t) for t in ts]) if ts else set()
        leaves=[t for t in ts if not any(t!=u and t in A(u) for u in ts)]
        prof[k]=(leaves,frozenset(full))
    return prof[k]
mica={}
def M(a,b):
    k=(a,b) if a<b else (b,a)
    if k not in mica:
        c=A(a)&A(b); mica[k]=max((IC.get(t,0) for t in c),default=0.0)
    return mica[k]
def score(g,h,o):
    (la,fa),(lb,fb)=P(g,o),P(h,o)
    if not la or not lb: return 0,0,0,0,fa,fb
    R=np.array([[M(x,y) for y in lb] for x in la])
    ica=np.array([IC.get(x,0) for x in la]); icb=np.array([IC.get(y,0) for y in lb])
    L=2*R/np.maximum(ica[:,None]+icb[None,:],1e-9)
    bma=lambda X:(X.max(1).mean()+X.max(0).mean())/2
    u=sum(IC.get(t,0) for t in fa|fb); gic=sum(IC.get(t,0) for t in fa&fb)/u if u>0 else 0
    return bma(R),R.max(),bma(L),gic,fa,fb
pairs=d['P']+d['N']; y=np.r_[np.ones(len(d['P'])),np.zeros(len(d['N']))]
cols={}
for i,(g,h) in enumerate(pairs):
    FA=set();FB=set()
    for o in O:
        r=score(g,h,o)
        for n,v in zip(['ResBMA','ResMax','LinBMA','simGIC'],r[:4]): cols.setdefault(n+'_'+o,[]).append(v)
        FA|=r[4]; FB|=r[5]
    u=sum(IC.get(t,0) for t in FA|FB); cols.setdefault('simGIC_ALL',[]).append(sum(IC.get(t,0) for t in FA&FB)/u if u>0 else 0)
    if i%2000==0: print(i,len(mica),flush=True)
S={k:np.array(v) for k,v in cols.items()}
import pandas as pd; pd.DataFrame(S).assign(y=y,a=[p[0] for p in pairs],b=[p[1] for p in pairs]).to_csv('../results/pair_scores.tsv.gz',sep='\t',index=False)
res={'n_pos':int(y.sum()),'n_neg':int((1-y).sum()),'auroc':{k:float(roc_auc_score(y,v)) for k,v in S.items()}}
best=max(['ResBMA_BP','ResBMA_MF','ResBMA_CC'],key=lambda k:res['auroc'][k]); res['best_ResBMA']=best
rng=np.random.default_rng(31); ip=np.flatnonzero(y==1); ineg=np.flatnonzero(y==0); B=[]
for r in range(1000):
    ii=np.r_[rng.choice(ip,len(ip)),rng.choice(ineg,len(ineg))]; yy=y[ii]; au=lambda k:roc_auc_score(yy,S[k][ii])
    g=au('simGIC_BP'); B.append([g-au('ResBMA_BP'),au('simGIC_ALL')-au(best),g-au('ResMax_BP')])
B=np.array(B); ci=lambda v:[float(x) for x in np.percentile(v,[2.5,97.5])]; a=res['auroc']
res['d1']=a['simGIC_BP']-a['ResBMA_BP']; res['ci1']=ci(B[:,0])
res['d2']=a['simGIC_ALL']-a[best]; res['ci2']=ci(B[:,1])
res['d3']=a['simGIC_BP']-a['ResMax_BP']; res['ci3']=ci(B[:,2])
res['gates']={'G1':bool(res['d1']>=0.01 and res['ci1'][0]>0),'G2':bool(res['d2']>=0.02 and res['ci2'][0]>0),'G3':bool(res['ci3'][0]>0)}
json.dump(res,open('../results/metrics.json','w'),indent=1); print(json.dumps(res,indent=1))
