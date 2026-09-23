# Provenance (PPD-v2)
- GSE44132 series matrix (discovery): https://ftp.ncbi.nlm.nih.gov/geo/series/GSE44nnn/GSE44132/matrix/GSE44132_series_matrix.txt.gz
  SHA-256 b2d715ec45c250426c8b2a4e5317bf589f581f8425d1101d9f6d752ba6dc19b9 (450K betas, 55 samples, 23 PPD/32 no, 5 array batches)
- HM450 probe annotation (Zhou lab InfiniumAnnotation, gencode v22, hg38): https://zhouserver.research.chop.edu/InfiniumAnnotation/current/HM450/HM450.hg38.manifest.gencode.v22.tsv.gz
  SHA-256 bd675db87cbba861a9178fc5caa0d483ac06cd7ba8f5cac3a25401602daa6a6d
- Cohort scouting (documented negatives): GSE43460 mouse, GSE114685 neurons, GSE153934 mouse adipose,
  GSE179393 cardiac, GSE35141 cancer, GSE98203 heroin brain, GSE192918 no depression labels,
  GSE32528/GSE43462/GSE41826 brain/methods, GSE201287 MDD blood idat-only (G3 transport cohort, not run - see README).
## G3 transport cohort (follow-up)
- GSE201287 series matrix (labels): https://ftp.ncbi.nlm.nih.gov/geo/series/GSE201nnn/GSE201287/matrix/GSE201287_series_matrix.txt.gz
  SHA-256 0b14f16843b6ac2ca5c2466c2a3101593c44dd024217c8e454a70c6e8bbe3c0d
- GSE201287 normalized matrix (AVG_Beta): https://ftp.ncbi.nlm.nih.gov/geo/series/GSE201nnn/GSE201287/suppl/GSE201287_matrix_norm.txt.gz
  SHA-256 fe7d172ab1e5d4f8a72e129fdde41fd928509d5b7ea5e1d3e1e3bb5cd89cfed5
- GSE201287 filelist (GSM<->barcode map): https://ftp.ncbi.nlm.nih.gov/geo/series/GSE201nnn/GSE201287/suppl/filelist.txt
  SHA-256 6916fb1ba57f6b5d27628e73aac28a819f93ced5fc16e1129c3131891eafb030
- GPL13534.annot.gz is a 990-byte stub on NCBI; GPL13534 family soft is ~230GB -> Zhou manifest substituted (GATES.addendum1.md).
- No other public PPD blood methylation cohort with labels found in GEO (eSearch, 2026-09-24).
