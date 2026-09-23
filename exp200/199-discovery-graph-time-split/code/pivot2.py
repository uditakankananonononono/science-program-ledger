import pandas as pd, numpy as np, json
import scipy.sparse as sp
exec(open('code/run.py').read().split("k11,s11=keys")[0])  # loaders + keys()
k11w,s11w=keys('data/9606.protein.links.v11.0.txt.gz',m11,150)
k12,s12=keys('data/9606.protein.links.v12.0.txt.gz',m12,400)
rng=np.random.default_rng(0)
E=k11w[s11w>=700]; a=E//N; b=E%N
A=sp.coo_matrix((np.ones(len(a)*2),(np.r_[a,b],np.r_[b,a])),shape=(N,N)).tocsr()
deg=np.asarray(A.sum(1)).ravel(); w=np.where(deg>1,1/np.log(np.maximum(deg,2)),0)
Aw=A@sp.diags(w)
pool=(s11w>=150)&(s11w<400); pk=k11w[pool]; pw=s11w[pool]
u=pk//N; v=pk%N; ok=(deg[u]>0)&(deg[v]>0); pk,pw,u,v=pk[ok],pw[ok],u[ok],v[ok]
AA=np.zeros(len(pk))
for i in range(0,len(pk),200000):
    s=slice(i,i+200000); AA[s]=np.asarray(Aw[u[s]].multiply(A[v[s]]).sum(1)).ravel()
j=np.searchsorted(k12,pk); j=np.minimum(j,len(k12)-1); y=(k12[j]==pk)&(s12[j]>=700)
jit=rng.random(len(pk))*1e-9
def top(score,n=1000): return float(y[np.argsort(-(score+jit))[:n]].mean())
S=(pw/1000)*(1+AA)
res={'pool':int(len(pk)),'base_rate':float(y.mean()),'S_top1000':top(S),'W_top1000':top(pw.astype(float)),'AA_top1000':top(AA),
     'S_top10000':top(S,10000),'W_top10000':top(pw.astype(float),10000),'AA_top10000':top(AA,10000)}
res['S_fold_vs_base']=res['S_top1000']/res['base_rate']
print(json.dumps(res,indent=1)); json.dump(res,open('results/pivot2.json','w'),indent=1)
o=np.argsort(-(S+jit))[:1000]
inv={i:n for n,i in gid.items()}
pd.DataFrame({'gene_a':[inv[x] for x in u[o]],'gene_b':[inv[x] for x in v[o]],'v11_score':pw[o],'AA':AA[o],'S':S[o],'v12_ge700':y[o]}).to_csv('results/pivot2_top1000.csv',index=False)
