exec(open('run.py').read().split('X=np.array([feats(s)')[0])
def low(s):
    n=len(s); return [charge(s),moment(s),n,sum(c in 'AILMFVWC' for c in s)/n,s.count('C'),sum(c in 'FWY' for c in s)/n,sum(c in 'GP' for c in s)/n,charge(s)*moment(s)]
X=np.array([low(s) for s in seq]); SR=X[:,7]; SP=np.zeros(len(D))
for tr,te in GroupKFold(5).split(X,y,gp):
    m=make_pipeline(StandardScaler(),LogisticRegression(C=1.0,class_weight='balanced',max_iter=5000)).fit(X[tr],y[tr]); SP[te]=m.decision_function(X[te])
cys=np.array([s.count('C')>=4 for s in seq])
res={'auroc_R':roc_auc_score(y,SR),'auroc_LP':roc_auc_score(y,SP),'auprc_LP':average_precision_score(y,SP),'cys_auroc_LP':roc_auc_score(y[cys],SP[cys]),'cys_auroc_R':roc_auc_score(y[cys],SR[cys])}
gi={x:np.where(g==x)[0] for x in ug}; b=[]
for _ in range(2000):
    idx=np.concatenate([gi[x] for x in rng.choice(ug,len(ug))])
    if len(set(y[idx]))<2: continue
    b.append(roc_auc_score(y[idx],SP[idx])-roc_auc_score(y[idx],SR[idx]))
res['d_LP-R']=res['auroc_LP']-res['auroc_R']; res['ci_LP-R']=list(np.percentile(b,[2.5,97.5]))
res['pivot_gates']={'P1':bool(res['d_LP-R']>=0.03 and res['ci_LP-R'][0]>0),'P2':bool(res['cys_auroc_LP']>=0.80)}
json.dump(res,open('../results/pivot_metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
