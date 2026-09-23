import sys,pickle,json,numpy as np; sys.path.insert(0,'code')
from feat import *; from seg import *
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, matthews_corrcoef
d=pickle.load(open('data/set.pkl','rb'))
for x in d: x['F']=feats(x['seq']); x['fi']=foldindex(x['seq']); x['top']=topidp(x['seq'])
tr=[x for x in d if x['split']=='train']; tu=[x for x in d if x['split']=='tune']; te=[x for x in d if x['split']=='test']
X=np.vstack([x['F'] for x in tr]); Y=np.concatenate([x['y'] for x in tr])
rng=np.random.default_rng(0); idx=rng.choice(len(Y),min(400000,len(Y)),replace=False)
sc=StandardScaler().fit(X[idx]); m=LogisticRegression(max_iter=2000,class_weight='balanced').fit(sc.transform(X[idx]),Y[idx])
for x in d: x['p']=m.predict_proba(sc.transform(x['F']))[:,1]
pt=np.concatenate([x['p'] for x in tr]); ths=np.quantile(pt,np.linspace(0.3,0.98,120)); mc=[matthews_corrcoef(Y,pt>=t) for t in ths]; tau=float(ths[int(np.argmax(mc))])
b=np.log(tau/(1-tau))
def emis(p): p=np.clip(p,1e-6,1-1e-6); return np.log(p/(1-p))-b
def rf1(data,labs):
    tp=np_=nt=0
    for x,l in zip(data,labs): a,bb,c=region_counts(x['y'],l); tp+=a; np_+=bb; nt+=c
    pr=tp/max(np_,1); rc=tp/max(nt,1); return 2*pr*rc/max(pr+rc,1e-9)
grid={}
for L in (5,10,20,30):
    for pen in (1,2,4,8):
        grid[(L,pen)]=rf1(tu,[segment(emis(x['p']),L,float(pen)) for x in tu])
Lb,pb=max(grid,key=grid.get)
thr_tu=rf1(tu,[(x['p']>=tau).astype(np.int8) for x in tu])
for x in te: x['thr']=(x['p']>=tau).astype(np.int8); x['hmm']=segment(emis(x['p']),Lb,float(pb))
def metrics(S):
    y=np.concatenate([x['y'] for x in S]); r={}
    for k in ('p','fi','top'): r['auc_'+k]=float(roc_auc_score(y,np.concatenate([x[k] for x in S])))
    for k in ('thr','hmm'):
        yp=np.concatenate([x[k] for x in S]); r['mcc_'+k]=float(matthews_corrcoef(y,yp)); r['rf1_'+k]=rf1(S,[x[k] for x in S])
        r['regions_per_kres_'+k]=1000*sum(len(regions(x[k])) for x in S)/len(y)
    r['regions_per_kres_true']=1000*sum(len(regions(x['y'])) for x in S)/len(y); return r
res={'n':{s:len(v) for s,v in [('train',tr),('tune',tu),('test',te)]},'tau':tau,'tune_grid':{f'{k[0]}_{k[1]}':v for k,v in grid.items()},'tune_thr_rf1':thr_tu,'chosen':[Lb,pb]}
res['test']=metrics(te); nh=[x for x in te if x['tax']!=9606]; res['test_nonhuman']=metrics(nh)
def cnt(S,k):
    return np.array([region_counts(x['y'],x[k]) for x in S]),np.array([[((x[k]==1)&(x['y']==1)).sum(),((x[k]==1)&(x['y']==0)).sum(),((x[k]==0)&(x['y']==1)).sum(),((x[k]==0)&(x['y']==0)).sum()] for x in S],float)
def f1c(c): t=c.sum(0); pr=t[0]/max(t[1],1); rc=t[0]/max(t[2],1); return 2*pr*rc/max(pr+rc,1e-9)
def mccc(c):
    tp,fp,fn,tn=c.sum(0); return (tp*tn-fp*fn)/np.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
Rt,Ct=cnt(te,'thr'); Rh,Ch=cnt(te,'hmm'); bs={'rf1_diff':[],'mcc_diff':[],'auc_diff':[]}
for it in range(2000):
    i=rng.integers(0,len(te),len(te))
    bs['rf1_diff'].append(f1c(Rh[i])-f1c(Rt[i])); bs['mcc_diff'].append(mccc(Ch[i])-mccc(Ct[i]))
    if it<500:
        S=[te[j] for j in i]; y=np.concatenate([x['y'] for x in S])
        bs['auc_diff'].append(roc_auc_score(y,np.concatenate([x['p'] for x in S]))-roc_auc_score(y,np.concatenate([x['fi'] for x in S])))
res['boot_CI']={k:[float(np.percentile(v,2.5)),float(np.percentile(v,97.5))] for k,v in bs.items()}; res['boot_B']={'rf1':2000,'mcc':2000,'auc':500}
json.dump(res,open('results/results.json','w'),indent=1); print(json.dumps(res,indent=1))
pickle.dump({'coef':m.coef_,'int':m.intercept_,'mu':sc.mean_,'sd':sc.scale_,'tau':tau,'L':Lb,'pen':pb},open('results/model.pkl','wb'))
