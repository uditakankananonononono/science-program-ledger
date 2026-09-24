import json,numpy as np,pandas as pd
from scipy.stats import rankdata
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV,StratifiedKFold
from sklearn.metrics import roc_auc_score
exec(open('code/labels.py').read().split('print(')[0].replace("'GSE89570_sm","'data/GSE89570_sm"))
A=pd.read_csv('data/GSE89570.txt.gz',sep='\t').drop(columns='pos').groupby('gene').sum()
typ={d:(s if st=='cancer' else 'healthy') for d,t,s,st in rows if t=='plasma' and st in('cancer','healthy')}
A=A[[c for c in A.columns if c in typ]];B=pd.read_csv('data/GSE81314.txt.gz',sep='\t',index_col=0)
common=sorted(set(A.index)&set(B.index));A=A.loc[common];A=A[A.median(1)>=10];G=list(A.index)
R=lambda X:np.apply_along_axis(lambda c:rankdata(c)/len(c),0,X.values).T
X=R(A);T=np.array([typ[c] for c in A.columns]);types=['colon','stomach','thyroid','pancreas','liver']
rng=np.random.default_rng(0);h=np.where(T=='healthy')[0];rng.shuffle(h);hte=set(h[:len(h)//5])
def shared(Xtr,Ttr,tt):
    hv=Xtr[Ttr=='healthy'].mean(0);D=np.stack([Xtr[Ttr==t].mean(0)-hv for t in tt])
    med=np.median(D,0);cons=(np.sign(D)==np.sign(med)).sum(0)>=len(tt)-1
    cand=np.where(cons)[0];top=cand[np.argsort(-np.abs(med[cand]))[:200]];return top,np.sign(med[top])
def F(Xs,top,sg): return (Xs[:,top]*sg).mean(1)
res={};cv=StratifiedKFold(3,shuffle=True,random_state=0)
for t in types:
    tr=np.array([(T[i]!=t) and (i not in hte) for i in range(len(T))]);te=np.array([(T[i]==t) or (i in hte) for i in range(len(T))])
    Xtr,Ttr=X[tr],T[tr];ytr=(Ttr!='healthy').astype(int);yte=(T[te]!='healthy').astype(int)
    var=np.argsort(-Xtr.var(0))[:2000];tt=[x for x in types if x!=t]
    top,sg=shared(Xtr[:,var],Ttr,tt);f=F(X[te][:,var],top,sg)
    b1=GridSearchCV(LogisticRegression(penalty='elasticnet',solver='saga',l1_ratio=.5,max_iter=1000,tol=1e-3),{'C':[0.01,0.1,1]},cv=cv,scoring='roc_auc').fit(Xtr[:,var],ytr)
    ga=np.array([roc_auc_score(ytr,Xtr[:,var][:,j]) for j in range(2000)]);gj=int(np.abs(ga-.5).argmax());gs=1 if ga[gj]>=.5 else -1
    res[t]=dict(n_case=int(yte.sum()),n_ctrl=int((1-yte).sum()),F=roc_auc_score(yte,f),B1=roc_auc_score(yte,b1.predict_proba(X[te][:,var])[:,1]),B2=roc_auc_score(yte,gs*X[te][:,var][:,gj]),B2_gene=G[var[gj]])
    print(t,res[t],flush=True)
m={k:float(np.mean([res[t][k] for t in types])) for k in['F','B1','B2']}
bb='B1' if m['B1']>=m['B2'] else 'B2';wins=sum(res[t]['F']>=res[t]['B1'] for t in types)
out=dict(loco=res,mean=m,best=bb,diff=m['F']-m[bb],F_ge_B1=wins,G1=m['F']>=.75,G2=bool(m['F']-m[bb]>=.03 and wins>=4))
var=np.argsort(-X.var(0))[:2000];top,sg=shared(X[:,var],T,types)
Bc=[c for c in B.columns if c.split('_')[0] not in('Blood','Blood-input','Input')];XB=R(B.loc[G,Bc]);yB=np.array([0 if c.split('_')[0] in('Healthy','HBV') else 1 for c in Bc])
out['transfer_GSE81314']=roc_auc_score(yB,F(XB[:,var],top,sg));out['shared_top']=[(G[var[i]],int(s)) for i,s in zip(top[:30],sg[:30])]
print(json.dumps({k:v for k,v in out.items() if k!='loco'},indent=1));json.dump(out,open('results/main.json','w'),indent=1)
