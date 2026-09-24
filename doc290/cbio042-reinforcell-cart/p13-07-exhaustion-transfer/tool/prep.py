"""P13-07 stage 1: normalize, HVG panel, L1/L2 labels, L1-vs-L2 kappa."""
import numpy as np, scipy.sparse as sp, json, sys, os, warnings; warnings.filterwarnings("ignore")
import scanpy as sc, anndata as an
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, cohen_kappa_score
sys.path.insert(0,'tool'); from fetch import COH
EXH=["PDCD1","HAVCR2","LAG3","TIGIT","CTLA4","TOX","ENTPD1","CXCL13","LAYN"]
PLAT=lambda a:"smartseq" if "Smart" in a else "bd" if "BD" in a else "10x5" if "5'" in a else "10x3" if "3'" in a else "multiome"
DCLASS={"COVID-19":"viral","B-cell non-Hodgkin lymphoma":"lymphoma"}
rng=np.random.default_rng(0)
cids=[c for c in sorted(COH) if os.path.exists(f"data/{c}.npz")]
print("cohorts",cids,flush=True)
A={}
for c in cids:
    X=sp.load_npz(f"data/{c}.npz"); g=np.load(f"data/{c}_genes.npy",allow_pickle=True).astype(str)
    ad=an.AnnData(X.tocsr().astype(np.float32)); ad.var_names=g; ad.var_names_make_unique()
    sc.pp.normalize_total(ad,target_sum=1e4); sc.pp.log1p(ad)
    sc.pp.highly_variable_genes(ad,n_top_genes=2000,flavor="seurat"); A[c]=ad
# feature panel
from collections import Counter
cnt=Counter(g for c in cids for g in A[c].var_names[A[c].var.highly_variable])
common=set.intersection(*[set(A[c].var_names) for c in cids])
panel=sorted(g for g,k in cnt.items() if k>=3 and g in common and g not in EXH)
exh_ok=[g for g in EXH if all(g in A[c].var_names for c in cids)]
info={"cohorts":cids,"panel_size":len(panel),"exh_genes_used":exh_ok}
lab={};feat={};kap={}
for c in cids:
    ad=A[c]; Z=ad[:,exh_ok].X.toarray(); Z=(Z-Z.mean(0))/(Z.std(0)+1e-9); s=Z.mean(1)
    lo,hi=np.quantile(s,[1/3,2/3]); L1=np.full(len(s),-1); L1[s<=lo]=0; L1[s>=hi]=1
    b=ad[:,ad.var.highly_variable].copy(); sc.pp.scale(b,max_value=10); sc.tl.pca(b,n_comps=30); sc.pp.neighbors(b); sc.tl.leiden(b,resolution=1.0,random_state=0,flavor="igraph",n_iterations=2,directed=False)
    cl=b.obs.leiden.values; cm={k:s[cl==k].mean() for k in np.unique(cl)}; v=np.array(sorted(cm.values())); t1,t2=np.quantile(v,[1/3,2/3])
    L2=np.array([1 if cm[k]>=t2 else 0 if cm[k]<=t1 else -1 for k in cl])
    m=(L1>=0)&(L2>=0); kap[c]=float(cohen_kappa_score(L1[m],L2[m])) if m.sum()>20 and len(set(L1[m]))>1 and len(set(L2[m]))>1 else None
    lab[c]={"L1":L1,"L2":L2}; feat[c]=ad[:,panel].X.toarray().astype(np.float32)
np.savez("results/prep.npz",**{f"F_{c}":feat[c] for c in cids},**{f"L1_{c}":lab[c]["L1"] for c in cids},**{f"L2_{c}":lab[c]["L2"] for c in cids})
json.dump(dict(info=info,kappa=kap,panel=panel),open("results/prep_info.json","w"),indent=1)
print(json.dumps(info),json.dumps(kap))
