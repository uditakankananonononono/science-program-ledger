#!/usr/bin/env python3
"""POST-HOC EXPLORATORY (written after results.json existed; not a gate). Specificity control for G2:
same learner and LOCO on 30 random gene sets of equal size (251) drawn from genes measured in all 5
cohorts, excluding FerrDb set genes. seed 0. Usage same as ferroatlas.py."""
import sys
src=open(sys.argv[0].replace('exploratory_random_sets.py','ferroatlas.py')).read().split('# G2')[0]
exec(src)
allc=sorted(set.intersection(*[set(E.index) for E,_ in cohorts.values()])-set(SET))
rng=np.random.default_rng(0); out_aucs=[]
for r in range(30):
    common=list(rng.choice(allc,251,replace=False))
    Xs=[];ys=[];cs=[];bs=[]
    for g,(E,K) in cohorts.items():
        Zs=(E.loc[common].T-E.loc[common].T.mean())/E.loc[common].T.std()
        Xs.append(Zs.values); ys.append(K.ad.values.astype(int)); cs+=[g]*len(K); bs.append(np.c_[K.age.values,K.sex.values])
    X=np.nan_to_num(np.vstack(Xs)); y=np.concatenate(ys); coh=np.array(cs); BA=np.vstack(bs); F=np.c_[X,BA]
    a=[]
    for g in cohorts:
        tr=coh!=g; te=coh==g
        m=make_pipeline(StandardScaler(),LogisticRegression(penalty='elasticnet',solver='saga',l1_ratio=0.5,C=0.5,class_weight='balanced',max_iter=5000))
        a.append(roc_auc_score(y[te],m.fit(F[tr],y[tr]).predict_proba(F[te])[:,1]))
    out_aucs.append(float(np.mean(a))); print(r,round(out_aucs[-1],3),flush=True)
ferro=json.load(open(os.path.join(out,'results.json')))['G2']['ferro_mean']
res={'random_mean_loco_auc':out_aucs,'median':float(np.median(out_aucs)),'ferro_mean':ferro,'frac_random_ge_ferro':float(np.mean(np.array(out_aucs)>=ferro))}
json.dump(res,open(os.path.join(out,'exploratory_random_sets.json'),'w'),indent=1); print({k:v for k,v in res.items() if k!='random_mean_loco_auc'})
