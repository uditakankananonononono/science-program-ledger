# PROVENANCE (started 2026-09-24, LOCKED with GATES before outcomes)
- figshare article 5715040: "Single-cell RNA-seq data from Smart-seq2 sequencing of FACS sorted cells"
  (Tabula Muris). FACS.zip https://ndownloader.figshare.com/files/10038307 (290MB, range-extract tissue
  members only); annotations_FACS.csv https://ndownloader.figshare.com/files/10039267.
- Schaum, Karkanias et al. 2018, Nature 562:367-372 (Tabula Muris).
- Harmony: Korsunsky et al. 2019, Nat Methods 16:1289-1296; harmonypy (pip, slowkow/harmonypy).
- Luecken et al. 2022, Nat Methods 19:41-50 (scIB benchmark, context for baseline choice).
- Member hashes, cell counts, gene overlap, and the exact tissue list are appended when data lands.

## Landed (2026-09-24 07:32)
- FACS.zip 304,170,230B; members range-extracted: Pancreas-counts.csv 94MB sha256_16 cff5ce3901636b1e,
  Liver-counts.csv 46MB fcb94b3094a18096, Spleen-counts.csv 80MB 7ce239adb0529fa7,
  Lung-counts.csv 91MB 28cfca9c867d05bb (hashes of decompressed bytes, script code/prep_data.py).
- annotations_FACS.csv 4,321,940B (direct download).
- After label join: Pancreas 710 / Liver 710+ / Spleen 1689 / Lung 1620 annotated cells used (see split.json);
  23,433 genes shared across the 4 tissues. Shared label set (>=30 cells in >=2 tissues): 5 classes
  (B cell, T cell, endothelial cell, leukocyte, natural killer cell), frozen pre-scoring in
  results/class_list.json. Caveat: Tabula Muris labels are hierarchical (leukocyte is a parent of B/T/NK);
  carried into G4 interpretation.
