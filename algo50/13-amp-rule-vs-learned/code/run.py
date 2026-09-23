import numpy as np, json
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import GroupKFold
AA='ACDEFGHIKLMNPQRSTVWY'
EIS=dict(zip(AA,[0.62,0.29,-0.90,-0.74,1.19,0.48,-0.40,1.38,-1.50,1.06,0.64,-0.78,0.12,-0.85,-2.53,-0.18,-0.05,1.08,0.81,0.26]))
def load(fn,lab,sc):
    out=[]
    for l in list(open(fn))[1:]:
        f=l.rstrip('\n').split('\t'); s=f[sc]
        if set(s)<=set(AA): out.append((f[0],f[1],s,lab))
    return out
D=load('../data/amp.tsv',1,3)+load('../data/nonamp.tsv',0,4)
acc=[d[0] for d in D]; fam=[d[1] for d in D]; seq=[d[2] for d in D]; y=np.array([d[3] for d in D])
def charge(s): return sum(c in 'KR' for c in s)-sum(c in 'DE' for c in s)
def moment(s):
    a=np.deg2rad(100)*np.arange(len(s)); h=np.array([EIS[c] for c in s])
    return float(np.hypot((h*np.cos(a)).sum(),(h*np.sin(a)).sum())/len(s))
def feats(s):
    c=np.array([s.count(a) for a in AA],float)/len(s)
    dp=np.zeros(400)
    for i in range(len(s)-1): dp[AA.index(s[i])*20+AA.index(s[i+1])]+=1
    dp/=max(len(s)-1,1)
    return np.concatenate([c,dp,[len(s),charge(s),moment(s)]])
K=[set(s[i:i+3] for i in range(len(s)-2)) for s in seq]
# union-find groups
par=list(range(len(D)))
def find(i):
    while par[i]!=i: par[i]=par[par[i]]; i=par[i]
    return i
def uni(a,b): par[find(a)]=find(b)
byfam={}
for i,f in enumerate(fam):
    if f: byfam.setdefault(f,[]).append(i)
for v in byfam.values():
    for j in v[1:]: uni(v[0],j)
inv={}
for i,k in enumerate(K):
    for t in k: inv.setdefault(t,[]).append(i)
for i,k in enumerate(K):
    cand=set(j for t in k for j in inv[t] if j>i)
    for j in cand:
        if len(k&K[j])/len(k|K[j])>=0.3: uni(i,j)
g=np.array([find(i) for i in range(len(D))])
rng=np.random.default_rng(13); ug=np.unique(g); perm=dict(zip(ug,rng.permutation(len(ug)))); gp=np.array([perm[x] for x in g])
X=np.array([feats(s) for s in seq])
SR=np.array([charge(s)*moment(s) for s in seq]); SL=np.zeros(len(D)); SN=np.zeros(len(D))
def jac(a,b): return len(a&b)/len(a|b) if a|b else 0
for tr,te in GroupKFold(5).split(X,y,gp):
    m=make_pipeline(StandardScaler(),LogisticRegression(C=1.0,class_weight='balanced',max_iter=5000)).fit(X[tr],y[tr])
    SL[te]=m.decision_function(X[te])
    pa=set(i for i in tr if y[i]==1); na=set(i for i in tr if y[i]==0)
    for i in te:
        cp=set(j for t in K[i] for j in inv[t])
        SN[i]=max([jac(K[i],K[j]) for j in cp if j in pa] or [0])-max([jac(K[i],K[j]) for j in cp if j in na] or [0])
S={'R':SR,'L':SL,'NN':SN}
res={'n':len(D),'n_amp':int(y.sum()),'n_groups':int(len(ug)),'largest_group':int(np.bincount(np.searchsorted(ug,g)).max())}
for k,v in S.items(): res['auroc_'+k]=roc_auc_score(y,v); res['auprc_'+k]=average_precision_score(y,v)
cys=np.array([s.count('C')>=4 for s in seq]); res['n_cys']=int(cys.sum()); res['n_cys_amp']=int(y[cys].sum())
for k,v in S.items(): res['cys_auroc_'+k]=roc_auc_score(y[cys],v[cys])
B={'L-R':[],'L-NN':[]}; gi={x:np.where(g==x)[0] for x in ug}
for _ in range(2000):
    idx=np.concatenate([gi[x] for x in rng.choice(ug,len(ug))])
    if len(set(y[idx]))<2: continue
    aL=roc_auc_score(y[idx],SL[idx]); B['L-R'].append(aL-roc_auc_score(y[idx],SR[idx])); B['L-NN'].append(aL-roc_auc_score(y[idx],SN[idx]))
for k,v in B.items(): res['d_'+k]=res['auroc_L']-res['auroc_'+k.split('-')[1]]; res['ci_'+k]=list(np.percentile(v,[2.5,97.5]))
res['gates']={'G1':bool(res['d_L-R']>=0.05 and res['ci_L-R'][0]>0),'G2':bool(res['d_L-NN']>0 and res['ci_L-NN'][0]>0),'G3':bool(res['cys_auroc_L']>=0.80)}
json.dump(res,open('../results/metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
