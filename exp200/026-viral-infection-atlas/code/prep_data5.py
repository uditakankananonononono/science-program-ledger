import numpy as np, pandas as pd, json, gc, os, cellxgene_census
from scipy.sparse import save_npz, load_npz, diags, vstack
census=cellxgene_census.open_soma(census_version="2025-01-30")
full=census["census_info"]["datasets"].read().concat().to_pandas()
did=full[full['dataset_title'].str.contains('Immunophenotyping of COVID-19 and influenza', case=False, na=False)].iloc[0]['dataset_id']
sel_path='results/local/sel.csv'
if os.path.exists(sel_path):
    sel=pd.read_csv(sel_path)
else:
    obs=census["census_data"]["homo_sapiens"].obs
    df=obs.read(value_filter=f"dataset_id == '{did}'", column_names=['soma_joinid','disease','cell_type']).concat().to_pandas()
    df['disease']=df['disease'].astype(str); df['cell_type']=df['cell_type'].astype(str)
    top6=df['cell_type'].value_counts().head(6).index.tolist()
    rng=np.random.default_rng(7)
    keep=[]
    for dis in ['COVID-19','influenza','normal']:
        for ct in top6:
            sub=df[(df['disease']==dis)&(df['cell_type']==ct)]['soma_joinid'].values
            if len(sub)>600: sub=rng.choice(sub,600,replace=False)
            keep.append(pd.DataFrame({'soma_joinid':sub,'disease':dis,'cell_type':ct}))
    sel=pd.concat(keep).sort_values('soma_joinid').reset_index(drop=True)
    sel.to_csv(sel_path, index=False)
    json.dump({'dataset_id':did,'cell_types':top6,'n_cells':int(len(sel)),'per_group_cap':600,'seed':7},
              open('results/subsample.json','w'), indent=1)
ids=sel['soma_joinid'].tolist()
print('subsample', len(ids), flush=True)
B=100
n_chunks=(len(ids)+B-1)//B
genes=None
for ci in range(n_chunks):
    p=f'results/local/chunks/chunk_{ci}.npz'
    if os.path.exists(p): continue
    ad=cellxgene_census.get_anndata(census, organism='Homo sapiens',
        obs_value_filter=f"dataset_id == '{did}'", obs_coords=ids[ci*B:(ci+1)*B],
        var_column_names=['feature_name'], X_name='raw')
    X=ad.X.tocsr().astype(np.float32)
    lib=np.asarray(X.sum(1)).ravel(); lib[lib==0]=1
    X=diags(1/lib)@X; X.data*=1e4; np.log1p(X.data, out=X.data)
    save_npz(p, X.tocsr())
    if genes is None:
        np.save('results/local/genes.npy', ad.var['feature_name'].values)
    del ad, X; gc.collect()
    print('chunk', ci, flush=True)
print('ALL_CHUNKS_DONE', flush=True)
