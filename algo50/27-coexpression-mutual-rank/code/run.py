import numpy as np, pandas as pd, json
from scipy.stats import rankdata
par=set(l.split()[0] for l in open('../data/ReactomePathwaysRelation.txt') if l.startswith('R-HSA'))
pw={}
for l in open('../data/ReactomePathways.gmt'):
    f=l.rstrip('\n').split('\t')
    if f[1] not in par and 10<=len(f)-2<=200: pw[f[1]]=set(f[2:])
g=pd.read_csv('../data/gtex_median_tpm.gct.gz',sep='\t',skiprows=2)
tis=[c for c in g.columns if c not in('Name','Description') and not c.startswith('Cells')]
g=g[g[tis].max(1)>=1].drop_duplicates('Description')
allg=set().union(*pw.values()); g=g[g.Description.isin(allg)].reset_index(drop=True)
genes=list(g.Description); N=len(genes); gi={x:i for i,x in enumerate(genes)}
X=np.log2(g[tis].values.astype(np.float64)+1); X=(X-X.mean(1,keepdims=True))/X.std(1,keepdims=True)
C=(X@X.T/X.shape[1]).astype(np.float32); np.fill_diagonal(C,np.nan)
Rk=np.empty((N,N),np.float32)
for i in range(N):
    row=C[i].copy(); row[i]=-np.inf; Rk[i]=rankdata(-row,method='average')
mu=np.nanmean(C,1); sd=np.nanstd(C,1)
Xr=np.apply_along_axis(rankdata,1,g[tis].values.astype(float)); Xr=(Xr-Xr.mean(1,keepdims=True))/Xr.std(1,keepdims=True)
mem=[set() for _ in range(N)]
for k,(p,s) in enumerate(pw.items()):
    for x in s:
        if x in gi: mem[gi[x]].add(k)
rows=[]
for i in range(N):
    if not mem[i]: continue
    lab=np.array([bool(mem[i]&mem[j]) for j in range(N)]); lab[i]=False
    if lab.sum()==0: continue
    msk=np.ones(N,bool); msk[i]=False; y=lab[msk]
    zi=np.nan_to_num((C[i]-mu[i])/sd[i]).clip(min=0); zj=np.nan_to_num((C[:,i]-mu)/sd).clip(min=0)
    sc={'PCC':np.nan_to_num(C[i]),'SCC':(Xr[i]@Xr.T/Xr.shape[1]),'MR':-np.sqrt(Rk[i]*Rk[:,i]),'CLR':np.sqrt(zi**2+zj**2)}
    r={'gene':genes[i],'n_partners':int(y.sum())}
    for k,s in sc.items():
        s=s[msk].astype(np.float64); rk=rankdata(s); npos=y.sum(); nneg=len(y)-npos
        r['auc_'+k]=(rk[y].sum()-npos*(npos+1)/2)/(npos*nneg)
        top=np.argsort(-s,kind='stable')[:50]; r['p50_'+k]=y[top].mean()
    rows.append(r)
df=pd.DataFrame(rows); df.to_csv('../results/per_gene.tsv.gz',sep='\t',index=False)
M=['PCC','SCC','MR','CLR']; res={'n_genes':N,'n_query':len(df),'n_pathways':len(pw),'mean_partner_rate':float((df.n_partners/(N-1)).mean())}
for k in M: res['auroc_'+k]=df['auc_'+k].mean(); res['p50_'+k]=df['p50_'+k].mean()
rng=np.random.default_rng(27); A=df[['auc_MR','auc_PCC','auc_CLR','p50_MR','p50_PCC']].values; b=[]
for _ in range(2000):
    s=A[rng.integers(0,len(A),len(A))].mean(0); b.append([s[0]-s[1],s[3]-s[4],s[0]-s[2]])
b=np.array(b)
res['d_auc_MR_PCC']=res['auroc_MR']-res['auroc_PCC']; res['ci1']=list(np.percentile(b[:,0],[2.5,97.5]))
res['d_p50_MR_PCC']=res['p50_MR']-res['p50_PCC']; res['ci2']=list(np.percentile(b[:,1],[2.5,97.5]))
res['d_auc_MR_CLR']=res['auroc_MR']-res['auroc_CLR']; res['ci3']=list(np.percentile(b[:,2],[2.5,97.5]))
res['gates']={'G1':bool(res['d_auc_MR_PCC']>=0.01 and res['ci1'][0]>0),'G2':bool(res['d_p50_MR_PCC']>=0.005 and res['ci2'][0]>0),'G3':bool(res['d_auc_MR_CLR']>0 and res['ci3'][0]>0)}
json.dump(res,open('../results/metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
