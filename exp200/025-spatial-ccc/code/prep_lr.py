import numpy as np, pandas as pd, json
from scipy.io import mmread
prot=pd.read_csv('results/local/protein_input.csv')
u2g={}
for _,r in prot.iterrows():
    pn=str(r['protein_name'])
    if pn.endswith('_HUMAN'): u2g[str(r['uniprot'])]=pn[:-6].upper()
lr=pd.read_csv('results/local/interaction_input.csv')
pairs=[]
for _,r in lr.iterrows():
    ga,gb=u2g.get(str(r['partner_a'])),u2g.get(str(r['partner_b']))
    if ga and gb and ga!=gb: pairs.append((ga,gb))
pairs=sorted(set(pairs))
print('single-gene LR pairs:', len(pairs), flush=True)
lr_genes=sorted({g for p in pairs for g in p})
for name in ['Anterior','Posterior']:
    d=f'results/local/fbcm_{name}'
    M=mmread(f'{d}/matrix.mtx.gz').tocsr().T.tocsr()
    feats=pd.read_csv(f'{d}/features.tsv.gz', sep='\t', header=None, compression='gzip')
    genes=feats[1].values
    bc=pd.read_csv(f'{d}/barcodes.tsv.gz', header=None, compression='gzip')[0].values
    sp=pd.read_csv(f'results/local/spatial_{name}/spatial/tissue_positions_list.csv', header=None)
    sp.columns=['barcode','in_tissue','array_row','array_col','px_row','px_col']
    keep=(sp.set_index('barcode').reindex(bc)['in_tissue'].values==1)
    M=M[keep]
    lib=np.asarray(M.sum(1)).ravel().astype(np.float32); lib[lib==0]=1
    X=M.multiply(1/lib[:,None]).multiply(1e4).tocsr(); X.data=np.log1p(X.data)
    X=X.astype(np.float32)
    gidx={str(g2).upper(): i for i,g2 in enumerate(genes)}
    cols=[(gidx[g2], g2) for g2 in lr_genes if g2 in gidx]
    XL=np.zeros((X.shape[0], len(cols)), np.float32)
    for j,(gi,_) in enumerate(cols):
        XL[:,j]=X[:,gi].toarray().ravel()
    np.save(f'results/local/{name}_Xlr.npy', XL)
    np.save(f'results/local/{name}_lrgenes.npy', np.array([c[1] for c in cols]))
    print(name,'lr genes present:', len(cols), flush=True)
    del M,X,XL
json.dump(pairs, open('results/lr_pairs.json','w'), indent=1)
print('lr_pairs.json', len(pairs))
