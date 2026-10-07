import numpy as np, json, wfdb, warnings
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
warnings.filterwarnings('ignore')
DS1='101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230'.split(',')
DS2='100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234'.split(',')
MAP={}
for s in 'NLRej': MAP[s]=0
for s in 'AaJS': MAP[s]=1
for s in 'VE': MAP[s]=2
MAP['F']=3
def feats(r):
    rec=wfdb.rdrecord(f'data/{r}',channels=[0]); ann=wfdb.rdann(f'data/{r}','atr'); x=rec.p_signal[:,0]
    idx=[(s,MAP[c]) for s,c in zip(ann.sample,ann.symbol) if c in MAP]
    S=np.array([i[0] for i in idx]); Y=np.array([i[1] for i in idx]); X=[];keep=[]
    for k,s in enumerate(S):
        if s-90<0 or s+144>len(x) or k<11 or k>=len(S)-1: continue
        w=x[s-90:s+144]; w=np.interp(np.linspace(0,233,90),np.arange(234),w); w=(w-w.mean())/(w.std()+1e-9)
        rr=[S[k]-S[k-1],S[k+1]-S[k],np.mean(np.diff(S[k-10:k+1]))]
        X.append(np.concatenate([w,rr])); keep.append(k)
    return np.array(X),Y[keep]
def build(recs):
    X=[];Y=[];G=[]
    for r in recs:
        a,b=feats(r); X.append(a);Y.append(b);G+= [r]*len(b)
    return np.vstack(X),np.concatenate(Y),np.array(G)
def f1s(y,p): return f1_score(y,p,labels=[1,2,3],average='macro')
rng=np.random.RandomState(0); folds=[]
Xtr,ytr,gtr=build(DS1); Xte,yte,gte=build(DS2)
print('DS1',Xtr.shape,np.bincount(ytr),'DS2',Xte.shape,np.bincount(yte),flush=True)
ug=np.array(DS1); rng.shuffle(ug); fold_of={g:i%5 for i,g in enumerate(ug)}; fid=np.array([fold_of[g] for g in gtr])
def cvscore(fit_pred):
    p=np.zeros(len(ytr),int)
    for f in range(5):
        tr=fid!=f; te=fid==f; p[te]=fit_pred(Xtr[tr],ytr[tr],Xtr[te])
    return f1s(ytr,p),p
def knn(k): 
    def fp(a,b,c):
        sc=StandardScaler().fit(a); return KNeighborsClassifier(k).fit(sc.transform(a),b).predict(sc.transform(c))
    return fp
def lr(C):
    def fp(a,b,c):
        sc=StandardScaler().fit(a); return LogisticRegression(C=C,class_weight='balanced',max_iter=300).fit(sc.transform(a),b).predict(sc.transform(c))
    return fp
cands={('knn',k):knn(k) for k in (5,15,45)}; cands.update({('lr',C):lr(C) for C in (.1,1,10)})
cv={n:cvscore(f)[0] for n,f in cands.items()}; print('baseline CV',cv,flush=True)
bB=max(cv,key=cv.get)
def pbc_scores(a,b,c,m):
    sc=StandardScaler().fit(a); A=sc.transform(a); C=sc.transform(c); pca=PCA(20,random_state=0).fit(A); A=pca.transform(A); C=pca.transform(C)
    S=[]
    for k in range(4):
        P=A[b==k]; mm=min(m,len(P)); cen=KMeans(mm,random_state=0,n_init=5).fit(P).cluster_centers_
        S.append(-np.sqrt(((C[:,None,:]-cen[None])**2).sum(2)).min(1))
    return np.column_stack(S)
best=None
grid=np.arange(-1,1.01,.25)
for m in (4,8,16):
    # out-of-fold scores
    O=np.zeros((len(ytr),4))
    for f in range(5):
        tr=fid!=f; te=fid==f; O[te]=pbc_scores(Xtr[tr],ytr[tr],Xtr[te],m)
    b=np.zeros(4)
    for it in range(2):
        for c in (1,2,3):
            bs=[(f1s(ytr,np.argmax(O+np.where(np.arange(4)==c,v,b),1)),-abs(v),v) for v in grid]
            b[c]=max(bs)[2]
    s=f1s(ytr,np.argmax(O+b,1)); print('pbc',m,round(s,4),b,flush=True)
    if best is None or s>best[0]: best=(s,m,b.copy())
s,m,b=best
pB=cands[bB](Xtr,ytr,Xte); pP=np.argmax(pbc_scores(Xtr,ytr,Xte,m)+b,1)
recs=sorted(set(gte)); rs=np.random.RandomState(7); ds=[]
for _ in range(10000):
    rr=rs.choice(recs,len(recs)); idx=np.concatenate([np.where(gte==r)[0] for r in rr]); ds.append(f1s(yte[idx],pP[idx])-f1s(yte[idx],pB[idx]))
lo,hi=np.percentile(ds,[2.5,97.5]); d=f1s(yte,pP)-f1s(yte,pB)
v='WIN' if d>=.02 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
pc=lambda p:[float(x) for x in f1_score(yte,p,labels=[0,1,2,3],average=None)]
out=dict(baseline=list(map(str,bB)),cv_baseline={str(k):v for k,v in cv.items()},pbc_m=m,pbc_cv=s,pbc_bias=list(b),f1_baseline=f1s(yte,pB),f1_pbc=f1s(yte,pP),diff=d,ci=[lo,hi],verdict=v,perclass_baseline=pc(pB),perclass_pbc=pc(pP))
json.dump(out,open('results.json','w'),indent=1); print(json.dumps(out))
