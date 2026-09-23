import pickle
src=open('code/run.py').read();exec(src[:src.index('D={}')])
exec(src[src.index('def z('):src.index('res={')])
common,clf=pickle.load(open('results/model.pkl','rb'))
pool={'c':[],'m':[],'b1':[],'b2':[],'y':[]};res={}
for p in ['GPL570','GPL96']:
    df,meta=load(f'GSE6269-{p}')
    y=[]
    for m in meta:
        pa=[x for x in m.split(' | ') if x.startswith('Pathogen:')][0]
        y.append(0 if 'Influenza A' in pa else np.nan if 'Influenza' in pa else 1)
    y=np.array(y);k=~np.isnan(y);X=genes(df,'GPL96').iloc[:,np.where(k)[0]];y=y[k].astype(int)
    miss=[g for g in common if g not in X.index];Xc=X.reindex(common)
    Rk=np.apply_along_axis(lambda c:rankdata(np.nan_to_num(c,nan=np.nanmedian(c)))/len(c),0,Xc.values).T
    pm=clf.predict_proba(Rk)[:,1]
    zz,gl=z(X,['IFI44L','FAM89A']);b1=-(zz.loc['IFI44L']-zz.loc['FAM89A']).values if len(gl)==2 else np.zeros(len(y))
    up,gu=z(X,['HK3','TNIP1','GPAA1','CTSB']);dn,gd=z(X,['IFI27','JUP','LAX1']);b2=(up.mean(0)-dn.mean(0)).values
    pr=lambda s:rankdata(s)/len(s);c=(pr(pm)+pr(b2))/2
    res[p]=dict(n_bact=int(y.sum()),n_fluA=int((1-y).sum()),n_model_genes_missing=len(miss),b1_genes=gl,b2_genes=gu+gd,
      model=roc_auc_score(y,pm),B1=roc_auc_score(y,b1),B2=roc_auc_score(y,b2),combined=roc_auc_score(y,c))
    for kk,s in [('c',c),('m',pm),('b1',b1),('b2',b2)]: pool[kk]+=list(pr(s))
    pool['y']+=list(y)
P={k:np.array(v) for k,v in pool.items()};y=P['y'];pa={k:roc_auc_score(y,P[k]) for k in('c','m','b1','b2')}
bb='b1' if pa['b1']>=pa['b2'] else 'b2';rng=np.random.default_rng(0);i1=np.where(y==1)[0];i0=np.where(y==0)[0];d=[]
for _ in range(2000):
    s=np.concatenate([rng.choice(i1,len(i1)),rng.choice(i0,len(i0))]);d.append(roc_auc_score(y[s],P['c'][s])-roc_auc_score(y[s],P[bb][s]))
res['pooled']=dict(pa,best_baseline=bb,diff=pa['c']-pa[bb],CI=[float(np.percentile(d,2.5)),float(np.percentile(d,97.5))])
res['P1_G1']=bool(pa['c']>=0.85);res['P1_G2']=bool(res['pooled']['diff']>=0.02 and res['pooled']['CI'][0]>0)
print(json.dumps(res,indent=1));json.dump(res,open('results/pivot1.json','w'),indent=1)
