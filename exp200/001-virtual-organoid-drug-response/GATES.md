# DOC-1-001 — Virtual Organoid / Drug Response from Baseline Transcriptomics
# GATES (locked 2026-09-23 21:49 IST, before any outcome inspection)
# Lane: EXP-1. Compute reality: 2 CPU / 2GB RAM sandbox — full generative organoid model
# is not executable here; per the program's redesign-path rule, the testable core is:
# can baseline transcriptomic state predict small-molecule sensitivity, for which drugs,
# and where is the boundary?

## Data (public, URLs + SHA-256 recorded in results/provenance.md after download)
- GDSC2 fitted dose response (Sanger cancerrxgene release 8.5): ln IC50 per cell line x drug.
- DepMap Public 24Q2 OmicsExpressionProteinCodingGenesTPMLogp1 (baseline expression) + Model.csv (lineage).

## Frozen design decisions (pre-outcome)
- Drug panel rule (fully specified, applied before any model evaluation):
  all GDSC2 drugs with >=300 cell lines having both IC50 and expression; if >30 qualify,
  keep the 30 with highest IC50 variance across lines. This rule is frozen NOW, before
  seeing which drugs qualify.
- Features: top 2000 protein-coding genes by variance (selection inside each training
  fold only — no leakage), log1p TPM input.
- Model: ridge regression (alpha by inner 3-fold CV), 5-fold cell-line-disjoint CV.
- Baseline: drug-specific training-fold mean (the "no-information" predictor).

## Success gates
- G1 (primary): median relative RMSE reduction vs drug-mean baseline >= 5% across panel
  drugs, AND >=50% of panel drugs individually beat a 20x label-permutation null (p<=0.05).
- G2 (boundary hypothesis, pre-registered): drugs classed as targeted (kinase/epigenetic/
  pathway inhibitors per GDSC TARGET_PATHWAY) show higher per-drug predictability
  (CV R^2) than cytotoxic drugs (Mann-Whitney U, p<=0.05, one-sided).
- G3 (tool): shipped CLI predicts ln IC50 for (expression vector, drug) with an
  abstention rule (training-set Mahalanobis distance threshold); abstention set shows
  higher accuracy than the abstained set — sanity, not a headline claim.

## Failure policy (pivot rule)
- If G1 fails: pivot to boundary mapping — which drug classes are intrinsically
  unpredictable from baseline expression, and is unpredictability itself informative
  (e.g., correlates with response heterogeneity)? New gates locked in GATES-v2.md
  BEFORE any new-direction results are inspected. Original failure documented here.
- Honest negatives preserved; no re-fishing.

## Reviewer questions (pre-registered)
- Leakage? Feature selection is in-fold; CV is line-disjoint.
- Clinical relevance? Cell lines are a proxy; the boundary map is the contribution.
- Permutation count low (20)? Compute ceiling declared; p-resolution 0.048 acknowledged.
