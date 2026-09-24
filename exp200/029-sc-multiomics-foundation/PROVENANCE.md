# PROVENANCE - DOC-1-029
- DEV: https://exampledata.scverse.org/scvi-tools/pbmc_10k_protein_v3.h5ad (24.9MB, fetched
  2026-09-24) - 10x Genomics 3' v3 CITE-seq PBMC, processed per totalVI (Gayoso et al 2021,
  Nat Methods 18:1209-1220, PMID 33723406).
- FROZEN: https://exampledata.scverse.org/scvi-tools/pbmc_5k_protein_v3.h5ad (18.3MB) - same
  processing, independent donor; the totalVI paper's two-dataset benchmark pair.
- Named baseline: ridge on HVGs, the documented simple baseline of the NeurIPS 2021 Multimodal
  Single-Cell Integration competition (Luecken et al 2022, NeurIPS 35 Datasets & Benchmarks)
  and totalVI benchmark supplements.
- Protocol reference: masked self-supervised pretraining + linear probe (scBERT/Geneformer
  family); here at 2-CPU/1.9GB envelope scale, disclosed as such.
- Tools: anndata 0.11.4, numpy, scikit-learn, torch (CPU, 2 threads). No cost.
