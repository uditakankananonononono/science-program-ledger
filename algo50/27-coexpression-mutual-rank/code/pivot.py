exec(open('run.py').read().split("Rk=np.empty")[0])
import scipy.sparse as sp
Cn=np.nan_to_num(C,nan=-np.inf); K=50
top=np.argpartition(-Cn,K,axis=1)[:,:K]
B=sp.csr_matrix((np.ones(N*K,np.float32),(np.repeat(np.arange(N),K),top.ravel())),shape=(N,N))
SN=(B@B.T).tocsr()
mem=[set() for _ in range(N)]
for k,(p,s) in enumerate(pw.items()):
    for x in s:
        if x in gi: mem[gi[x]].add(k)
rows=[]
for i in range(N):
    lab=np.array([bool(mem[i]&mem[j]) for j in range(N)]); lab[i]=False
    if not mem[i] or lab.sum()==0: continue
    msk=np.ones(N,bool); msk[i]=False; y=lab[msk]
    pcc=np.nan_to_num(C[i]).astype(np.float64); snn=SN[i].toarray().ravel()/K+0.001*pcc
    r={'gene':genes[i]}
    for k,s in (('PCC',pcc),('SNN',snn)):
        s=s[msk]; rk=rankdata(s); npos=y.sum(); nneg=len(y)-npos
        r['auc_'+k]=(rk[y].sum()-npos*(npos+1)/2)/(npos*nneg); r['p50_'+k]=y[np.argsort(-s,kind='stable')[:50]].mean()
    rows.append(r)
df=pd.DataFrame(rows); df.to_csv('../results/per_gene_pivot.tsv.gz',sep='\t',index=False)
res={'n_query':len(df)}
for k in ('PCC','SNN'): res['auroc_'+k]=df['auc_'+k].mean(); res['p50_'+k]=df['p50_'+k].mean()
A=df[['auc_SNN','auc_PCC','p50_SNN','p50_PCC']].values; rng=np.random.default_rng(27); b=[]
for _ in range(2000):
    s=A[rng.integers(0,len(A),len(A))].mean(0); b.append([s[0]-s[1],s[2]-s[3]])
b=np.array(b)
res['d_auc']=res['auroc_SNN']-res['auroc_PCC']; res['ci1']=list(np.percentile(b[:,0],[2.5,97.5]))
res['d_p50']=res['p50_SNN']-res['p50_PCC']; res['ci2']=list(np.percentile(b[:,1],[2.5,97.5]))
res['pivot_gates']={'P1':bool(res['d_auc']>=0.01 and res['ci1'][0]>0),'P2':bool(res['d_p50']>=0.005 and res['ci2'][0]>0)}
json.dump(res,open('../results/pivot_metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
