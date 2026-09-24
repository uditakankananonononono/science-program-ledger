import anndata as ad, numpy as np, json, hashlib, gc
d=ad.read_h5ad('results/local/dev10k.h5ad')
f=ad.read_h5ad('results/local/frz5k.h5ad')
genes=[g for g in d.var_names if g in set(f.var_names)]
dpos=d.var_names.get_indexer(genes); fpos=f.var_names.get_indexer(genes)
pn_d=list(d.uns['protein_names']); pn_f=list(f.uns['protein_names'])
fidx=[pn_f.index(p) for p in pn_d]
Yd=np.log1p(np.asarray(d.obsm['protein_expression'], dtype=np.float32))
Yf=np.log1p(np.asarray(f.obsm['protein_expression'][:, fidx], dtype=np.float32))
rng=np.random.default_rng(17); n=d.shape[0]
perm=rng.permutation(n); ntr=int(n*0.8)
tr, te = np.sort(perm[:ntr]), np.sort(perm[ntr:])
# pass 1: chunked normalize dev-train rows to compute variance for HVG
s1=np.zeros(len(genes), np.float64); s2=np.zeros(len(genes), np.float64); cnt=0
def chunks(idxs, B=800):
    for i in range(0, len(idxs), B): yield idxs[i:i+B]
for c in chunks(tr):
    X=np.asarray(d.X[c][:, dpos], dtype=np.float32)
    lib=X.sum(1, keepdims=True); lib[lib==0]=1
    X=np.log1p(X/lib*1e4)
    s1+=X.sum(0); s2+=(X*X).sum(0); cnt+=X.shape[0]
    del X; gc.collect()
var=s2/cnt-(s1/cnt)**2
hv_rel=var.argsort()[::-1][:2000]; hv_rel=np.sort(hv_rel)
hv_abs=dpos[hv_rel]  # positions in original dev var order
# pass 2: write normalized HVG arrays
def write_norm(a, rows, colpos_abs, out):
    arr=np.zeros((len(rows), 2000), np.float32)
    w=0
    for c in chunks(rows):
        X=np.asarray(a.X[c][:, colpos_abs], dtype=np.float32)
        lib_full=None
        lib=np.asarray(a.X[c], dtype=np.float32).sum(1, keepdims=True)  # library over ALL genes
        lib[lib==0]=1
        arr[w:w+len(c)]=np.log1p(X/lib*1e4); w+=len(c)
        del X, lib; gc.collect()
    np.save(out, arr)
    return arr.shape
# frozen columns must map to the SAME genes: frozen positions of hv genes
hv_genes=[genes[i] for i in hv_rel]
fpos_hv=f.var_names.get_indexer(hv_genes)
print('shapes:', write_norm(d, tr, hv_abs, 'results/local/Xtr.npy'),
      write_norm(d, te, hv_abs, 'results/local/Xte.npy'),
      write_norm(f, np.arange(f.shape[0]), fpos_hv, 'results/local/Xfz.npy'))
np.save('results/local/Ytr.npy', Yd[tr]); np.save('results/local/Yte.npy', Yd[te]); np.save('results/local/Yfz.npy', Yf)
np.save('results/local/hv.npy', hv_rel)
json.dump({'proteins':pn_d,'genes_intersect':len(genes),'hvg':2000,'seed':17,
 'n_train':len(tr),'n_test':len(te),'n_frozen':f.shape[0]}, open('results/prep_spec.json','w'))
man={p: hashlib.sha256(open('results/local/'+p,'rb').read()).hexdigest()[:16]
     for p in ['Xtr.npy','Xte.npy','Ytr.npy','Yte.npy','Xfz.npy','Yfz.npy','hv.npy','dev10k.h5ad','frz5k.h5ad']}
json.dump({'hashes':man,'note':'all arrays hashed BEFORE any training/scoring'}, open('results/data_manifest.json','w'), indent=1)
print('done')
