import cellxgene_census, numpy as np, sys, json
sys.path.insert(0,'tool'); from fetch import COH
with cellxgene_census.open_soma(census_version="2025-11-08") as c:
    hs=c["census_data"]["homo_sapiens"]
    for cid in sys.argv[1:]:
        ds,dis,tis,assay=COH[cid]
        f=(f"cell_type == 'CD8-positive, alpha-beta T cell' and is_primary_data == True and dataset_id == '{ds}' and disease == '{dis}' and tissue_general == '{tis}' and assay == \"{assay}\"")
        obs=hs.obs.read(value_filter=f,column_names=["soma_joinid","donor_id","observation_joinid"]).concat().to_pandas()
        rng=np.random.default_rng(0)
        if len(obs)>2000: obs=obs.iloc[np.sort(rng.choice(len(obs),2000,replace=False))]
        obs.to_csv(f"data/{cid}_obs.csv",index=False); print(cid,len(obs),obs.donor_id.nunique(),flush=True)
    hs.ms["RNA"].var.read(value_filter="feature_type == 'protein_coding'",column_names=["soma_joinid","feature_name"]).concat().to_pandas().to_csv("data/pc_genes.csv",index=False)
