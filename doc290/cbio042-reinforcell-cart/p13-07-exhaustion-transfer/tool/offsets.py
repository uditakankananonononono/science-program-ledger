"""Census soma_joinid is contiguous per dataset in source-h5ad row order (verified constant offset on C02/C03/C06/C10);
store the per-dataset minimum soma_joinid so large files skip the slow remote observation_joinid scan."""
import cellxgene_census, sys
sys.path.insert(0,'tool'); from fetch import COH
with cellxgene_census.open_soma(census_version="2025-11-08") as c:
    hs=c["census_data"]["homo_sapiens"]
    for cid in sys.argv[1:]:
        o=hs.obs.read(value_filter=f"dataset_id == '{COH[cid][0]}'",column_names=["soma_joinid"]).concat().to_pandas()
        open(f"data/{cid}_offset.txt","w").write(str(int(o.soma_joinid.min()))); print(cid,o.soma_joinid.min(),len(o))
