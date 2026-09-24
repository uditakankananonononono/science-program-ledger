# ADDENDUM A (locked 2026-09-24 07:42, BEFORE any outcomes)

## Erratum: locked frozen cohort does not exist
GATES.md named Tabula Muris droplet (10x) Pancreas as the frozen cohort. Range-inspection of droplet.zip
(figshare 5715025, member list) shows NO Pancreas tissue in the droplet half of the atlas (dissociation
constraints; FACS Smart-seq2 only). Found during data acquisition, before any model run.

## Repair (governs the frozen gate; thresholds and margins unchanged)
- FROZEN cohort = human pancreas, smartseq2 study (Segerstolpe 2016) from the scIB integration task
  dataset (human_pancreas_norm_complexBatch.h5ad, figshare file 24539828, 315,955,785B; Luecken et al
  2022 Nat Methods 19:41). Labels: gamma = pancreatic PP cell = 213 cells; background = 2,181 cells
  across 12 other classes. This is a HARDER external validation than planned: species shift (mouse ->
  human) plus lab/pipeline shift; platform family nominal Smart-seq2.
- Gene harmonization: uppercase-symbol intersection between dev (mouse) and frozen (human) feature
  spaces; frozen pipeline uses its own HVG/standardization (same protocol steps).
- Adaptation disclosed: scIB X is already log-normalized, so the frozen pipeline SKIPS the log1p(CPM)
  step (documented; all other steps identical).
- Frozen rarity grid: background 2,181 -> n_gamma = 11 / 22 / 44 / 115 at r = 0.5% / 1% / 2% / 5%,
  nested, seed 7 (213 available, all feasible). Dev grid unchanged (6/12/25/64 of 1,220).
- G3 margins as locked: contrastive frozen mean-F1 >= frozen baseline + 0.03 AND winner frozen >= its
  dev - 0.10. No threshold relaxations.
