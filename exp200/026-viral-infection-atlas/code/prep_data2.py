import numpy as np, pandas as pd, json, cellxgene_census
from scipy.sparse import save_npz, diags
census=cellxgene_census.open_soma(census_version="2025-01-30")
full=census["census_info"]["datasets"].read().concat().to_pandas()
did=full[full['dataset_title'].str.contains('Immunophenotyping of COVID-19 and influenza', case=False, na=False)].iloc[0]['dataset_id']
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
sel=pd.concat(keep).sort_values('soma_joinid')
json.dump({'dataset_id':did,'cell_types':top6,'n_cells':int(len(sel)),'per_group_cap':600,'seed':7},
          open('results/subsample.json','w'), indent=1)
print('subsample', len(sel), flush=True)
genes=None; obs_rows=[]
for i,dis in enumerate(['COVID-19','influenza','normal']):
    ids=sel[sel['disease']==dis]['soma_joinid'].tolist()
    ad=cellxgene_census.get_anndata(census, organism='Homo sapiens',
        obs_value_filter=f"dataset_id == '{did}'", obs_coords=ids,
        var_column_names=['feature_name'], X_name='raw')
    X=ad.X.tocsr().astype(np.float32)
    lib=np.asarray(X.sum(1)).ravel(); lib[lib==0]=1
    X=diags(1/lib)@X; X.data*=1e4; np.log1p(X.data, out=X.data)
    save_npz(f'results/local/X_{i}.npz', X.tocsr())
    if genes is None: genes=ad.var['feature_name'].values
    obs_rows.append(sel[sel['disease']==dis])
    print(dis, X.shape, flush=True)
    del ad, X
np.save('results/local/genes.npy', genes)
pd.concat(obs_rows).to_csv('results/local/obs.csv', index=False)
print('done', flush=True)
