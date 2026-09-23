import json, numpy as np, scipy.sparse as sp
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import matthews_corrcoef
AA='ACDEFGHIKLMNPQRSTVWY'; ST='HEC'; W=8
C=json.load(open('../data/chains.json'))
seqs=[c['seq'] for c in C]; ss=[c['ss3'] for c in C]
K=[set(s[i:i+3] for i in range(len(s)-2)) for s in seqs]
par=list(range(len(C)))
def find(i):
    while par[i]!=i: par[i]=par[par[i]]; i=par[i]
    return i
inv={}
for i,k in enumerate(K):
    for t in k: inv.setdefault(t,[]).append(i)
for i,k in enumerate(K):
    cnt={}
    for t in k:
        for j in inv[t]:
            if j>i: cnt[j]=cnt.get(j,0)+1
    for j,c in cnt.items():
        if c/(len(k)+len(K[j])-c)>=0.3: par[find(i)]=find(j)
g=np.array([find(i) for i in range(len(C))]); ug=np.unique(g)
rng=np.random.default_rng(21); perm=dict(zip(ug,rng.permutation(len(ug)))); gp=np.array([perm[x] for x in g])
def enc(s): return np.array([AA.index(c) for c in s])
E=[enc(s) for s in seqs]; Y=[np.array([ST.index(c) for c in t]) for t in ss]
def onehot(e):
    n=len(e); r=[];cc=[]
    for j in range(-W,W+1):
        idx=np.arange(n)+j; ok=(idx>=0)&(idx<n)
        r.extend(np.where(ok)[0]); cc.extend((j+W)*20+e[idx[ok]])
    return sp.csr_matrix((np.ones(len(r),np.float32),(r,cc)),shape=(n,(2*W+1)*20))
X=[onehot(e) for e in E]
P={'CF':[None]*len(C),'GOR':[None]*len(C),'MLP':[None]*len(C)}
for tr,te in GroupKFold(5).split(np.zeros(len(C)),groups=gp):
    ea=np.concatenate([E[i] for i in tr]); ya=np.concatenate([Y[i] for i in tr])
    ps=np.bincount(ya,minlength=3)/len(ya)
    cnt=np.ones((20,3)); np.add.at(cnt,(ea,ya),1); psa=cnt/cnt.sum(1,keepdims=True); prop=psa/ps
    gor=np.ones((2*W+1,20,3))
    for i in tr:
        e,y=E[i],Y[i]; n=len(e)
        for j in range(-W,W+1):
            idx=np.arange(n)+j; ok=(idx>=0)&(idx<n); np.add.at(gor[j+W],(e[idx[ok]],y[ok]),1)
    lg=np.log(gor/gor.sum(1,keepdims=True))
    mlp=MLPClassifier(hidden_layer_sizes=(64,),early_stopping=True,max_iter=30,random_state=21).fit(sp.vstack([X[i] for i in tr]).tocsr(),ya)
    for i in te:
        e=E[i]; n=len(e)
        pr=prop[e]; k=np.ones(7)/7; sm=np.column_stack([np.convolve(pr[:,s],k,'same') for s in range(3)]); P['CF'][i]=sm.argmax(1)
        sc=np.tile(np.log(ps),(n,1))
        for j in range(-W,W+1):
            idx=np.arange(n)+j; ok=(idx>=0)&(idx<n); sc[ok]+=lg[j+W][e[idx[ok]]]
        P['GOR'][i]=sc.argmax(1); P['MLP'][i]=mlp.predict(X[i])
yall=np.concatenate(Y); res={'n_chains':len(C),'n_res':int(len(yall)),'n_groups':int(len(ug)),'state_freq':(np.bincount(yall)/len(yall)).tolist()}
for k in P:
    pa=np.concatenate(P[k]); res['Q3_'+k]=float((pa==yall).mean())
    for s,nm in ((0,'H'),(1,'E')): res['MCC%s_%s'%(nm,k)]=matthews_corrcoef(yall==s,pa==s)
gi={x:np.where(g==x)[0] for x in ug}; corr={k:[(P[k][i]==Y[i]).sum() for i in range(len(C))] for k in P}; ln=np.array([len(y) for y in Y])
b=[]
for _ in range(2000):
    idx=np.concatenate([gi[x] for x in rng.choice(ug,len(ug))]); L=ln[idx].sum()
    b.append(np.array(corr['MLP'])[idx].sum()/L-np.array(corr['GOR'])[idx].sum()/L)
res['dQ3']=res['Q3_MLP']-res['Q3_GOR']; res['dQ3_ci']=list(np.percentile(b,[2.5,97.5]))
res['gates']={'G1':bool(res['dQ3']>=0.03 and res['dQ3_ci'][0]>0),'G2':bool(res['MCCH_MLP']>res['MCCH_GOR'] and res['MCCE_MLP']>res['MCCE_GOR']),'G3':bool(res['Q3_MLP']>=0.65)}
json.dump(res,open('../results/metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
