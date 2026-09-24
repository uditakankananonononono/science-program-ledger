import numpy as np, pandas as pd, json, cellxgene_census
census=cellxgene_census.open_soma(census_version="2025-01-30")
full=census["census_info"]["datasets"].read().concat().to_pandas()
did=full[full['dataset_title'].str.contains('Immunophenotyping of COVID-19 and influenza', case=False, na=False)].iloc[0]['dataset_id']
obs=census["census_data"]["homo_sapiens"].obs
df=obs.read(value_filter=f"dataset_id == '{did}'", column_names=['soma_joinid','disease','cell_type']).concat().to_pandas()
df['disease']=df['disease'].astype(str); df['cell_type']=df['cell_type'].astype(str)
top6=df['cell_type'].value_counts().head(6).index.tolist()
print('top6', top6, flush=True)
rng=np.random.default_rng(7)
keep=[]
for dis in ['COVID-19','influenza','normal']:
    for ct in top6:
        sub=df[(df['disease']==dis)&(df['cell_type']==ct)]['soma_joinid'].values
        if len(sub)>1200: sub=rng.choice(sub,1200,replace=False)
        keep.append(sub)
ids=np.sort(np.concatenate(keep))
json.dump({'dataset_id':did,'cell_types':top6,'n_cells':int(len(ids)),
           'per_group_cap':1200,'seed':7}, open('results/subsample.json','w'), indent=1)
print('subsample', len(ids), flush=True)
ad=cellxgene_census.get_anndata(census, organism='Homo sapiens',
    obs_value_filter=f"dataset_id == '{did}'", obs_coords=ids.tolist(),
    var_column_names=['feature_name'], X_name='raw')
print(ad, flush=True)
from scipy.sparse import save_npz
X=ad.X.tocsr().astype(np.float32)
lib=np.asarray(X.sum(1)).ravel(); lib[lib==0]=1
from scipy.sparse import diags
X=diags(1/lib)@X; X.data*=1e4; np.log1p(X.data, out=X.data)
save_npz('results/local/X_lognorm.npz', X.tocsr())
np.save('results/local/genes.npy', ad.var['feature_name'].values)
ad.obs[['disease','cell_type']].to_csv('results/local/obs.csv')
print('saved', X.shape, flush=True)
