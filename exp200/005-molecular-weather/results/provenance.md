# Provenance - DOC-1-005
- Data: Paul et al. 2015 (Cell, "Transcriptional Heterogeneity and Lineage Commitment in
  Myeloid Progenitors"), MARS-seq umitab.
  URL: https://ftp.ncbi.nlm.nih.gov/geo/series/GSE72nnn/GSE72857/suppl/GSE72857_umitab.txt.gz
  SHA-256: 6f45b72b... (full hash recorded at download time 2026-09-23; file 16,413,252 bytes)
  Companion: https://ftp.ncbi.nlm.nih.gov/geo/series/GSE72nnn/GSE72857/suppl/GSE72857_experimental_design.txt.gz
- Code: code/analysis_v2_staged.py (staged loader for 2GB RAM envelope; parses umitab in
  3 row-chunks to /tmp, float32 sub-blocking), code/fate_forecast.py (CLI).
  code/analysis.py + analysis_v2.py = original single-shot versions (kept for audit;
  they exceed the foreground time/memory envelope on this container).
- Gates: GATES.md (v1), GATES_v2.md (trained-model arm amendment). SHA-256 in each file header.
- Model artifact: results/fate_forecast_model.joblib (MLPClassifier + PCA + gene panel).
- Seeds: rng 20260923; PCA/KMeans/MLP random_state fixed. Deterministic rerun.
