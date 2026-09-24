# PROVENANCE - DOC-1-028
- Dataset: GSE284989, "Spatial genomics reveals cholesterol metabolism as a key factor in
  immunotherapy resistance in colorectal cancer" (GEO, 2025; OmicsDI record
  https://www.omicsdi.org/dataset/geo/GSE284989). 10x Visium, 16 MC38 tumors, 48,636 spots.
  Response = immune infiltration level after 5-day aPD1 (paper's definition).
- Files: per-sample filtered_feature_bc_matrix.h5 + tissue_positions_list.csv.gz from
  ftp.ncbi.nlm.nih.gov/geo/samples/GSM8694nnn/<GSM>/suppl/ (fetched 2026-09-24); series metadata
  from GSE284989_family.soft.gz (SOFT); file inventory from GSE284989 suppl filelist.txt.
- Labels: aPD1_NR (m09-m14) / aPD1_R (m15, m16) parsed from GEO sample titles; multi-section
  mice: m15 x2, m16 x3 sections; m04 (IgG) x3 sections + base_protocol variant (not gated).
- Named published baseline: the source paper's own bulk RNA-seq comparison (bulk detected immune
  correlates of response but lacked sensitivity for cholesterol synthesis - replicated here as F2).
- Gene lists: HALLMARK_CHOLESTEROL_HOMEOSTASIS core enzymes (MSigDB), cytotoxic T markers; mouse
  symbols verified present in the m09 matrix before gate lock (08:15).
- Tools: h5py/numpy/scipy/pandas (CPU). No cost, no restricted data.
