# DOC-2-032 Virtual Cell Failure Cartography - R0 locked protocol

Lock timestamp: 2026-09-22 13:02 IST, before opening expression outcomes.

## Question and novelty
Can a virtual-cell predictor look accurate on whole-transcriptome expression while failing on the perturbation-induced response, and is that failure label reproducible across independent cell splits? This maps evaluation failure regimes rather than asking whether another perturbation model wins an average benchmark.

## Data
Primary R0 source: scPerturb's harmonized Adamson et al. 2016 `GSM2406675_10X001` CRISPRi Perturb-seq sample, Zenodo record 7041849. One sample avoids batch ambiguity. The original study profiled unfolded-protein-response perturbations. Required fields will be identified without changing thresholds. Open sources:
- https://zenodo.org/records/7041849
- https://doi.org/10.1016/j.cell.2016.11.048
- https://www.sanderlab.org/scPerturb/

## Unit, estimand, and predictor
Unit: a perturbation condition with at least 50 cells. Control requires at least 200 cells. Genes require detection in at least 20 cells; retain up to 2,000 most variable genes based only on control cells.

For each of two deterministic, stratified half-splits of cells, compute condition pseudobulk means. The deliberately simple virtual-cell baseline predicts each perturbed mean as the control mean (a no-response predictor).

For perturbation p:
1. `r_abs(p)`: Pearson correlation between predicted and observed absolute mean expression over analysis genes.
2. `response_capture(p)`: 1 - MAE(predicted response, observed response) / mean(abs(observed response)); for the no-response predictor this is exactly 0, retained as a sanity check.
3. `top50_sign(p)`: fraction of the 50 genes with largest absolute observed response whose predicted response has the same nonzero sign. Ties/zero predictions count wrong.
4. `relative_response_norm(p)`: L2 norm(predicted-control) / L2 norm(observed-control), expected 0 for the no-response baseline.

Primary estimand: proportion of eligible perturbations in the **metric-mirage** regime: `r_abs >= 0.90` AND `top50_sign <= 0.55`.

Failure taxonomy (priority order):
- Metric mirage: above definition.
- Transparent collapse: `r_abs < 0.90` AND `relative_response_norm <= 0.25`.
- Other directional failure: `top50_sign <= 0.55` but neither above.
- Directionally adequate: `top50_sign > 0.55`.

Reproducibility: same perturbation receives same taxonomy label in both half-splits. Also report median absolute split-to-split difference in `r_abs`.

## Locked feasibility and success gates
F0 data feasibility: >=8 eligible non-control perturbations, >=200 control cells, and >=1,000 eligible genes. If F0 fails, R0 stops negative.

S1 primary gate: in both cell half-splits, metric-mirage prevalence >=25%, and the pooled Wilson 95% lower confidence bound is >10%.

S2 stability gate: label agreement between the two half-splits >=80%, and median absolute change in `r_abs` <=0.03.

S3 nontriviality gate: at least two taxonomy classes are occupied in either split. This prevents claiming a useful cartography if every perturbation gets the same label.

Overall R0 pass requires F0 + S1 + S2 + S3. Gates will not be changed after outcome inspection. Negative results and implementation failures are retained.

## Sensitivity analyses (descriptive only, cannot rescue gate failure)
Repeat `r_abs` after per-gene centering by control; report how many metric mirages disappear. Repeat top-k sign score for k=25 and k=100. No new success gate will be introduced.
