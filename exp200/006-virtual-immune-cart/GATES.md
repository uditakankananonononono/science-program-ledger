# DOC-1-006 — "Virtual Immune System" for CAR-T: infusion-product fitness classifier
# GATES locked 2026-09-24 ~00:22 IST, before any expression data is parsed. Lane EXP-1.
# New bar + ISEF checklist applied. PPD lessons applied: permutation discipline inside
# full pipeline, frozen external cohort, no post-hoc panel claims.

## Data (public, GEO, URLs + SHA-256 in provenance.md)
- DISCOVERY: GSE151511 (Deng et al. 2020 Nat Med, scRNA of CAR-T infusion products,
  DLBCL/tFL/PMBCL). Response label from GEO metadata "3mo pet/ct": CR = responder,
  PD = non-responder; PR (n=1) and NE (n=1) EXCLUDED. Locked n=22 (9 CR / 13 PD).
- EXTERNAL (frozen, untouched until model lock): GSE197268 (Haradhvala et al. 2022
  Nat Med, axi-cel scRNA). Infusion-product (Day 0) samples only; per-patient response
  labels from the paper's public supplementary table (recorded verbatim in provenance;
  if labels are not extractable, fallback external = GSE235760, same gate structure,
  documented as an addendum before any external data is touched).

## Frozen per-patient feature design (cell-level counts -> patient vector)
- T-cell gate: cell is a T cell if CD3D>0 or CD3E>0 (UMI counts).
- Frozen marker panel (22 genes): ID: CD3D, CD3E, CD8A, CD8B, CD4; memory/fitness:
  CCR7, SELL, TCF7, IL7R, CD27; exhaustion: PDCD1, HAVCR2, LAG3, TOX, TIGIT;
  cytotoxic: NKG7, GZMB, PRF1, GZMK, GNLY; proliferation: MKI67, TOP2A.
- Per patient: among T cells, fraction positive (count>0) for each marker, mean
  log1p(CPM) per marker, CD8A/CD4 positive-fraction ratio = 24 features. No other
  features. Streaming aggregation (no full matrix load).

## Model + gates
- Model: L2 logistic regression (C=1.0), patient-level, frozen seeds.
- G1 (discovery): 20x repeated 5-fold CV mean AUROC >= 0.70 AND 200 full-pipeline
  permutations with observed AUROC exceeding ALL nulls (the PPD-learned criterion:
  internal CV alone is not evidence).
- G2 (PRIMARY, external): frozen feature extractor + frozen model applied ONCE to
  GSE197268 infusion samples: AUROC >= 0.65 AND bootstrap 95% CI lower > 0.5.
- G2c (named published baseline): beat the Deng 2020 reported response correlate -
  their CD8 memory-score direction (CCR7/SELL/TCF7 mean, documented from the paper) -
  on the SAME external cohort. Loss documented honestly.
- Biological interpretation: fitness-vs-exhaustion direction checked against Fraietta
  2018 (CD27+ PD-1- memory) and Deng 2020/Haradhvala 2022 reported biology.
- Tool: car_fitness.py CLI (infusion-product counts -> response probability) + ONE
  prospective lab nomination (top fitness marker with external-consistent direction).
- Failure/pivot: if G1 fails, ONE pre-registered pivot (v2): add MLP on the same 24
  features (the DL arm). If G2 fails after G1 passes: documented boundary, negatives
  preserved, no re-fishing.
