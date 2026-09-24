"""Pull selected CD8 rows from CELLxGENE source h5ad files over S3 range reads (fits in <1 GB RAM)."""
import s3fs, h5py, numpy as np, pandas as pd, scipy.sparse as sp, sys, cellxgene_census
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'tool'); from fetch import COH
fs=s3fs.S3FileSystem(anon=True)
def opn(uri): return h5py.File(fs.open(uri,"rb",block_size=256*1024,cache_type="none"),"r")
def decode(g):
    if isinstance(g,h5py.Group): 
        cats=g["categories"][:]; codes=g["codes"][:]; cats=np.array([c.decode() if isinstance(c,bytes) else c for c in cats],dtype=object); return cats[codes]
    v=g[:]; return np.array([x.decode() if isinstance(x,bytes) else x for x in v],dtype=object)
cid=sys.argv[1]; ds=COH[cid][0]
uri=cellxgene_census.get_source_h5ad_uri(ds,census_version="2025-11-08")["uri"]
sel=pd.read_csv(f"data/{cid}_obs.csv")
f=opn(uri)
oj=f["obs"]["observation_joinid"]; oj=decode(oj)
pos=pd.Series(np.arange(len(oj)),index=oj)
rows=np.sort(pos.loc[sel.observation_joinid.astype(str)].values)
G=f["raw/X"] if "raw/X" in f else f["X"]; vg=f["raw/var"] if "raw/X" in f else f["var"]
names=decode(vg["feature_name"]) if "feature_name" in vg else decode(vg["_index"])
indptr=G["indptr"][:]
pc=set(pd.read_csv("data/pc_genes.csv").feature_name)
f.close()
def work(chunk):
    h=opn(uri); g=h["raw/X"] if "raw/X" in h else h["X"]; out=[]
    for r in chunk:
        a,b=indptr[r],indptr[r+1]; out.append((g["indices"][a:b],g["data"][a:b]))
    h.close(); return out
chunks=np.array_split(rows,12)
with ThreadPoolExecutor(12) as ex: res=[x for part in ex.map(work,chunks) for x in part]
ind=[r[0] for r in res]; dat=[r[1] for r in res]; ptr=np.concatenate([[0],np.cumsum([len(i) for i in ind])])
X=sp.csr_matrix((np.concatenate(dat).astype(np.float32),np.concatenate(ind),ptr),shape=(len(rows),len(names)))
keepg=np.array([n in pc for n in names]); X=X[:,keepg]; names=names[keepg]
k2=np.asarray((X>0).mean(0)).ravel()>=0.01
sp.save_npz(f"data/{cid}.npz",X[:,k2]); np.save(f"data/{cid}_genes.npy",names[k2].astype(str))
donor=sel.set_index(sel.observation_joinid.astype(str)).loc[oj[rows],"donor_id"].astype(str).values
np.save(f"data/{cid}_donor.npy",donor)
print(cid,X[:,k2].shape,"maxval",X.data.max() if X.nnz else 0,flush=True)
