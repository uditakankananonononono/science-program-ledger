# PROVENANCE - DOC-1-027
- Data: Tabula Muris FACS Lung (mouse), raw count matrix + FACS annotations, from the Tabula Muris
  Consortium release (Nature 2018, PMID 30283141); local float32 matrices in
  exp200/022-cross-tissue-embedding/results/local/ (Lung_X.npy raw counts - verified integer-like;
  Lung_y.npy type labels; genes.npy 23433 genes), originally fetched from the public Tabula Muris
  figshare/10x release. No new download required.
- Baseline method: NNLS deconvolution as published in SPOTlight (Elosua-Bayes et al 2021, NAR 49:e50,
  PMID 33501959) and Stereoscope (Andersson et al 2020, Nat Commun 11:243, PMID 31924730).
- Reference design: DSTG (He et al 2021, "Deconvoluting spatial transcriptomics data through
  graph-based artificial intelligence", Brief Bioinform 22:bbaa414, PMID 33341842).
- Simulation approach: synthetic-mixture benchmarking as in CARD (Ma & Zhou 2022, Nat Biotechnol
  40:1377, PMID 35322228) with spatial structure added via Gaussian random field.
- Tools: numpy/scipy/scikit-learn/torch (CPU, 2 threads). No external services, no cost.
