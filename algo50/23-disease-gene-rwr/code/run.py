import gzip, json, numpy as np, scipy.sparse as sp, collections
info={}
for l in gzip.open('../data/string_info.txt.gz','rt'):
    if l.startswith('#'): continue
    f=l.split('\t'); info[f[0]]=f[1]
ed=set()
f=gzip.open('../data/string_detailed.txt.gz','rt'); next(f)
for l in f:
    p=l.split()
    if int(p[6])>=400 and p[0] in info and p[1] in info:
        a,b=info[p[0]],info[p[1]]
        if a!=b: ed.add((min(a,b),max(a,b)))
nodes=sorted({x for e in ed for x in e}); ix={n:i for i,n in enumerate(nodes)}; N=len(nodes)
r=[ix[a] for a,b in ed]+[ix[b] for a,b in ed]; c=[ix[b] for a,b in ed]+[ix[a] for a,b in ed]
A=sp.csr_matrix((np.ones(len(r)),(r,c)),shape=(N,N)); deg=np.asarray(A.sum(0)).ravel()
Wm=(A@sp.diags(1/deg)).tocsr().astype(np.float32)
dis=collections.defaultdict(set)
for l in list(open('../data/genes_to_disease.txt'))[1:]:
    f=l.rstrip('\n').split('\t')
    if f[2]=='MENDELIAN' and f[1] in ix: dis[f[3]].add(ix[f[1]])
dis={d:sorted(g) for d,g in dis.items() if 5<=len(g)<=50}
R=0.7
def rwr(P0):
    P=P0.copy()
    for _ in range(100):
        Pn=(1-R)*(Wm@P)+R*P0
        if np.abs(Pn-P).sum(0).max()<1e-8: P=Pn; break
        P=Pn
    return P
base=rwr(np.full((N,1),1/N,np.float32))[:,0]
Q=[(d,h,[s for s in g if s!=h]) for d,g in dis.items() for h in g]
res_rows=[]
for b0 in range(0,len(Q),400):
    batch=Q[b0:b0+400]; P0=np.zeros((N,len(batch)),np.float32)
    for k,(d,h,seeds) in enumerate(batch): P0[seeds,k]=1/len(seeds)
    P=rwr(P0)
    for k,(d,h,seeds) in enumerate(batch):
        cand=np.ones(N,bool); cand[seeds]=False; ci=np.where(cand)[0]
        dn=np.asarray(A[:,seeds].sum(1)).ravel()
        sc={'DEG':deg,'DN':dn+deg/(deg.max()+1),'RWR':P[:,k],'RWRdc':P[:,k]/base}
        row={'disease':d,'gene':nodes[h]}
        for m,s in sc.items():
            sv=s[ci]; hv=s[h]; rank=1+(sv>hv).sum()+0.5*((sv==hv).sum()-1)
            row['rank_'+m]=float(rank); row['auc_'+m]=1-(rank-1)/(len(ci)-1)
        res_rows.append(row)
import pandas as pd
df=pd.DataFrame(res_rows); df.to_csv('../results/per_query.tsv',sep='\t',index=False)
M=['DEG','DN','RWR','RWRdc']
out={'n_nodes':N,'n_edges':len(ed),'n_diseases':len(dis),'n_queries':len(df)}
for m in M: out['auroc_'+m]=df['auc_'+m].mean(); out['top100_'+m]=(df['rank_'+m]<=100).mean()
rng=np.random.default_rng(23); ds=df['disease'].unique(); grp={d:df.index[df['disease']==d].values for d in ds}
b1=[];b2=[];b3=[]
for _ in range(2000):
    idx=np.concatenate([grp[d] for d in rng.choice(ds,len(ds))]); s=df.loc[idx]
    b1.append(s['auc_RWR'].mean()-s['auc_DN'].mean()); b2.append((s['rank_RWR']<=100).mean()-(s['rank_DN']<=100).mean()); b3.append((s['rank_RWRdc']<=100).mean()-(s['rank_RWR']<=100).mean())
out['d_auc_RWR_DN']=out['auroc_RWR']-out['auroc_DN']; out['ci1']=list(np.percentile(b1,[2.5,97.5]))
out['d_top_RWR_DN']=out['top100_RWR']-out['top100_DN']; out['ci2']=list(np.percentile(b2,[2.5,97.5]))
out['d_top_dc_RWR']=out['top100_RWRdc']-out['top100_RWR']; out['ci3']=list(np.percentile(b3,[2.5,97.5]))
out['gates']={'G1':bool(out['d_auc_RWR_DN']>=0.02 and out['ci1'][0]>0),'G2':bool(out['d_top_RWR_DN']>=0.02 and out['ci2'][0]>0),'G3':bool(out['d_top_dc_RWR']>0 and out['ci3'][0]>0)}
json.dump(out,open('../results/metrics.json','w'),indent=1,default=float); print(json.dumps(out,indent=1,default=float))
