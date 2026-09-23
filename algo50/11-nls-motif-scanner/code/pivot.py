# Amendment 2 pivot: regex-then-scanner cascade (M3). Reuses run.py definitions and folds.
exec(open('run.py').read().split('Y=[lab(p)')[0])
Y=[lab(p) for p in pos]; X=[feats(p['seq']) for p in pos]
groups=[p['fam'] for p in pos]; rng=np.random.default_rng(11)
order=rng.permutation(len(pos))
R0=[segs(regex_mask(p['seq'])) for p in pos]
def cascade(sc,rs,t): return [(a,b) for a,b in rs if sc[a:b].max()>=t]
C3=[None]*len(pos); T3=[]
for tr,te in GroupKFold(5).split(order,groups=[groups[i] for i in order]):
    tr=order[tr]; te=order[te]
    clf=LogisticRegression(C=1.0,class_weight='balanced',max_iter=2000).fit(sp.vstack([X[i] for i in tr]).tocsr(),np.concatenate([Y[i] for i in tr]))
    sc={i:clf.decision_function(X[i]) for i in np.concatenate([tr,te])}
    cand=np.unique(np.quantile([sc[i][a:b].max() for i in tr for a,b in R0[i]],np.linspace(0,0.95,60)))
    t=max(cand,key=lambda t:f1([seg_counts(cascade(sc[i],R0[i],t),pos[i]['segs']) for i in tr])); T3.append(float(t))
    for i in te: C3[i]=seg_counts(cascade(sc[i],R0[i],t),pos[i]['segs'])
C0=[seg_counts(R0[i],pos[i]['segs']) for i in range(len(pos))]
res={'segF1_M0':f1(C0),'segF1_M3':f1(C3),'thr_M3_folds':T3}
for k,C in (('M0',C0),('M3',C3)):
    s=np.sum(C,0); res['recall_'+k]=s[0]/s[1]; res['precision_'+k]=s[2]/max(s[3],1)
b=[]
for _ in range(2000):
    idx=rng.integers(0,len(pos),len(pos)); b.append(f1([C3[i] for i in idx])-f1([C0[i] for i in idx]))
res['dF1_M3_M0']=res['segF1_M3']-res['segF1_M0']; res['dF1_ci']=list(np.percentile(b,[2.5,97.5]))
full=LogisticRegression(C=1.0,class_weight='balanced',max_iter=2000).fit(sp.vstack(X).tocsr(),np.concatenate(Y)); tm=float(np.median(T3))
fl3=[];fl0=[]
for n in neg:
    r=segs(regex_mask(n['seq'])); fl0.append(len(r)>0)
    fl3.append(len(r)>0 and len(cascade(full.decision_function(feats(n['seq'])),r,tm))>0)
res['neg_flag_M0']=float(np.mean(fl0)); res['neg_flag_M3']=float(np.mean(fl3))
res['pivot_gates']={'P1':bool(res['dF1_M3_M0']>=0.03 and res['dF1_ci'][0]>0),'P2':bool(res['neg_flag_M3']<=0.5*res['neg_flag_M0'])}
json.dump(res,open('../results/pivot_metrics.json','w'),indent=1,default=float)
print(json.dumps(res,indent=1,default=float))
