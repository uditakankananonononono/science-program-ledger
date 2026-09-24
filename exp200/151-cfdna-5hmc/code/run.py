import gzip,json,numpy as np,pandas as pd
from scipy.stats import rankdata
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV,StratifiedKFold
from sklearn.cluster import KMeans
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
var=np.argsort(-Xtr.var(0))[:2000];Z=(Xtr[:,var]-Xtr[:,var].mean(0))/Xtr[:,var].std(0)
km=KMeans(50,random_state=0,n_init=4).fit(Z.T);mod=km.labels_
feat=lambda X:np.stack([X[:,var][:,mod==k].mean(1) for k in range(50)],1)
M=GridSearchCV(LogisticRegression(max_iter=5000),{'C':[0.01,0.1,1,10]},cv=cv,scoring='roc_auc').fit(feat(Xtr),ytr)
au=[roc_auc_score(ytr,Xtr[:,j]) for j in range(Xtr.shape[1])];au2=np.abs(np.array(au)-.5);j=int(au2.argmax());sg=1 if au[j]>=.5 else -1
B2=GridSearchCV(LogisticRegression(penalty='elasticnet',solver='saga',l1_ratio=0.5,max_iter=1000,tol=1e-3),{'C':[0.01,0.1,1]},cv=cv,scoring='roc_auc').fit(Xtr[:,var],ytr)
pm=M.predict_proba(feat(Xex))[:,1];p1=sg*Xex[:,j];p2=B2.predict_proba(Xex[:,var])[:,1]
ex={k:roc_auc_score(yex,v) for k,v in [('M',pm),('B1',p1),('B2',p2)]};bb='B1' if ex['B1']>=ex['B2'] else 'B2';pb=p1 if bb=='B1' else p2
rng=np.random.default_rng(0);i1=np.where(yex==1)[0];i0=np.where(yex==0)[0];d=[]
for _ in range(2000):
    s=np.concatenate([rng.choice(i1,len(i1)),rng.choice(i0,len(i0))]);d.append(roc_auc_score(yex[s],pm[s])-roc_auc_score(yex[s],pb[s]))
w=M.best_estimator_.coef_[0];top=np.argsort(-np.abs(w))[:5]
mods={int(k):dict(weight=float(w[k]),n=int((mod==k).sum()),genes=[genes[var[i]] for i in np.where(mod==k)[0]][:40]) for k in top}
res=dict(n_train=len(ytr),n_train_cancer=int(ytr.sum()),n_ext=len(yex),n_ext_cancer=int(yex.sum()),n_genes=len(genes),cv_M=M.best_score_,cv_B2=B2.best_score_,B1_gene=genes[j],B1_train_auc=au[j],ext=ex,best_baseline=bb,diff=ex['M']-ex[bb],CI=[float(np.percentile(d,2.5)),float(np.percentile(d,97.5))],top_modules=mods)
res['G1']=bool(ex['M']>=0.80);res['G2']=bool(res['diff']>=0.03 and res['CI'][0]>0)
print(json.dumps({k:v for k,v in res.items() if k!='top_modules'},indent=1));json.dump(res,open('results/main.json','w'),indent=1)
