import pickle,numpy as np,json,scipy.sparse as sp
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
d=pickle.load(open('../data/sites.pkl','rb')); M={c:i for i,c in enumerate('ACGT')}
def enc(ws): return np.array([[M[x] for x in w] for w in ws],np.int8)
def get(cs):
    P=[w for c in cs for w in d[c][0] if w[3:5]=='GT']; N=[w for c in cs for w in d[c][1]]
    return enc(P),enc(N)
trP,trN=get(['chr1','chr2','chr3']); teP,teN=get(['chr21','chr22'])
print('train',len(trP),len(trN),'test',len(teP),len(teN),flush=True)
X=np.vstack([teP,teN]); y=np.r_[np.ones(len(teP)),np.zeros(len(teN))]
def pwm(S):
    f=np.ones((9,4))
    for j in range(9): f[j]+=np.bincount(S[:,j],minlength=4)
    return np.log(f/f.sum(1,keepdims=True))
def wam(S):
    f0=np.ones(4)+np.bincount(S[:,0],minlength=4); t=np.ones((8,4,4))
    for j in range(8): np.add.at(t[j],(S[:,j],S[:,j+1]),1)
    return np.log(f0/f0.sum()),np.log(t/t.sum(2,keepdims=True))
pP,pN=pwm(trP),pwm(trN); s0=(pP-pN)[np.arange(9),X].sum(1)
(a,A),(b,B)=wam(trP),wam(trN); j=np.arange(8)
s1=(a-b)[X[:,0]]+(A-B)[j,X[:,:-1],X[:,1:]].sum(1)
pairs=[(i,k) for i in range(9) for k in range(i+1,9)]
def feat(S):
    cols=[S[:,i]*4+0 + 0 for i in range(9)]
    idx=[S[:,i].astype(np.int32)+4*i for i in range(9)]
    off=36
    for q,(i,k) in enumerate(pairs): idx.append(off+16*q+S[:,i].astype(np.int32)*4+S[:,k]); 
    I=np.stack(idx,1); n=len(S)
    return sp.csr_matrix((np.ones(I.size,np.float32),(np.repeat(np.arange(n),I.shape[1]),I.ravel())),shape=(n,36+16*len(pairs)))
del d
key=lambda S:(S.astype(np.int64)*(4**np.arange(8,-1,-1))).sum(1)
uP,cP=np.unique(key(trP),return_counts=True); uN,cN=np.unique(key(trN),return_counts=True)
dec=lambda u:((u[:,None]//(4**np.arange(8,-1,-1)))%4).astype(np.int8)
Xtr=sp.vstack([feat(dec(uP)),feat(dec(uN))]); ytr=np.r_[np.ones(len(uP)),np.zeros(len(uN))]; wtr=np.r_[cP,cN].astype(float)
print('unique train rows',len(uP),len(uN),flush=True)
lr=LogisticRegression(C=1.0,solver='liblinear',max_iter=200).fit(Xtr,ytr,sample_weight=wtr)
uX,inv=np.unique(key(X),return_inverse=True); s2=lr.decision_function(feat(dec(uX)))[inv]
print('fit done',flush=True)
def fpr90(s,y):
    t=np.quantile(s[y==1],0.10); return float((s[y==0]>=t).mean())
S=[s0,s1,s2]; res={'n_train_pos':len(trP),'n_train_neg':len(trN),'n_test_pos':len(teP),'n_test_neg':len(teN)}
for k,s in zip(['PWM','WAM','MAXENT'],S): res['auprc_'+k]=float(average_precision_score(y,s)); res['fpr90_'+k]=fpr90(s,y)
def wap(s,y,w):
    o=np.argsort(-s,kind='stable'); s,y,w=s[o],y[o],w[o]
    tp=np.cumsum(w*y); fp=np.cumsum(w*(1-y)); last=np.r_[s[1:]!=s[:-1],True]
    tp,fp=tp[last],fp[last]; prec=tp/(tp+fp); rec=tp/tp[-1]
    return float(np.sum(np.diff(np.r_[0,rec])*prec))
def wfpr(s,y,w):
    sp_,wp=s[y==1],w[y==1]; o=np.argsort(sp_); c=np.cumsum(wp[o]); t=sp_[o][np.searchsorted(c,0.10*c[-1])]
    return float((w[y==0]*(s[y==0]>=t)).sum()/w[y==0].sum())
rng=np.random.default_rng(29); ip=np.flatnonzero(y==1); ineg=np.flatnonzero(y==0); B=[]
one=np.ones(len(y)); res['check_wap_equals_sklearn']=[wap(s,y,one) for s in S]
for r in range(1000):
    w=np.zeros(len(y)); w[ip]=rng.multinomial(len(ip),np.full(len(ip),1/len(ip))); w[ineg]=rng.multinomial(len(ineg),np.full(len(ineg),1/len(ineg)))
    ap=[wap(s,y,w) for s in S]; fp=[wfpr(s,y,w) for s in S]
    B.append([ap[2]-ap[0],ap[1]-ap[0],fp[0]-fp[2]])
    if r%100==0: print('boot',r,flush=True)
B=np.array(B); ci=lambda v:[float(x) for x in np.percentile(v,[2.5,97.5])]
res['d_auprc_MAXENT_PWM']=res['auprc_MAXENT']-res['auprc_PWM']; res['ci1']=ci(B[:,0])
res['d_auprc_WAM_PWM']=res['auprc_WAM']-res['auprc_PWM']; res['ci2']=ci(B[:,1])
res['d_fpr90_PWM_MAXENT']=res['fpr90_PWM']-res['fpr90_MAXENT']; res['ci3']=ci(B[:,2])
res['gates']={'G1':bool(res['d_auprc_MAXENT_PWM']>=0.03 and res['ci1'][0]>0),'G2':bool(res['ci2'][0]>0),
 'G3':bool(res['fpr90_MAXENT']<=0.8*res['fpr90_PWM'] and res['ci3'][0]>0)}
json.dump(res,open('../results/metrics.json','w'),indent=1); print(json.dumps(res,indent=1))
