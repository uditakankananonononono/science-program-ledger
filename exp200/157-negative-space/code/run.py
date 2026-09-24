import json,sys,numpy as np
sys.path.insert(0,'code');from geo import load,genes
from scipy.stats import rankdata,spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV,StratifiedKFold
from sklearn.metrics import roc_auc_score
def labs(meta,g):
    y=[]
    for m in meta:
        s=m.lower()
        if g=='GSE87466': y.append(0 if 'disease: normal' in s else 1)
        elif g=='GSE38713': y.append(0 if 'non-inflammatory control' in s else 1 if ('remission' in s or 'non-involved' in s) else None)
        else: y.append(0 if 'control subject' in s else 1 if 'no macroscopic' in s else None)
    return y
D={}
for g,p in [('GSE87466','GPL13158'),('GSE38713','GPL96'),('GSE9452','GPL96')]:
    df,meta=load(g);y=np.array([np.nan if v is None else v for v in labs(meta,g)]);k=~np.isnan(y)
    D[g]=(genes(df,p).iloc[:,np.where(k)[0]],y[k].astype(int));print(g,D[g][0].shape,int(y[k].sum()),flush=True)
common=sorted(set.intersection(*[set(v[0].index) for v in D.values()]))
R=lambda X:np.apply_along_axis(lambda c:rankdata(c)/len(c),0,X.loc[common].values).T
X={g:R(v[0]) for g,v in D.items()};Y={g:v[1] for g,v in D.items()}
Xt,yt=X['GSE87466'],Y['GSE87466'];nm=Xt[yt==0]
var=np.argsort(-Xt.var(0))[:1000];r=spearmanr(nm[:,var]).correlation
I,J=np.where(np.triu(np.abs(r)>=0.8,1));print('coupled pairs',len(I),flush=True)
a=var[I];b=var[J]
def fit(Z):
    out=[]
    for x,yv in zip(Z[:,a].T,Z[:,b].T): out.append(np.polyfit(x,yv,1))
    return np.array(out)
co=fit(nm);res_n=nm[:,b]-(co[:,0]*nm[:,a]+co[:,1]);sd=res_n.std(0)+1e-6
brk=lambda Z:np.abs(Z[:,b]-(co[:,0]*Z[:,a]+co[:,1]))/sd
Bt=brk(Xt);pa=np.array([roc_auc_score(yt,Bt[:,k]) for k in range(Bt.shape[1])]);sel=np.argsort(-pa)[:100]
N=lambda Z:brk(Z)[:,sel].mean(1)
rng=np.random.default_rng(0);perm=[]
for _ in range(200):
    yp=rng.permutation(yt);perm.append(np.sort([roc_auc_score(yp,Bt[:,k]) for k in range(0,Bt.shape[1],max(1,Bt.shape[1]//2000))])[-100:].mean())
cv=StratifiedKFold(5,shuffle=True,random_state=0)
def ktsp_pairs(Xa,ya,top=200):
    v=np.argsort(-Xa.var(0))[:top];P1=Xa[ya==1][:,v];P0=Xa[ya==0][:,v]
    s=np.abs((P1[:,:,None]<P1[:,None,:]).mean(0)-(P0[:,:,None]<P0[:,None,:]).mean(0));np.fill_diagonal(s,0)
    iu=np.dstack(np.unravel_index(np.argsort(-s,axis=None),s.shape))[0];out=[];used=set()
    for i,j in iu:
        if i in used or j in used: continue
        out.append((v[i],v[j],1 if (P1[:,i]<P1[:,j]).mean()>(P0[:,i]<P0[:,j]).mean() else -1));used|={i,j}
        if len(out)>=9: break
    return out
def ktsp_score(Z,pairs,k): return np.sum([s*(Z[:,i]<Z[:,j]) for i,j,s in pairs[:k]],0)
best=(0,1)
for k in [1,3,5,7,9]:
    au=[]
    for tr,te in cv.split(Xt,yt):
        pp=ktsp_pairs(Xt[tr],yt[tr]);sc=ktsp_score(Xt[te],pp,k);au.append(roc_auc_score(yt[te],sc) if len(set(yt[te]))>1 else .5)
    if np.mean(au)>best[0]: best=(np.mean(au),k)
KP=ktsp_pairs(Xt,yt);K=best[1]
L1=GridSearchCV(LogisticRegression(penalty='l1',solver='liblinear',max_iter=5000),{'C':[0.03,0.1,0.3,1]},cv=cv,scoring='roc_auc').fit(Xt,yt)
ga=np.array([roc_auc_score(yt,Xt[:,j]) for j in range(Xt.shape[1])]);gj=int(np.abs(ga-.5).argmax());gs=1 if ga[gj]>=.5 else -1
out=dict(n_genes=len(common),n_pairs=int(len(I)),sel_mean_train_auc=float(pa[sel].mean()),perm_null_mean=float(np.mean(perm)),perm_p=float((np.sum(np.array(perm)>=pa[sel].mean())+1)/201),ktsp_k=K,ktsp_cv=best[0],B3_gene=common[gj])
pool={k:[] for k in['N','B1','B2','B3','y']}
for g in ['GSE38713','GSE9452']:
    Z,y=X[g],Y[g];sc=dict(N=N(Z),B1=ktsp_score(Z,KP,K)+1e-6*rng.random(len(y)),B2=L1.predict_proba(Z)[:,1],B3=gs*Z[:,gj])
    out[g]={k:roc_auc_score(y,v) for k,v in sc.items()}
    for k,v in sc.items(): pool[k]+=list(rankdata(v)/len(v))
    pool['y']+=list(y)
P={k:np.array(v) for k,v in pool.items()};y=P['y'];pa2={k:roc_auc_score(y,P[k]) for k in['N','B1','B2','B3']}
bb=max(['B1','B2','B3'],key=lambda k:pa2[k]);i1=np.where(y==1)[0];i0=np.where(y==0)[0];d=[]
for _ in range(2000):
    s=np.concatenate([rng.choice(i1,len(i1)),rng.choice(i0,len(i0))]);d.append(roc_auc_score(y[s],P['N'][s])-roc_auc_score(y[s],P[bb][s]))
out['pooled']=dict(pa2,best=bb,diff=pa2['N']-pa2[bb],CI=[float(np.percentile(d,2.5)),float(np.percentile(d,97.5))])
out['G1']=bool(out['GSE38713']['N']>=.75 and out['GSE9452']['N']>=.75);out['G2']=bool(out['pooled']['diff']>=.03 and out['pooled']['CI'][0]>0)
out['top_pairs']=[(common[a[k]],common[b[k]],float(pa[k])) for k in sel[:15]]
print(json.dumps(out,indent=1));json.dump(out,open('results/main.json','w'),indent=1)
