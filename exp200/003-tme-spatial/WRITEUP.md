# DOC-1-003 — TME as interacting agents: spatial autocorrelation is largely technical; LR co-localization below the floor

**Status: G1 locked-direction FAIL with the pre-locked inversion CONFIRMED (candidate methodological result); G2 + v2 FAIL (documented boundary).**

## One-line
In the 10x Visium breast-cancer section (3798 in-tissue spots), a gene's spatial
autocorrelation (Moran's I) is predicted by just two technical covariates - mean
expression and dropout - at held-out r=0.716 (500/500 gene split, permutation null
q95=0.085). And 48 pre-registered ligand-receptor pairs show NO co-neighborhood
enrichment above an expression-decile-matched null at 1-hop (median 0.022 vs q95 0.077)
or 2-hop (0.030 vs 0.104).

## Gate ledger
- G1 (locked direction "structure is biological"): FAIL. The locked inversion clause
  fires: covariates suffice to predict Moran's I. Quantified: r=0.716 held-out.
- G2 (LR co-localization vs plain randoms): FAIL as-run (implementation erratum
  documented in addendum-1: frozen gate specified decile-matched nulls).
- G2 corrected (matched null): FAIL (0.022 vs 0.077).
- v2 pivot (2-hop, locked before computation): FAIL (0.030 vs 0.104).

## Why this is still worth reading (per the pivot rule)
The useful extraction: Visium spot resolution (~100um, 1-10 cells) plus expression-level
technical autocorrelation sets a FLOOR - 48 classic TME ligand-receptor pairs cannot be
resolved above it in either neighborhood radius. Any Visium cell-cell-communication
claim in this tissue needs (a) technical-covariate control (our ridge reaches r=0.72
with 2 features) and (b) sub-spot deconvolution. The audit CLI ships exactly that check.
Counting: reported to lead lane as a CANDIDATE methodological useful result
(technical-floor quantification + tool); LR boundary not counted.

## Payload
- results/morans_i.csv (1000 genes), lr_scores_*_matched.csv, random_*_matched.csv
- code/visium_spatial_tool.py - Moran's I + technical-covariate audit for any Visium
  filtered matrix (smoke-tested on this section, reproduces r=0.72).
