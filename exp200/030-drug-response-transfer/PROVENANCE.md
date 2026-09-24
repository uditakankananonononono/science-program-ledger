# PROVENANCE - DOC-1-030
- scRNA: Gambardella, Viscido et al 2022, "A single-cell analysis of breast cancer cell lines to
  study tumour heterogeneity and drug response", Nat Commun 13:2394 (PMID 35513312). Raw UMI
  MatrixMarket files: figshare article 15022698 (files 30469062 matrix.mtx.gz, 30469065
  barcodes.tsv.gz, 30469068 features.tsv.gz). GEO mirror GSE173634.
- Bulk expression + potency: Cross-Study Analysis (CSA) benchmark, Zenodo record 15258883
  (csa_data.zip): x_data/cancer_gene_expression.tsv (IMPROVE/CCLE), y_data/response.tsv
  (sources CCLE/CTRPv2/gCSI/GDSCv1/GDSCv2; fields include auc; improve IDs), x_data/drug_info.tsv
  (lapatinib=Drug_435, afatinib=Drug_520). Line ID mapping: DepMap 23Q4 Public, figshare article
  24667905, Model.csv (file 43746708).
- Named baseline: the source paper's cognate-target-expression biomarker and its published PCC
  values (Nat Commun source data, Supp Dataset 02, MOESM4: lapatinib CTRPv2 -0.395 / GDSC -0.423;
  afatinib CTRPv2 -0.530 / GDSC -0.716); DREEP is the paper's per-cell method (P1 reference).
- Tools: numpy/pandas/scipy/scikit-learn (CPU). No cost, no restricted data.
