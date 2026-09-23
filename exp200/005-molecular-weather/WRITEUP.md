# DOC-1-005 — "Molecular weather": forecasting cell-fate transitions (EXP-1)

**Verdict: USEFUL (candidate, adjudication requested).** A trained neural forecaster and a
Markov transition model both forecast held-out cell-fate transitions far above climatology;
the head-to-head ordering (Markov beats the deep model on NLL) is itself the measured,
surprising result.

## Design (gates locked before outcomes)
GATES.md (v1, SHA 99eb3c8b...) locked the Markov-vs-climatology design. GATES_v2.md
(SHA f3767e42...) amended in the trained-model arm after the program-wide bar moved to
concrete experiments only, BEFORE any v2 outcomes: sklearn MLPClassifier (64,32), frozen
seeds, trained on 20-dim PCA of CPM+log1p top-1000 variable genes, labels = next-state of
nearest train neighbor at higher diffusion pseudotime; 50/50 stratified held-out split.

## Data
Paul et al. 2015 myeloid progenitors, MARS-seq, GEO GSE72857 (URLs + SHA-256 in
results/provenance.md). **Errata vs gates:** the GEO umitab contains 10,368 wells, not the
~2.7k QC'd cells the paper analyzes; all wells were used (gates did not pre-register a QC
cutoff). 3 of 4 pre-registered stemness markers were found (Cd34, Flt3, Gata2; Kit absent
from the matrix). MLP hit max_iter=300 without full convergence (documented; predictions
still dominate climatology by ~8x).

## Results (5,180 held-out cells)
| gate | result | verdict |
|---|---|---|
| G1b (primary, v2): MLP vs climatology | NLL 0.959 vs 2.456, Wilcoxon p < 1e-300; top-1 86.4% vs 11.0% (7.9x, gate 1.5x) | **PASS** |
| G1 (v1): Markov vs climatology | NLL 0.490 vs 2.456, p < 1e-300; top-1 88.2% vs 11.0% | PASS |
| G3: head-to-head (report-only) | Markov NLL 0.490 < MLP NLL 0.959; top-1 88.2% vs 86.4% | **Markov wins** |
| G2: horizon curve | 2-step NLL 0.550, 3-step 0.637, both < climatology 2.456 | PASS |

## What is useful here
1. **A trained fate forecaster that works on held-out cells** (86.4% top-1 next-state
   accuracy, ~8x climatology) - shipped as fate_forecast_model.joblib + fate_forecast.py
   CLI (expression vector -> next-state distribution; smoke-tested on a real cell).
2. **A measured methodological ordering:** at this data scale (10k cells, 12 states), the
   trivially-simple first-order Markov model calibrated the better probabilistic forecast
   (NLL 0.49 vs 0.96) while the neural net matches on accuracy. Deep models do not
   automatically win single-snapshot trajectory forecasting - a useful negative for the
   "just use deep learning" instinct, with both models shipped for reuse.
3. **Weather-style skill decay quantified:** forecast skill persists but degrades with
   horizon (0.49 -> 0.55 -> 0.64 NLL at 1/2/3 steps), the "molecular weather" payload.

## Honest limits
Next-state labels derive from pseudotime ordering on the same unsupervised PCA all models
share (locked design; unsupervised, no outcome leakage). Single snapshot: no true temporal
ground truth exists in this data; "next state" is a pseudotime construct. Wells include
low-UMI droplets (min lib size 10) since no QC cutoff was pre-registered.
