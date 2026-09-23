import json, re, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
from sklearn.model_selection import GroupKFold
AA='ACDEFGHIKLMNPQRSTVWY'; W=15; H=W//2
pos=json.load(open('../data/pos.json')); neg=json.load(open('../data/neg.json'))
def lab(p):
    y=np.zeros(len(p['seq']),int)
    for a,b in p['segs']: y[a:b]=1
    return y
def feats(s):
    pad='X'*H+s+'X'*H; F=np.zeros((len(s),W*20+4),np.float32)
    for i in range(len(s)):
        w=pad[i:i+W]
        for j,c in enumerate(w):
            if c in AA: F[i,j*20+AA.index(c)]=1
        F[i,-4]=sum(c in 'KR' for c in w); F[i,-3]=w.count('P'); F[i,-2]=w.count('H'); F[i,-1]=sum(c in 'DE' for c in w)
    return F
def dens(s,w=11):
    b=np.array([c in 'KR' for c in s],float); return np.convolve(b,np.ones(w),'same')
def regex_mask(s):
    m=np.zeros(len(s),bool)
    for i in range(len(s)-3):
        w=s[i:i+4]; nb=sum(c in 'KR' for c in w)
        if nb==4 or (nb==3 and any(c in 'HP' for c in w)): m[i:i+4]=True
    for i,c in enumerate(s):
        if c=='P':
            for k in range(i+1,i+4):
                if sum(x in 'KR' for x in s[k:k+4])>=3 and k+4<=len(s): m[i:k+4]=True
    for i in range(len(s)-1):
        if s[i] in 'KR' and s[i+1] in 'KR':
            for sp in (10,11,12):
                j=i+2+sp
                if j+5<=len(s) and sum(x in 'KR' for x in s[j:j+5])>=3: m[i:j+5]=True
    return m
def segs(mask):
    out=[];i=0;n=len(mask)
    while i<n:
        if mask[i]:
            j=i
            while j<n and mask[j]: j+=1
            out.append((i,j)); i=j
        else: i+=1
    return out
def seg_counts(pred,true):
    tp_t=sum(any(a<d and c<b for c,d in pred) for a,b in true)
    tp_p=sum(any(a<d and c<b for a,b in true) for c,d in pred)
    return tp_t,len(true),tp_p,len(pred)
def f1(C):
    C=np.sum(C,0); r=C[0]/C[1] if C[1] else 0; p=C[2]/C[3] if C[3] else 0
    return 2*p*r/(p+r) if p+r else 0.0
def best_thr(scores,ps):
    qs=np.unique(np.quantile(np.concatenate(scores),np.linspace(0.8,0.999,60)))
    return max(qs,key=lambda t:f1([seg_counts(segs(s>=t),p['segs']) for s,p in zip(scores,ps)]))
Y=[lab(p) for p in pos]; X=[feats(p['seq']) for p in pos]; D=[dens(p['seq']) for p in pos]
groups=[p['fam'] for p in pos]; rng=np.random.default_rng(11)
order=rng.permutation(len(pos)); inv=np.argsort(order)
S1=[None]*len(pos); T1=[]; T2=[]; R2=[None]*len(pos)
for tr,te in GroupKFold(5).split(order,groups=[groups[i] for i in order]):
    tr=order[tr]; te=order[te]
    clf=LogisticRegression(C=1.0,class_weight='balanced',max_iter=2000).fit(np.vstack([X[i] for i in tr]),np.concatenate([Y[i] for i in tr]))
    t1=best_thr([clf.decision_function(X[i]) for i in tr],[pos[i] for i in tr]); T1.append(t1)
    t2=best_thr([D[i] for i in tr],[pos[i] for i in tr]); T2.append(t2)
    for i in te: S1[i]=(clf.decision_function(X[i]),t1); R2[i]=t2
C0=[seg_counts(segs(regex_mask(p['seq'])),p['segs']) for p in pos]
C1=[seg_counts(segs(S1[i][0]>=S1[i][1]),pos[i]['segs']) for i in range(len(pos))]
C2=[seg_counts(segs(D[i]>=R2[i]),pos[i]['segs']) for i in range(len(pos))]
def auprc(idx,which):
    y=np.concatenate([Y[i] for i in idx]); s=np.concatenate([(S1[i][0] if which==1 else D[i]) for i in idx]); return average_precision_score(y,s)
yall=np.concatenate(Y); m0=np.concatenate([regex_mask(p['seq']) for p in pos])
res={'n_pos':len(pos),'n_seg':int(sum(len(p['segs']) for p in pos)),'n_neg':len(neg),
 'auprc_M1':auprc(range(len(pos)),1),'auprc_M2':auprc(range(len(pos)),2),'residue_base_rate':float(yall.mean()),
 'M0_residue_precision':float(yall[m0].mean()),'M0_residue_recall':float(m0[yall==1].mean()),
 'segF1_M0':f1(C0),'segF1_M1':f1(C1),'segF1_M2':f1(C2),'thr_M1_folds':[float(t) for t in T1],'thr_M2_folds':[float(t) for t in T2]}
for k,C in (('M0',C0),('M1',C1),('M2',C2)):
    s=np.sum(C,0); res['recall_'+k]=s[0]/s[1]; res['precision_'+k]=s[2]/max(s[3],1)
bA=[];bF=[]
for _ in range(2000):
    idx=rng.integers(0,len(pos),len(pos))
    bA.append(auprc(idx,1)-auprc(idx,2)); bF.append(f1([C1[i] for i in idx])-f1([C0[i] for i in idx]))
res['dAUPRC_M1_M2']=res['auprc_M1']-res['auprc_M2']; res['dAUPRC_ci']=list(np.percentile(bA,[2.5,97.5]))
res['dF1_M1_M0']=res['segF1_M1']-res['segF1_M0']; res['dF1_ci']=list(np.percentile(bF,[2.5,97.5]))
full=LogisticRegression(C=1.0,class_weight='balanced',max_iter=2000).fit(np.vstack(X),yall); tf=float(np.median(T1))
res['neg_flag_M1']=float(np.mean([np.any(full.decision_function(feats(n['seq']))>=tf) for n in neg]))
res['neg_flag_M0']=float(np.mean([regex_mask(n['seq']).any() for n in neg]))
res['neg_flag_M2']=float(np.mean([np.any(dens(n['seq'])>=np.median(T2)) for n in neg]))
res['gates']={'G1':bool(res['dAUPRC_M1_M2']>=0.05 and res['dAUPRC_ci'][0]>0),'G2':bool(res['dF1_M1_M0']>=0.05 and res['dF1_ci'][0]>0),'G3':bool(res['neg_flag_M1']<=res['neg_flag_M0'])}
json.dump(res,open('../results/metrics.json','w'),indent=1,default=float)
print(json.dumps(res,indent=1,default=float))
