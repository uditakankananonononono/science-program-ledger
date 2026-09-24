import json,glob,numpy as np,pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
S={}
for f in sorted(glob.glob('../data/fluview_*.json')):
    e=json.load(open(f))['epidata']; r=f.split('_')[1][:-5]
    S[r]=pd.DataFrame({'ew':[x['epiweek'] for x in e],'y':[max(x['wili'],0.05) for x in e]}).sort_values('ew').reset_index(drop=True)
TRS=range(2003,2017); TES=[2017,2018,2022,2023]
for r,d in S.items():
    yr,wk=d.ew//100,d.ew%100; d['season']=np.where(wk>=40,yr,yr-1)
    d['wos']=d.groupby('season').cumcount()+np.where(d.groupby('season').ew.transform('min')%100>=40,0,0)
    first=d.groupby('season').ew.transform('first')%100; d.loc[first!=40,'wos']=np.nan  # partial first season
clim={}
for r,d in S.items():
    t=d[d.season.isin(TRS)&d.wos.notna()]; c=t.groupby('wos').y.mean(); clim[r]=c
def C(r,w): c=clim[r]; w=min(int(w),51); return c.loc[w]
rows=[]
for r,d in S.items():
    y=d.y.values
    for i in range(3,len(d)-1):
        if np.isnan(d.wos[i]) or d.wos[i]>33: continue
        for h in range(1,5):
            j=i+h
            if j>=len(d) or d.season[j]!=d.season[i] and not (d.season[i] in TRS and d.season[j] in TRS): continue
            w=d.wos[i]; rows.append(dict(r=r,season=d.season[i],tseason=d.season[j],h=h,yt=y[i],y1=y[i-1],y2=y[i-2],y3=y[i-3],yh=y[j],ct=C(r,w),ch=C(r,w+h),wos=w))
D=pd.DataFrame(rows)
def X(q): 
    return np.c_[np.log(q.yt),np.log(q.y1),np.log(q.y2),np.log(q.y3),np.log(q.ct),np.log(q.ch),np.log(q.yt)-np.log(q.ct),np.sin(2*np.pi*q.wos/52),np.cos(2*np.pi*q.wos/52)]
tr=D[D.season.isin(TRS)&D.tseason.isin(TRS)]; te=D[D.season.isin(TES)].copy()
print('train rows',len(tr),'test rows',len(te),te.groupby('season').size().to_dict(),flush=True)
te['pers']=te.yt; te['clim']=te.ch; te['gbm']=np.nan
for h in range(1,5):
    a=tr[tr.h==h]; m=HistGradientBoostingRegressor(max_iter=300,learning_rate=0.05,max_leaf_nodes=15,random_state=39).fit(X(a),np.log(a.yh)-np.log(a.yt))
    b=te.h==h; te.loc[b,'gbm']=te.yt[b]*np.exp(m.predict(X(te[b])))
for k in ('pers','clim','gbm'): te['e_'+k]=(te[k]-te.yh).abs()
te.to_csv('../results/test_forecasts.tsv.gz',sep='\t',index=False)
def stats(t):
    g=t.groupby('h')[['e_pers','e_clim','e_gbm']].mean(); rp=g.e_gbm/g.e_pers; rc=g.e_gbm/g.e_clim
    return rp.mean(),rp.loc[1],rc.mean(),g
rp,rp1,rc,g=stats(te); res={'mae_by_h':g.to_dict(),'relMAE_pers_mean':rp,'relMAE_pers_h1':rp1,'relMAE_clim_mean':rc}
blocks=[b for _,b in te.groupby(['season','r'])]; rng=np.random.default_rng(39); B=[]
for _ in range(2000):
    t=pd.concat([blocks[i] for i in rng.integers(0,len(blocks),len(blocks))]); B.append(stats(t)[:3])
B=np.array(B); ci=lambda v:[float(x) for x in np.percentile(v,[2.5,97.5])]
res['ci1'],res['ci2'],res['ci3']=ci(B[:,0]),ci(B[:,1]),ci(B[:,2])
res['per_season_relMAE_pers']={int(s):float(stats(t)[0]) for s,t in te.groupby('season')}
res['gates']={'G1':bool(rp<=0.90 and res['ci1'][1]<1),'G2':bool(res['ci2'][1]<1),'G3':bool(res['ci3'][1]<1)}
json.dump(res,open('../results/metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
