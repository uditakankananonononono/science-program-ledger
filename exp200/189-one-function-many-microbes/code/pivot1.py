import pandas as pd, numpy as np, json
exec(open('code/run.py').read().split("def cramers")[0])
keep=['Pseudomonadota','Actinomycetota','Bacillota','Bacteroidota','Methanobacteriota','Mycoplasmatota']
S=S[S.phylum.isin(keep)].reset_index(drop=True)
def vcorr(x,y):
    t=pd.crosstab(x,y).values; n=t.sum(); r,k=t.shape
    if r<2 or k<2: return np.nan
    e=np.outer(t.sum(1),t.sum(0))/n; chi=((t-e)**2/e).sum(); phi2=chi/n
    p2=max(0,phi2-(k-1)*(r-1)/(n-1)); rc=r-(r-1)**2/(n-1); kc=k-(k-1)**2/(n-1)
    return np.sqrt(p2/max(min(kc-1,rc-1),1e-9))
res={}; npass=0
for fn,ms in F.items():
    r=S.code.map(lambda c:'+'.join(sorted(m for m in ms if m in mods[c])))
    d=S.assign(route=r)[r!=''].reset_index(drop=True)
    vc=d.route.value_counts(); d['route']=d.route.where(d.route.map(vc)>=5,'other')
    if len(d)<15: res[fn]={'n':int(len(d)),'status':'too few genomes (fail)'}; print(fn,res[fn]); continue
    V=vcorr(d.route,d.phylum); null=[vcorr(pd.Series(rng.permutation(d.route.values)),d.phylum) for _ in range(1000)]
    p=(1+sum((n>=V) for n in null if n==n))/1001
    modal=d.groupby('phylum').route.agg(lambda s:s.value_counts().index[0]).to_dict()
    split=len(set(modal.values()))>=2
    ok=(V>=0.30) and (p<0.01) and split; npass+=ok
    res[fn]={'n':int(len(d)),'V_corrected':float(V),'p':float(p),'modal_route_by_phylum':modal,'lineage_split':split,'pass':bool(ok)}
    print(fn,res[fn])
res['summary']={'functions_passing':npass}
print(res['summary']); json.dump(res,open('results/pivot1.json','w'),indent=1)
