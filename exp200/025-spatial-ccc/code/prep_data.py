import numpy as np, pandas as pd, json
from scipy.io import mmread
import igraph as ig, leidenalg
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors

prot=pd.read_csv('results/local/protein_input.csv')
u2g={}
for _,r in prot.iterrows():
    g=str(r.get('gene_name',''))
    if g and g!='nan': u2g[str(r['uniprot'])]=g.upper()
lr=pd.read_csv('results/local/interaction_input.csv')
pairs=[]
for _,r in lr.iterrows():
    ga,gb=u2g.get(str(r['partner_a'])),u2g.get(str(r['partner_b']))
    if ga and gb and ga!=gb: pairs.append((ga,gb))
pairs=sorted(set(pairs))
print('single-gene LR pairs:', len(pairs), flush=True)

def load_section(name):
    d=f'results/local/fbcm_{name}'
    M=mmread(f'{d}/matrix.mtx.gz').tocsr().T.tocsr()
    feats=pd.read_csv(f'{d}/features.tsv.gz', sep='\t', header=None, compression='gzip')
    genes=feats[1].values
    bc=pd.read_csv(f'{d}/barcodes.tsv.gz', header=None, compression='gzip')[0].values
    sp=pd.read_csv(f'results/local/spatial_{name}/spatial/tissue_positions_list.csv', header=None)
    sp.columns=['barcode','in_tissue','array_row','array_col','px_row','px_col']
    sp=sp.set_index('barcode').reindex(bc)
    keep=(sp['in_tissue'].values==1)
    return M[keep], genes, sp[keep]

lr_genes=sorted({g for p in pairs for g in p})
for name in ['Anterior','Posterior']:
    M, genes, sp = load_section(name)
    lib=np.asarray(M.sum(1)).ravel().astype(np.float32); lib[lib==0]=1
    X=M.multiply(1/lib[:,None]).multiply(1e4).tocsr(); X.data=np.log1p(X.data)
    X=X.astype(np.float32)
    P=TruncatedSVD(n_components=30, random_state=7).fit_transform(X)
    nn=NearestNeighbors(n_neighbors=11).fit(P); _,I=nn.kneighbors(P)
    n=X.shape[0]; edges=[(i,j) for i in range(n) for j in I[i,1:]]
    g=ig.Graph(n=n, edges=edges).simplify()
    part=leidenalg.find_partition(g, leidenalg.RBConfigurationVertexPartition, resolution_parameter=1.0, seed=7)
    cl=np.array(part.membership)
    gidx={str(g2).upper(): i for i,g2 in enumerate(genes)}
    cols=[(gidx[g2], g2) for g2 in lr_genes if g2 in gidx]
    XL=np.zeros((n, len(cols)), np.float32)
    for j,(gi,_) in enumerate(cols):
        XL[:,j]=X[:,gi].toarray().ravel()
    np.save(f'results/local/{name}_Xlr.npy', XL)
    np.save(f'results/local/{name}_lrgenes.npy', np.array([c[1] for c in cols]))
    np.save(f'results/local/{name}_cl.npy', cl)
    sp.reset_index().to_csv(f'results/local/{name}_coords.csv', index=False)
    json.dump({'n_spots':int(n),'n_clusters':int(cl.max()+1),'lr_genes_present':len(cols)},
              open(f'results/clusters_{name}.json','w'), indent=1)
    print(name,'spots',n,'clusters',cl.max()+1,'lr genes',len(cols), flush=True)
    del M,X,P
json.dump(pairs, open('results/lr_pairs.json','w'), indent=1)
print('lr_pairs.json written', len(pairs))
