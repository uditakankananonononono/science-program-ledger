# PROVENANCE (started 2026-09-24, LOCKED with GATES before outcomes)
- figshare 5715040 (Tabula Muris FACS Smart-seq2): FACS.zip member Pancreas-counts.csv
  (re-extract; sha256_16 cff5ce3901636b1e per 022 provenance), annotations_FACS.csv (file 10039267).
- figshare 5715025 (Tabula Muris droplet 10x): droplet.zip member Pancreas-counts.csv,
  annotations_droplets.csv (file 10039264).
- Schaum, Karkanias et al. 2018, Nature 562:367-372.
- Baseline pipeline: Wolf et al 2018 Genome Biol 19:15; Traag et al 2019 Sci Rep 9:5233.
- Contrastive reference: Chen et al 2020 ICML (SimCLR) - adapted to scRNA, no claim of reproducing scCL.

## Addendum A cohort (2026-09-24 07:42)
- droplet.zip (figshare 5715025) inspected: NO Pancreas members - frozen cohort replaced per Addendum A.
- scIB integration task h5ad: human_pancreas_norm_complexBatch.h5ad, figshare file 24539828,
  315,955,785B (downloaded). Frozen cohort = smartseq2 study (Segerstolpe 2016): gamma 213 cells,
  background 2,181, 13 classes total; X log-normalized; labels via obs/celltype, study via obs/tech.
- Dev: pancreas_facs.csv 99,571,196B sha256_16 cff5ce3901636b1e (matches 022 provenance hash).
