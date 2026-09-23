# DOC-1-005 GATES v2 — locked 2026-09-23 ~23:52 IST, BEFORE any v2 outcomes. Lane EXP-1.
# Reason for amendment: new program-wide bar (user steering via main, 23:44): every topic
# must be a concrete experiment - trained model, docking, or biomarker classifier with
# held-out validation; descriptive-statistics-only no longer meets the useful bar.
# v1 design (Markov vs climatology, GATES.md SHA 99eb3c8b...) stays intact as the BASELINE
# arm. v2 adds the trained deep-learning arm. All v2 parameters frozen below.

## v2 addition: trained neural transition forecaster (the experimental arm)
- Model: sklearn MLPClassifier, hidden_layer_sizes=(64,32), relu, adam, lr default,
  max_iter=300, random_state=20260923, trained on the SAME 20-dim PCA features.
- Labels: for each train cell, true next-state = state of its nearest train neighbor at
  higher pseudotime (identical construction to v1; no leakage: PCA unsupervised on all
  cells, transitions and labels use train cells only, evaluation on held-out test cells).
- Inputs: same frozen split, same states (k=12), same pseudotime as v1.

## v2 success gates
- G1b (primary, replaces G1 as the useful bar): MLP per-cell NLL (predict_proba
  log-loss) < climatology NLL, paired Wilcoxon p<=0.01, AND MLP top-1 accuracy >= 1.5x
  climatology top-1. This is a trained model validated on held-out cells.
- G3 (head-to-head, reported not gated): MLP vs Markov transition model NLL + accuracy.
  If the Markov baseline wins, that is reported honestly as the measured ordering.
- v1 gates G1 (Markov vs climatology) and G2 (horizon curve) are still computed and
  reported as the baseline arm; they no longer decide usefulness on their own.
- Failure policy: if G1b fails, the pivot rule applies - next angle is a trained
  biomarker classifier for lineage commitment (cluster labels as outcome, held-out
  AUROC), locked as v3 before any v3 outcomes. A documented negative for BOTH a trained
  forecaster and the Markov baseline is a boundary only after that v3 attempt.
- Payload: trained model artifact (joblib) + fate_forecast.py CLI mapping an expression
  vector to a next-state distribution, plus the v1 horizon-skill curve.
