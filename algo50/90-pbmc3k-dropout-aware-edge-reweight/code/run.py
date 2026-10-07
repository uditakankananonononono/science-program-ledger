import numpy as np, scanpy as sc, anndata as ad, json, warnings, scipy.sparse as sp
from sklearn.metrics import adjusted_rand_score as ARI, normalized_mutual_info_score as NMI
warnings.filterwarnings('ignore')
PANEL='CD3D CD3E IL7R CCR7 CD8A CD8B NKG7 GNLY MS4A1 CD79A CD14 LYZ FCGR3A MS4A7 FCER1A CST3 PPBP'.split()
a=ad.read_h5ad('data/pbmc3k_raw.h5ad'); a.var_names_make_unique()
sc.pp.filter_cells(a,min_genes=200); sc.pp.filter_genes(a,min_cells=3)
a.var['mt']=a.var_names.str.startswith('MT-'); sc.pp.calculate_qc_metrics(a,qc_vars=['mt'],inplace=True)
a=a[(a.obs.pct_counts_mt<5)&(a.obs.n_genes_by_counts<2500)].copy()
sc.pp.normalize_total(a,target_sum=1e4); sc.pp.log1p(a)
X=a.X.toarray() if sp.issparse(a.X) else np.asarray(a.X)
g={n:i for i,n in enumerate(a.var_names)}
Z={m:(X[:,g[m]]-X[:,g[m]].mean())/(X[:,g[m]].std()+1e-9) for m in PANEL if m in g}
def cs(ms): return np.mean([Z[m] for m in ms if m in Z],axis=0)
cls={'T':cs(['CD3D','CD3E','IL7R']),'NK':cs(['NKG7','GNLY']),'B':cs(['MS4A1','CD79A']),'CD14':cs(['CD14','LYZ']),'FCGR3A':cs(['FCGR3A','MS4A7']),'DC':cs(['FCER1A','CST3']),'Mega':cs(['PPBP'])}
cls['NK']=np.where(Z['CD3D']<0.5,cls['NK'],-9)
names=list(cls); M=np.column_stack([cls[n] for n in names]); o=np.argsort(-M,1)
top=M[np.arange(len(M)),o[:,0]]; sec=M[np.arange(len(M)),o[:,1]]
lab=np.where((top>=1.0)&(top-sec>=0.5),np.array(names)[o[:,0]],'NA')
mask=lab!='NA'; print('labeled',mask.sum(),'of',len(lab),{n:int((lab==n).sum()) for n in names},flush=True)
sc.pp.highly_variable_genes(a,n_top_genes=2000,flavor='seurat')
a.var.loc[[m for m in PANEL if m in g],'highly_variable']=False
z=(np.asarray((X[:,a.var.highly_variable.values]==0).mean(1)))
q=(np.argsort(np.argsort(z))/(len(z)-1))
b=a[:,a.var.highly_variable].copy(); sc.pp.scale(b,max_value=10); sc.tl.pca(b,n_comps=30,svd_solver='arpack',random_state=0)
sc.pp.neighbors(b,n_neighbors=15,n_pcs=30,random_state=0)
C0=b.obsp['connectivities'].tocsr().copy()
def reweight(p):
    C=C0.tocoo(); w=C.data*(1-np.abs(q[C.row]-q[C.col]))**p
    return sp.csr_matrix((w,(C.row,C.col)),shape=C0.shape)
def clus(Cmat,res,seed):
    b.obsp['connectivities']=Cmat; sc.tl.leiden(b,resolution=res,random_state=seed,flavor='leidenalg',key_added='l',directed=False,n_iterations=2)
    return b.obs['l'].astype(int).values
out={}
for res in (0.8,0.4,1.2):
    r=[]
    for s in range(20):
        lb=clus(C0,res,s); l0=clus(reweight(0),res,s); ld=clus(reweight(2),res,s)
        assert (lb==l0).all()
        r.append((ARI(lab[mask],lb[mask]),ARI(lab[mask],ld[mask]),NMI(lab[mask],lb[mask]),NMI(lab[mask],ld[mask]),len(set(lb)),len(set(ld))))
    r=np.array(r); d=r[:,1]-r[:,0]; rs=np.random.RandomState(7)
    bs=[d[rs.randint(0,20,20)].mean() for _ in range(10000)]; lo,hi=np.percentile(bs,[2.5,97.5])
    v='WIN' if d.mean()>=.02 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
    out[str(res)]=dict(ari_base=r[:,0].mean(),ari_dalr=r[:,1].mean(),diff=d.mean(),ci=[lo,hi],nmi_base=r[:,2].mean(),nmi_dalr=r[:,3].mean(),k_base=r[:,4].mean(),k_dalr=r[:,5].mean(),verdict=v if res==0.8 else 'sensitivity:'+v)
    print(res,json.dumps(out[str(res)],default=float),flush=True)
json.dump(out,open('results.json','w'),indent=1,default=float)
