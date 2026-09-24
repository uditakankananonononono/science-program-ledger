import gzip,json,numpy as np,pandas as pd
from scipy.stats import rankdata
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV,StratifiedKFold
from sklearn.metrics import roc_auc_score
exec(open('code/labels.py').read().split('print(')[0].replace("'GSE89570_sm","'data/GSE89570_sm"))
A=pd.read_csv('data/GSE89570.txt.gz',sep='\t').drop(columns='pos').groupby('gene').sum()
lab={}
for d,t,s,st in rows:
    if t=='plasma' and st in('cancer','healthy'): lab[d]=1 if st=='cancer' else 0
A=A[[c for c in A.columns if c in lab]];ytr=np.array([lab[c] for c in A.columns])
B=pd.read_csv('data/GSE81314.txt.gz',sep='\t',index_col=0);grp=[c.split('_')[0] for c in B.columns]
keep=[c for c,g in zip(B.columns,grp) if g not in('Blood','Blood-input','Input')]
B=B[keep];yex=np.array([0 if c.split('_')[0] in('Healthy','HBV') else 1 for c in keep])
print('train',A.shape,ytr.sum(),'ext',B.shape,yex.sum(),flush=True)
common=sorted(set(A.index)&set(B.index));A=A.loc[common];A=A[A.median(1)>=10];genes=list(A.index);B=B.loc[genes]
R=lambda X:np.apply_along_axis(lambda c:rankdata(c)/len(c),0,X.values).T
Xtr,Xex=R(A),R(B);print('genes',len(genes),flush=True)
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
import glob
def kp(Xa,ya):
    v=np.argsort(-Xa.var(0))[:2000];return ktsp_pairs(Xa[:,v],ya,top=2000),v
def ks(Z,P,v,k): return ktsp_score(Z[:,v],P,k)
best=(0,1)
for k in [1,3,5,7,9]:
    au=[]
    for tr,te in cv.split(Xtr,ytr):
        P,v=kp(Xtr[tr],ytr[tr]);au.append(roc_auc_score(ytr[te],ks(Xtr[te],P,v,k)))
    if np.mean(au)>best[0]: best=(float(np.mean(au)),k)
K=best[1];P,v=kp(Xtr,ytr);rng=np.random.default_rng(0)
pk=ks(Xex,P,v,K)+1e-6*rng.random(len(yex))
au=[roc_auc_score(ytr,Xtr[:,j]) for j in range(Xtr.shape[1])];j=int(np.abs(np.array(au)-.5).argmax());sg=1 if au[j]>=.5 else -1;p1=sg*Xex[:,j]
ex=dict(ktsp=roc_auc_score(yex,pk),one_gene=roc_auc_score(yex,p1),one_gene_name=genes[j])
i1=np.where(yex==1)[0];i0=np.where(yex==0)[0];d=[]
for _ in range(2000):
    s=np.r_[rng.choice(i1,len(i1)),rng.choice(i0,len(i0))];d.append(roc_auc_score(yex[s],pk[s])-roc_auc_score(yex[s],p1[s]))
ci=[float(np.percentile(d,2.5)),float(np.percentile(d,97.5))]
# secondary: label-free anchor alignment + elastic-net
var=np.argsort(-Xtr.var(0))[:2000];Ac=Xtr-np.median(Xtr,0);Bc=Xex-np.median(Xex,0)
EN=GridSearchCV(LogisticRegression(penalty='elasticnet',solver='saga',l1_ratio=0.5,max_iter=1000,tol=1e-3),{'C':[0.01,0.1,1]},cv=cv,scoring='roc_auc').fit(Ac[:,var],ytr)
ex['anchor_EN']=roc_auc_score(yex,EN.predict_proba(Bc[:,var])[:,1])
pg=sorted(set(genes[v[a]] for a,b,s in P[:K])|set(genes[v[b]] for a,b,s in P[:K]))
top30=set(g for g,_ in json.load(open(glob.glob('../../ledger/exp200/158-*/results/main.json')[0]))['shared_top'])&set(genes)
from scipy.stats import hypergeom
ov=sorted(set(pg)&top30);p3=float(hypergeom.sf(len(ov)-1,len(genes),len(top30),len(pg)))
G1=bool(ex['ktsp']>=0.80 and ex['ktsp']>=0.76 and ci[0]>-0.05);G2=bool(best[0]>=0.75);G3=bool(p3<0.05)
pairs=[(genes[v[a]],genes[v[b]],int(s)) for a,b,s in P[:K]]
out=dict(K=K,cv_ktsp=best[0],ext=ex,ci_diff=ci,pairs=pairs,overlap158=ov,p_overlap=p3,G1=G1,G2=G2,G3=G3)
json.dump(out,open('results/results.json','w'),indent=1,default=float);print(json.dumps(out,indent=1,default=float))
