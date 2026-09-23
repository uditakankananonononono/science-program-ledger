import pandas as pd, numpy as np, json
from collections import defaultdict
GLOBAL=set(range(1100,1250))
out={}
for tax,org in [('511145','eco'),('224308','bsu')]:
    k=pd.read_csv(f'data/kegg_{org}.tsv',sep='\t',header=None,names=['g','p']); k['g']=k.g.str.split(':').str[1]
    k=k[~k.p.str[-5:].astype(int).isin(GLOBAL)]; lab=k.groupby('g').p.apply(set).to_dict()
    names=pd.read_csv(f'data/kegg_{org}_names.tsv',sep='\t',header=None,names=['p','n']); nm=dict(zip('path:'+names.p,names.n))
    L=pd.read_csv(f'data/{tax}.protein.links.detailed.v11.0.txt.gz',sep=' ',usecols=['protein1','protein2','cooccurence'])
    L=L[L.cooccurence>=400]; L['a']=L.protein1.str.split('.',n=1).str[1]; L['b']=L.protein2.str.split('.',n=1).str[1]
    nb=defaultdict(list)
    for a,b,s in L[['a','b','cooccurence']].values: nb[a].append((b,s))
    # calibrate: precision by vote-share bin on known genes (LOO)
    rows=[]
    for g in set(nb):
        v=defaultdict(float); tot=0
        for b,s in nb[g]:
            if b in lab and b!=g:
                for p in lab[b]: v[p]+=s
                tot+=s
        if not v: continue
        top=max(v,key=v.get); share=v[top]/tot
        rows.append((g,g in lab,top,nm.get(top,top),share,(top in lab[g]) if g in lab else None))
    d=pd.DataFrame(rows,columns=['gene','known','pred','pred_name','vote_share','correct'])
    d['bin']=pd.cut(d.vote_share,[0,.5,.8,1.0001])
    cal=d[d.known].groupby('bin',observed=True).correct.agg(['mean','count'])
    u=d[~d.known].sort_values('vote_share',ascending=False)
    u.to_csv(f'results/unknown_predictions_{org}.csv',index=False)
    out[org]={'calibration':{str(i):{'precision':float(r['mean']),'n':int(r['count'])} for i,r in cal.iterrows()},
      'unannotated_with_prediction':int(len(u)),'unannotated_share>0.8':int((u.vote_share>0.8).sum())}
    print(org,cal.to_string()); print(u.head(8).to_string())
json.dump(out,open('results/unknown_summary.json','w'),indent=1); print(json.dumps(out,indent=1))
