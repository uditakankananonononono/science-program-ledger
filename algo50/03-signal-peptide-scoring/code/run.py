import gzip,csv,re,json,sys,numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import matthews_corrcoef, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
AA="ACDEFGHIKLMNPQRSTVWY"; IDX={a:i for i,a in enumerate(AA)}
KD=dict(A=1.8,R=-4.5,N=-3.5,D=-3.5,C=2.5,Q=-3.5,E=-3.5,G=-0.4,H=-3.2,I=4.5,L=3.8,K=-3.9,M=1.9,F=2.8,P=-1.6,S=-0.8,T=-0.7,W=-0.9,Y=-1.3,V=4.2)
def load(org):
    out=[]
    with gzip.open(f'data/{org}.tsv.gz','rt') as f:
        for r in csv.DictReader(f,delimiter='\t'):
            s=r['Sequence'][:70]
            if not set(s)<=set(AA): continue
            sig=r['Signal peptide']; tm=r['Transmembrane']
            if sig:
                m=re.match(r'SIGNAL 1\.\.(\d+);',sig)
                if not (m and re.search(r'ECO:0000269|ECO:0007744',sig)): continue
                out.append((r['Entry'],s,1,int(m.group(1)),0))
            else:
                m=re.search(r'TRANSMEM (\d+)\.\.',tm); hard=int(bool(m and int(m.group(1))<=40))
                out.append((r['Entry'],s,0,0,hard))
    return out
def kdmax(s):
    v=np.array([KD[c] for c in s[:35]]); return max(v[i:i+11].mean() for i in range(len(v)-10))
def comp(s):
    f=[]
    for a,b in [(0,10),(10,25),(25,40)]:
        c=np.zeros(20); seg=s[a:b]
        for ch in seg: c[IDX[ch]]+=1
        f+=list(c/max(len(seg),1))
    return f
tr=load('human'); te={o:load(o) for o in ['yeast','ecoli']}
# --- NHC emissions via Viterbi training on human positives
bg=np.ones(20)
for _,s,_,_,_ in tr:
    for ch in s: bg[IDX[ch]]+=1
bg/=bg.sum()
pos=[(s,L) for _,s,y,L,_ in tr if y==1 and 13<=L<=45]
def tables(parts):
    T={}
    for k in 'nhc':
        c=np.ones(20)
        for seg in parts[k]:
            for ch in seg: c[IDX[ch]]+=1
        T[k]=np.log(c/c.sum()/bg)
    for k in ['m3','m1']:
        c=np.ones(20)
        for ch in parts[k]: c[IDX[ch]]+=1
        T[k]=np.log(c/c.sum()/bg)
    return T
parts={'n':[s[:5] for s,L in pos],'h':[s[5:L-5] for s,L in pos],'c':[s[L-5:L] for s,L in pos],'m3':[s[L-3] for s,L in pos],'m1':[s[L-1] for s,L in pos]}
T=tables(parts)
def parse(s,T,end=None):
    x=np.array([IDX[c] for c in s]); P={k:np.concatenate([[0],np.cumsum(T[k][x])]) for k in 'nhc'}
    best=(-1e9,None)
    for nl in range(1,11):
        for hl in range(6,21):
            for cl in range(3,13):
                e=nl+hl+cl
                if e>min(len(s)-1,60) or (end is not None and e!=end): continue
                sc=P['n'][nl]+(P['h'][nl+hl]-P['h'][nl])+(P['c'][e]-P['c'][nl+hl])+T['m3'][x[e-3]]+T['m1'][x[e-1]]
                if sc>best[0]: best=(sc,(nl,hl,cl,P['n'][nl],P['h'][nl+hl]-P['h'][nl],P['c'][e]-P['c'][nl+hl]))
    return best
for it in range(3):  # Viterbi re-estimation constrained to the annotated cleavage site
    parts={k:[] for k in ['n','h','c','m3','m1']}
    for s,L in pos:
        sc,b=parse(s,T,end=L)
        if b is None: continue
        nl,hl,cl=b[:3]; parts['n'].append(s[:nl]); parts['h'].append(s[nl:nl+hl]); parts['c'].append(s[nl+hl:L]); parts['m3'].append(s[L-3]); parts['m1'].append(s[L-1])
    T=tables(parts)
def feats(data):
    B1=np.array([kdmax(s) for _,s,_,_,_ in data]); C=np.array([comp(s) for _,s,_,_,_ in data])
    N=[]
    for _,s,_,_,_ in data:
        sc,b=parse(s,T); N.append([sc,b[3],b[4],b[5],b[1],b[2]])
    return B1,np.hstack([C,B1[:,None]]),np.hstack([np.array(N),B1[:,None]])
y=np.array([d[2] for d in tr])
Xtr=feats(tr)
def fitpick(X):
    m=make_pipeline(StandardScaler(),LogisticRegression(C=1.0,max_iter=2000,class_weight='balanced'))
    best=None
    for Cv in [0.01,0.1,1,10]:
        m.set_params(logisticregression__C=Cv)
        p=cross_val_predict(m,X,y,cv=StratifiedKFold(5,shuffle=True,random_state=0),method='predict_proba')[:,1]
        ths=np.quantile(p,np.linspace(0.5,0.995,200)); mc=[matthews_corrcoef(y,p>=t) for t in ths]; i=int(np.argmax(mc))
        if best is None or mc[i]>best[0]: best=(mc[i],Cv,ths[i],roc_auc_score(y,p))
    m.set_params(logisticregression__C=best[1]); m.fit(X,y); return m,best
# B1 threshold on human
ths=np.quantile(Xtr[0],np.linspace(0.3,0.995,300)); mc=[matthews_corrcoef(y,Xtr[0]>=t) for t in ths]; b1t=ths[int(np.argmax(mc))]
mB2,iB2=fitpick(Xtr[1]); mP,iP=fitpick(Xtr[2])
res={'n_train':len(tr),'pos_train':int(y.sum()),'human_cv':{'B1_mcc':float(max(mc)),'B2':iB2[:2]+(float(iB2[3]),),'P':iP[:2]+(float(iP[3]),)}}
rng=np.random.default_rng(0); preds={}
for o,d in list(te.items())+[('pooled',te['yeast']+te['ecoli'])]:
    yy=np.array([x[2] for x in d]); hard=np.array([x[4] for x in d]).astype(bool); X=feats(d)
    pr={'B1':X[0]>=b1t,'B2':mB2.predict_proba(X[1])[:,1]>=iB2[2],'P':mP.predict_proba(X[2])[:,1]>=iP[2]}
    sc={'B1':X[0],'B2':mB2.predict_proba(X[1])[:,1],'P':mP.predict_proba(X[2])[:,1]}
    r={'n':len(d),'pos':int(yy.sum()),'hard':int(hard.sum())}
    for k in pr: r[k]={'mcc':float(matthews_corrcoef(yy,pr[k])),'auc':float(roc_auc_score(yy,sc[k])),'hardFPR':float(pr[k][hard].mean()),'recall':float(pr[k][yy==1].mean()),'FPR':float(pr[k][yy==0].mean())}
    if o=='pooled':
        diffs=[]
        for _ in range(2000):
            i=rng.integers(0,len(yy),len(yy)); diffs.append(matthews_corrcoef(yy[i],pr['P'][i])-matthews_corrcoef(yy[i],pr['B2'][i]))
        r['P_minus_B2_mcc_CI']=[float(np.percentile(diffs,2.5)),float(np.percentile(diffs,97.5))]
    res[o]=r
json.dump(res,open('results/results.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
json.dump({k:v.tolist() for k,v in T.items()},open('results/nhc_tables.json','w'))
