import json,sys,gzip,numpy as np
sys.path.insert(0,'code');from geo import load,genes
from scipy.stats import rankdata,hypergeom
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
def labs(meta,g):
    y=[]
    for m in meta:
        s=m.lower()
        if g=='GSE87466': y.append(0 if 'disease: normal' in s else 1)
        elif g=='GSE38713': y.append(0 if 'non-inflammatory control' in s else 1 if ('remission' in s or 'non-involved' in s) else None)
        elif g=='GSE9452': y.append(0 if 'control subject' in s else 1 if 'no macroscopic' in s else None)
        elif g=='GSE59071': y.append(0 if 'control individual' in s else 1 if 'inactive uc' in s else None)
        elif g=='GSE16879': y.append(0 if 'disease: control' in s and 'colon' in s else 1 if ('uc responder after' in s) else None)
    return y
D={}
for g,p in [('GSE87466','GPL13158'),('GSE38713','GPL96'),('GSE9452','GPL96'),('GSE59071','GPL6244'),('GSE16879','GPL570')]:
    df,meta=load(g);y=np.array([np.nan if v is None else v for v in labs(meta,g)]);k=~np.isnan(y)
    D[g]=(genes(df,p).iloc[:,np.where(k)[0]],y[k].astype(int));print(g,D[g][0].shape,int(y[k].sum()),flush=True)
common=sorted(set.intersection(*[set(v[0].index) for v in D.values()]));print('genes',len(common))
R=lambda X:np.apply_along_axis(lambda c:rankdata(c)/len(c),0,X.loc[common].values).T
X={g:R(v[0]) for g,v in D.items()};Y={g:v[1] for g,v in D.items()}
Xt,yt=X['GSE87466'],Y['GSE87466'];var=np.argsort(-Xt.var(0))[:1000]
N=Xt[yt==0][:,var];U=Xt[yt==1][:,var]
pn=(N[:,:,None]>N[:,None,:]).mean(0);pu=(U[:,:,None]>U[:,None,:]).mean(0)
st=np.argwhere(pn>=0.95);print('stable pairs',len(st))
dflip=np.array([(1-pu[i,j])-(1-pn[i,j]) for i,j in st]);top=st[np.argsort(-dflip)[:100]]
PA=[(var[i],var[j]) for i,j in top]
flip=lambda Z:np.mean([Z[:,a]<=Z[:,b] for a,b in PA],0)
exec(open('code/ktsp.py').read())
cv=StratifiedKFold(5,shuffle=True,random_state=0);best=(0,1)
for k in [1,3,5,7,9]:
    au=[]
    for tr,te in cv.split(Xt,yt):
        pp=ktsp_pairs(Xt[tr],yt[tr]);au.append(roc_auc_score(yt[te],ktsp_score(Xt[te],pp,k)))
    if np.mean(au)>best[0]: best=(np.mean(au),k)
KP=ktsp_pairs(Xt,yt);K=best[1];rng=np.random.default_rng(0)
out=dict(n_genes=len(common),n_stable=int(len(st)),ktsp_k=K,train_flip=roc_auc_score(yt,flip(Xt)));E={}
for g in ['GSE38713','GSE9452','GSE59071','GSE16879']:
    Z,y=X[g],Y[g];E[g]=dict(n1=int(y.sum()),n0=int((y==0).sum()),flip=roc_auc_score(y,flip(Z)),ktsp=roc_auc_score(y,ktsp_score(Z,KP,K)+1e-6*rng.random(len(y))))
    print(g,E[g],flush=True)
gt=['GSE38713','GSE9452','GSE59071'];mf=np.mean([E[g]['flip'] for g in gt]);mk=np.mean([E[g]['ktsp'] for g in gt])
G1=bool(all(E[g]['flip']>=0.75 for g in gt) and mf-mk>=0.03);G2=bool(E['GSE59071']['flip']>=0.75 and E['GSE59071']['flip']>=E['GSE59071']['ktsp'])
pg=sorted(set(common[i] for p in PA for i in p));cand=set(common[i] for i in var);enr={}
for s in ['HALLMARK_FATTY_ACID_METABOLISM','HALLMARK_OXIDATIVE_PHOSPHORYLATION','HALLMARK_INFLAMMATORY_RESPONSE']:
    S=set(l.strip() for l in open(f'data/{s}.grp') if l.strip() and not l.startswith(('#','HALLMARK')))&cand;k=len(S&set(pg))
    enr[s]=dict(k=k,genes=sorted(S&set(pg)),p=float(hypergeom.sf(k-1,len(cand),len(S),len(pg))))
G3=bool(min(e['p'] for e in enr.values())<0.01)
pa=[roc_auc_score(yt,(Xt[:,a]<=Xt[:,b]).astype(float)) for a,b in PA];bi=int(np.argmax(pa))
out.update(ext=E,mean_flip=mf,mean_ktsp=mk,G1=G1,G2=G2,enrichment=enr,G3=G3,pair_genes=pg,top_pairs=[(common[a],common[b]) for a,b in PA[:15]],nominated_pair=[common[PA[bi][0]],common[PA[bi][1]]],nom_train_auc=pa[bi])
out['nom_ext']={g:roc_auc_score(Y[g],(X[g][:,PA[bi][0]]<=X[g][:,PA[bi][1]]).astype(float)+1e-6*rng.random(len(Y[g]))) for g in E}
json.dump(out,open('results/results.json','w'),indent=1,default=float);print(json.dumps({k:v for k,v in out.items() if k!='pair_genes'},indent=1,default=float))
