import pandas as pd, numpy as np, json, gc
from sklearn.metrics import roc_auc_score
rng=np.random.default_rng(0)
i11=pd.read_csv('data/9606.protein.info.v11.0.txt.gz',sep='\t',usecols=[0,1]); i11.columns=['pid','n']
i12=pd.read_csv('data/9606.protein.info.v12.0.txt.gz',sep='\t',usecols=[0,1]); i12.columns=['pid','n']
common=sorted(set(i11.n)&set(i12.n)); gid={n:k for k,n in enumerate(common)}; N=len(common)
m11=dict(zip(i11.pid,i11.n.map(gid))); m12=dict(zip(i12.pid,i12.n.map(gid)))
def keys(path,m,thr):
    ks=[];ss=[]
    for ch in pd.read_csv(path,sep=' ',chunksize=3_000_000):
        ch=ch[ch.combined_score>=thr]
        a=ch.protein1.map(m); b=ch.protein2.map(m); ok=a.notna()&b.notna()
        a=a[ok].astype(np.int64).values; b=b[ok].astype(np.int64).values; s=ch.combined_score[ok].values
        lo=np.minimum(a,b); hi=np.maximum(a,b); keep=lo!=hi
        ks.append(lo[keep]*N+hi[keep]); ss.append(s[keep])
    k=np.concatenate(ks); s=np.concatenate(ss); o=np.argsort(k); k,s=k[o],s[o]; u,idx=np.unique(k,return_index=True)
    return u,s[idx]
k11,s11=keys('data/9606.protein.links.v11.0.txt.gz',m11,400)
k12,s12=keys('data/9606.protein.links.v12.0.txt.gz',m12,400)
print('N',N,'v11>=400',len(k11),'v12>=400',len(k12))
E11=k11[s11>=700]
# adjacency of G11 (>=700)
a=E11//N; b=E11%N
nbr=[[] for _ in range(N)]
for x,y in zip(a,b): nbr[x].append(y); nbr[y].append(x)
nbr=[set(v) for v in nbr]; deg=np.array([len(v) for v in nbr])
inG11=deg>0
new=k12[s12>=700]; new=np.setdiff1d(new,k11)  # v11 <400 or absent
na=new//N; nb_=new%N; ok=inG11[na]&inG11[nb_]; new=new[ok]
print('positives available',len(new))
pos=rng.choice(new,5000,replace=False)
def inset(k,arr): 
    i=np.searchsorted(arr,k); return (i<len(arr))&(arr[np.minimum(i,len(arr)-1)]==k)
nodes=np.where(inG11)[0]
def key(u,v): return min(u,v)*N+max(u,v)
negA=[]
while len(negA)<5000:
    u,v=rng.choice(nodes,2,replace=False); k=key(u,v)
    if not inset(k,k12) and not inset(k,k11): negA.append(k)
order=np.argsort(deg[nodes]); sd=deg[nodes][order]; sn=nodes[order]
negB=[]
for k in pos:
    u,v=divmod(int(k),N); d=deg[v]; lo=np.searchsorted(sd,d*0.9); hi=np.searchsorted(sd,d*1.1,side='right')
    for _ in range(50):
        w=int(sn[rng.integers(lo,max(hi,lo+1))])
        kk=key(u,w)
        if w!=u and not inset(kk,k12) and not inset(kk,k11): negB.append(kk); break
def scores(ks):
    out=[]
    for k in ks:
        u,v=divmod(int(k),N); cn=nbr[u]&nbr[v]
        out.append((len(cn),sum(1/np.log(deg[z]) for z in cn if deg[z]>1),deg[u]*deg[v]))
    return np.array(out)
P,A,B=scores(pos),scores(negA),scores(negB)
res={'N_common_genes':N,'positives_available':int(len(new)),'n_negB':len(negB)}
for nm,j in [('CN',0),('AA',1),('PA',2)]:
    res[nm+'_vsA']=float(roc_auc_score(np.r_[np.ones(len(P)),np.zeros(len(A))],np.r_[P[:,j],A[:,j]]))
    res[nm+'_vsB']=float(roc_auc_score(np.r_[np.ones(len(P)),np.zeros(len(B))],np.r_[P[:,j],B[:,j]]))
y=np.r_[np.ones(len(P)),np.zeros(len(B))]; s=np.r_[P[:,1],B[:,1]]+rng.random(len(y))*1e-9
top=np.argsort(-s)[:len(y)//10]; res['AA_top_decile_precision_vsB']=float(y[top].mean())
res['frac_pos_with_zero_CN']=float((P[:,0]==0).mean()); res['frac_negB_zero_CN']=float((B[:,0]==0).mean())
print(json.dumps(res,indent=1)); json.dump(res,open('results/primary.json','w'),indent=1)
np.save('results/pos_scores.npy',P); np.save('results/negB_scores.npy',B)
