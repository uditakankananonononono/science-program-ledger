# DOC-1-005 — "Molecular weather": a Markov forecaster for cell fate transitions
# GATES locked 2026-09-23 ~23:34 IST, before any outcome inspection. Lane EXP-1.
# Redesign for 2 CPU/2GB: the weather-model idea reduces to its testable core - if cell
# state is a dynamical system, a first-order Markov model on expression states should
# forecast the next state better than climatology (the marginal distribution), and the
# forecast should decay with horizon like weather forecasts do.

## Data (public; GEO, URL + SHA-256 in provenance)
- Paul et al. 2015 myeloid progenitors MARS-seq (GSE72857_umitab.txt.gz) - ~2.7k cells
  spanning CMP/GMP/MEP differentiation, the standard fate-transition benchmark.

## Frozen design
- Normalization: CPM + log1p; top 1000 variable genes; PCA to 20 components (fit on
  all cells - unsupervised, no leakage).
- States: k=12 clusters (k-means, frozen seed) on PCA scores.
- Pseudotime: diffusion pseudotime computed on the PCA kNN graph, rooted at the
  cluster with the highest pre-registered stemness score (mean expression of
  pre-registered markers: Cd34, Kit, Flt3, Gata2) - all frozen before outcome metrics.
- Train/test: cells split 50/50 by frozen seed, stratified by cluster.
- Model: first-order Markov transition matrix on states ordered by pseudotime
  (transitions between pseudotime-adjacent cells, learned on train cells only);
  baseline = stationary state distribution ("climatology").
- Metric: per-cell negative log-likelihood of the TRUE next-state (the state of the
  test cell's nearest train neighbor at higher pseudotime) under model vs baseline.

## Success gates
- G1 (primary): model NLL < baseline NLL with a paired Wilcoxon p<=0.01 AND mean
  top-1 next-state accuracy >= 1.5x the baseline top-1 rate.
- G2 (weather payload): the forecast-horizon curve - 2-step and 3-step forecasts
  (matrix powers) still beat climatology (same NLL comparison), quantifying skill
  decay with horizon.
- Failure policy (pivot rule): if G1 fails, pivot to direction-only forecasting
  (does the model at least predict UP- vs DOWN-gradient moves? locked in v2 first);
  if that fails, documented boundary (single-snapshot scRNA cannot support dynamical
  forecasting at this resolution).
- Payload: transition matrix + horizon-skill curve + CLI that, given an expression
  vector, returns the predicted next-state distribution (the "fate forecast").

## Reviewer questions (pre-registered)
- Circular pseudotime? Root + markers frozen; pseudotime uses all cells unsupervised
  but outcomes are held-out on cells never used to learn transitions.
- Climatology too weak a baseline? It is the honest weather baseline; a stronger
  expression-similarity baseline is the named next experiment.
