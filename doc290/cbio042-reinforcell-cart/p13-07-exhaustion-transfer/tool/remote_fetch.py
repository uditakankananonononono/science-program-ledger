"""Resumable pull of selected CD8 rows from CELLxGENE source h5ad files over S3 range reads.
Stage 1 caches row positions + indptr bounds; stage 2 fetches rows in parts of 100 (skips done parts);
stage 3 assembles once every part exists. Safe to re-run until it prints DONE."""
import s3fs, h5py, numpy as np, pandas as pd, scipy.sparse as sp, sys, os, time, cellxgene_census
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'tool'); from fetch import COH
fs=s3fs.S3FileSystem(anon=True)
def opn(uri): return h5py.File(fs.open(uri,"rb",block_size=1024**2,cache_type="blockcache"),"r")
def decode(g):
    if isinstance(g,h5py.Group):
        cats=g["categories"][:]; codes=g["codes"][:]; cats=np.array([c.decode() if isinstance(c,bytes) else c for c in cats],dtype=object); return cats[codes]
    v=g[:]; return np.array([x.decode() if isinstance(x,bytes) else x for x in v],dtype=object)
def xg(h): return h["raw/X"] if "raw/X" in h else h["X"]
cid=sys.argv[1]; budget=float(sys.argv[2]) if len(sys.argv)>2 else 90; t0=time.time()
uri=cellxgene_census.get_source_h5ad_uri(COH[cid][0],census_version="2025-11-08")["uri"]
meta=f"data/{cid}_meta.npz"
if not os.path.exists(meta):
    sel=pd.read_csv(f"data/{cid}_obs.csv"); f=opn(uri)
    offp=f"data/{cid}_offset.txt"
    if os.path.exists(offp):
        sel=sel.sort_values("soma_joinid"); rows=sel.soma_joinid.values-int(open(offp).read())
        ojd=f["obs"]["observation_joinid"]; ojd=ojd["codes"] if isinstance(ojd,h5py.Group) else ojd
        for i in np.random.default_rng(1).choice(len(rows),5,replace=False):  # spot-check the offset mapping
            v=f["obs"]["observation_joinid"][rows[i]]; v=v.decode() if isinstance(v,bytes) else v
            assert v==str(sel.observation_joinid.values[i]), ("offset mismatch",v)
        oj=None
    else:
        oj=decode(f["obs"]["observation_joinid"]); pos=pd.Series(np.arange(len(oj)),index=oj)
        rows=np.sort(pos.loc[sel.observation_joinid.astype(str)].values)
    vg=f["raw/var"] if "raw/X" in f else f["var"]
    names=decode(vg["feature_name"]) if "feature_name" in vg else decode(vg["_index"])
    ip=xg(f)["indptr"]; a=np.array([ip[r] for r in rows]) if len(ip)>5_000_000 else ip[:][rows]; b=ip[:][rows+1]
    donor=sel.donor_id.astype(str).values if oj is None else sel.set_index(sel.observation_joinid.astype(str)).loc[oj[rows],"donor_id"].astype(str).values
    np.savez(meta,rows=rows,a=a,b=b,names=names.astype(str),donor=donor); f.close(); print("meta saved",time.time()-t0,flush=True)
m=np.load(meta,allow_pickle=True); A,B=m["a"],m["b"]; n=len(A); parts=range(0,n,100)
def work(k):
    p=f"data/{cid}_part{k:05d}.npz"
    if os.path.exists(p) or time.time()-t0>budget: return
    h=opn(uri); g=xg(h); ind=[];dat=[]
    for i in range(k,min(k+100,n)): ind.append(g["indices"][A[i]:B[i]]); dat.append(g["data"][A[i]:B[i]])
    h.close(); np.savez(p+".tmp.npz",ind=np.array(ind,dtype=object),dat=np.array(dat,dtype=object)); os.replace(p+".tmp.npz",p)
with ThreadPoolExecutor(10) as ex: list(ex.map(work,parts))
done=[os.path.exists(f"data/{cid}_part{k:05d}.npz") for k in parts]
print(cid,f"{sum(done)}/{len(done)} parts",flush=True)
if all(done):
    ind=[];dat=[]
    for k in parts:
        z=np.load(f"data/{cid}_part{k:05d}.npz",allow_pickle=True); ind+=list(z["ind"]); dat+=list(z["dat"])
    names=m["names"]; ptr=np.concatenate([[0],np.cumsum([len(i) for i in ind])])
    X=sp.csr_matrix((np.concatenate(dat).astype(np.float32),np.concatenate(ind),ptr),shape=(n,len(names)))
    pc=set(pd.read_csv("data/pc_genes.csv").feature_name); kg=np.array([x in pc for x in names]); X=X[:,kg]; names=names[kg]
    k2=np.asarray((X>0).mean(0)).ravel()>=0.01
    sp.save_npz(f"data/{cid}.npz",X[:,k2]); np.save(f"data/{cid}_genes.npy",names[k2]); np.save(f"data/{cid}_donor.npy",m["donor"])
    for k in parts: os.remove(f"data/{cid}_part{k:05d}.npz")
    print("DONE",cid,X[:,k2].shape,flush=True)
