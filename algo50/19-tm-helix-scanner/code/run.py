import json, numpy as np, scipy.sparse as sp
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
AA='ACDEFGHIKLMNPQRSTVWY'; W=21; H=W//2
KD=dict(zip(AA,[1.8,2.5,-3.5,-3.5,2.8,-0.4,-3.2,4.5,-3.9,3.8,1.9,-3.5,-1.6,-3.5,-4.5,-0.8,-0.7,4.2,-0.9,-1.3]))
pos=json.load(open('../data/pos.json')); neg=json.load(open('../data/neg.json'))
P=[dict(p,y=1) for p in pos]+[dict(n,segs=[],y=0) for n in neg]
def lab(p):
    y=np.zeros(len(p['seq']),int)
    for a,b in p['segs']: y[a:b]=1
    return y
def kdwin(s,w=19):
    h=np.array([KD[c] for c in s]); k=np.ones(w)/w
    return np.convolve(h,k,'same')
def feats(s):
    pad='X'*H+s+'X'*H; n=len(s); rows=[];cols=[]
    for i in range(n):
        for j,c in enumerate(pad[i:i+W]):
            if c!='X': rows.append(i); cols.append(j*20+AA.index(c))
    oh=sp.csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(n,W*20))
    kw=kdwin(s,W); win=lambda S: np.convolve(np.array([c in S for c in s],float),np.ones(W),'same')
    ex=np.column_stack([kw,win('DEKR'),win('FWY'),win('P')])
    return sp.hstack([oh,sp.csr_matrix(ex)]).tocsr()
def segs(mask,minlen=5):
    out=[];i=0;n=len(mask)
    while i<n:
        if mask[i]:
            j=i
            while j<n and mask[j]: j+=1
            if j-i>=minlen: out.append((i,j))
            i=j
        else: i+=1
    return out
ov=lambda a,b,c,d: min(b,d)-max(a,c)>=5
def counts(pred,true):
    return [sum(any(ov(a,b,c,d) for c,d in pred) for a,b in true),len(true),sum(any(ov(a,b,c,d) for a,b in true) for c,d in pred),len(pred),int(len(pred)==len(true))]
def f1(C):
    C=np.sum(C,0); r=C[0]/C[1] if C[1] else 0; p=C[2]/C[3] if C[3] else 0; return 2*p*r/(p+r) if p+r else 0.0
Y=[lab(p) for p in P]; X=[feats(p['seq']) for p in P]; K=[kdwin(p['seq']) for p in P]
isp=np.array([p['y'] for p in P]); groups=[p['fam'] for p in P]
rng=np.random.default_rng(19); order=rng.permutation(len(P))
S1=[None]*len(P); thr1=[None]*len(P); thrK=[None]*len(P); T1=[]; TK=[]
def best(scores,idx,qs):
    return max(qs,key=lambda t:f1([counts(segs(scores[i]>=t),P[i]['segs']) for i in idx]))
for tr,te in GroupKFold(5).split(order,groups=[groups[i] for i in order]):
    tr=order[tr]; te=order[te]
    clf=LogisticRegression(C=1.0,class_weight='balanced',max_iter=3000).fit(sp.vstack([X[i] for i in tr]).tocsr(),np.concatenate([Y[i] for i in tr]))
    sc={i:clf.decision_function(X[i]) for i in np.concatenate([tr,te])}
    trp=[i for i in tr if isp[i]]
    t1=best(sc,trp,np.linspace(-2,4,31)); tk=best({i:K[i] for i in trp},trp,np.linspace(0.6,2.4,19))
    T1.append(float(t1)); TK.append(float(tk))
    for i in te: S1[i]=sc[i]; thr1[i]=t1; thrK[i]=tk
pi=[i for i in range(len(P)) if isp[i]]; ni=[i for i in range(len(P)) if not isp[i]]
CK=[counts(segs(K[i]>=1.6),P[i]['segs']) for i in pi]
C1=[counts(segs(S1[i]>=thr1[i]),P[i]['segs']) for i in pi]
CKt=[counts(segs(K[i]>=thrK[i]),P[i]['segs']) for i in pi]
res={'n_pos':len(pi),'n_neg':len(ni),'n_helices':int(sum(len(P[i]['segs']) for i in pi)),'thr_M1_folds':T1,'thr_KDtuned_folds':TK}
for k,C in (('KD',CK),('M1',C1),('KDtuned',CKt)):
    s=np.sum(C,0); res['segF1_'+k]=f1(C); res['recall_'+k]=s[0]/s[1]; res['precision_'+k]=s[2]/max(s[3],1); res['countacc_'+k]=s[4]/len(C)
res['fp_soluble_KD']=float(np.mean([len(segs(K[i]>=1.6))>0 for i in ni]))
res['fp_soluble_M1']=float(np.mean([len(segs(S1[i]>=thr1[i]))>0 for i in ni]))
res['fp_soluble_KDtuned']=float(np.mean([len(segs(K[i]>=thrK[i]))>0 for i in ni]))
bF=[];bC=[]
for _ in range(2000):
    j=rng.integers(0,len(pi),len(pi))
    bF.append(f1([C1[x] for x in j])-f1([CK[x] for x in j])); bC.append(np.mean([C1[x][4] for x in j])-np.mean([CK[x][4] for x in j]))
res['dF1']=res['segF1_M1']-res['segF1_KD']; res['dF1_ci']=list(np.percentile(bF,[2.5,97.5]))
res['dCount']=res['countacc_M1']-res['countacc_KD']; res['dCount_ci']=list(np.percentile(bC,[2.5,97.5]))
res['gates']={'G1':bool(res['dF1']>=0.05 and res['dF1_ci'][0]>0),'G2':bool(res['fp_soluble_M1']<=res['fp_soluble_KD']),'G3':bool(res['dCount']>=0.10 and res['dCount_ci'][0]>0)}
json.dump(res,open('../results/metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
