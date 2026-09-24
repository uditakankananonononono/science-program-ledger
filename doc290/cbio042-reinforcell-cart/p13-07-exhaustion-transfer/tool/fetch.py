"""Fetch CD8 T-cell cohorts from CELLxGENE Census 2025-11-08 (one at a time, 1 GB RAM safe)."""
import tiledbsoma as soma, cellxgene_census, numpy as np, scipy.sparse as sp, json, sys, os
COH = {
 "C01":("5af90777-6760-4003-9dba-8f945fec6fdf","nonpapillary renal cell carcinoma","kidney","10x 5' transcription profiling"),
 "C02":("1e6a6ef9-7ec9-4c90-bbfb-2ad3c3165fd1","lung adenocarcinoma","lung","10x 3' v2"),
 "C03":("1e6a6ef9-7ec9-4c90-bbfb-2ad3c3165fd1","lung adenocarcinoma","lung","BD Rhapsody Whole Transcriptome Analysis"),
 "C04":("1e6a6ef9-7ec9-4c90-bbfb-2ad3c3165fd1","lung adenocarcinoma","lung","Smart-seq2"),
 "C05":("1e6a6ef9-7ec9-4c90-bbfb-2ad3c3165fd1","squamous cell lung carcinoma","lung","10x 3' v2"),
 "C06":("16023185-de21-4c0d-a9c8-73abdd52d142","colon adenocarcinoma","large intestine","10x 3' v2"),
 "C07":("9f222629-9e39-47d0-b83f-e08d610c7479","lung adenocarcinoma","lung","10x 3' v2"),
 "C08":("9fddb063-056d-4202-8b8a-4b0ee531d3ce","invasive ductal breast carcinoma","breast","10x 5' v1"),
 "C09":("b6b5ea88-e092-46e4-b9c5-e93b52d5c195","oropharynx squamous cell carcinoma","digestive system","10x 3' v3"),
 "C10":("67b6b9ac-b841-42ce-b2d4-ed2ec12327bd","B-cell non-Hodgkin lymphoma","lymph node","10x multiome"),
 "C11":("9dbab10c-118d-496b-966a-67f1763a6b7d","COVID-19","blood","10x 5' v2"),
}
CAP=4000
def main(ids):
    ctx=cellxgene_census.get_default_soma_context(tiledb_config={"soma.init_buffer_bytes":32*1024**2,"sm.memory_budget":256*1024**2,"sm.memory_budget_var":256*1024**2,"sm.mem.total_budget":512*1024**2})
    with cellxgene_census.open_soma(census_version="2025-11-08",context=ctx) as c:
        hs=c["census_data"]["homo_sapiens"]
        pc=hs.ms["RNA"].var.read(value_filter="feature_type == 'protein_coding'",column_names=["soma_joinid","feature_name"]).concat().to_pandas(); print("genes",len(pc),flush=True)
        for cid in ids:
            out=f"data/{cid}.npz"
            if os.path.exists(out): continue
            ds,dis,tis,assay=COH[cid]
            f=(f"cell_type == 'CD8-positive, alpha-beta T cell' and is_primary_data == True and dataset_id == '{ds}' "
               f"and disease == '{dis}' and tissue_general == '{tis}' and assay == \"{assay}\"")
            obs=hs.obs.read(value_filter=f,column_names=["soma_joinid","donor_id"]).concat().to_pandas()
            rng=np.random.default_rng(0)
            if len(obs)>CAP: obs=obs.iloc[np.sort(rng.choice(len(obs),CAP,replace=False))]
            print(cid,"obs",len(obs),flush=True)
            Xarr=hs.ms["RNA"].X["raw"]; vid=pc.soma_joinid.values; vmap=np.full(int(vid.max())+1,-1); vmap[vid]=np.arange(len(vid))
            oid=obs.soma_joinid.values; omap={o:i for i,o in enumerate(oid)}
            rows=[];cols=[];vals=[]
            for k in range(0,len(oid),250):
                for tb in Xarr.read(coords=(oid[k:k+250],vid)).tables():
                    d=tb.to_pydict(); rows+= [omap[o] for o in d["soma_dim_0"]]; cols+=list(vmap[np.array(d["soma_dim_1"])]); vals+=d["soma_data"]
            X=sp.csr_matrix((np.array(vals,dtype=np.float32),(np.array(rows),np.array(cols))),shape=(len(oid),len(vid)))
            del rows,cols,vals
            class A: pass
            ad=A(); ad.X=X
            import pandas as pd
            ad.var=pd.DataFrame({"feature_name":pc.feature_name.values}); ad.obs=obs.reset_index(drop=True)
            X=sp.csr_matrix(ad.X); keep=np.asarray((X>0).mean(0)).ravel()>=0.01
            X=X[:,keep]; genes=ad.var.feature_name.values[keep]
            sp.save_npz(out,X); np.save(f"data/{cid}_genes.npy",genes)
            np.save(f"data/{cid}_donor.npy",ad.obs.donor_id.astype(str).values)
            print(cid,X.shape,ad.obs.donor_id.nunique(),flush=True)
if __name__=="__main__": main(sys.argv[1:] or list(COH))
