# algo50/11 - Finding nuclear localization signals: classical regex vs a learned window scanner

Status: LOCKED before any method was scored (UTC time + sha256 in results/lock.txt). Lane RES-1.

## Question
Classical NLS patterns (pat4, pat7, bipartite) are the standard way to spot nuclear import signals. On experimentally mapped NLSs, does a small learned window scanner find them better than the regex rules and better than a plain basic-residue density score, without flagging more secreted proteins that should have no NLS?

## Data
- Positives: UniProt reviewed entries (release 2026_03) with a MOTIF "Nuclear localization signal" feature, keeping ONLY segments with experimental evidence ECO:0000269. ECO:0000255 (sequence-model inferred, often from the same regex rules) is excluded to avoid circularity. 289 proteins, 344 segments, 256 families.
- Negative control: 1126 reviewed human proteins with experimental "Secreted" location, not annotated nuclear, no NLS feature.
- Query URLs, time, sha256 in data/.

## Methods
- M0 regex (no training): pat4 = 4 consecutive K/R, or 3 K/R + H or P in a 4-window; pat7 = P then within 3 residues a 4-window with >= 3 K/R; bipartite = 2 K/R, 10-12 aa spacer, >= 3 K/R in the next 5.
- M2 baseline: K+R count in a centered 11-aa window.
- M1 learned scanner: logistic regression (C=1, balanced class weights) on a centered 15-aa window: position one-hot (300) + counts of K/R, P, H, D/E. Per-residue label = inside an experimental NLS.
- Split: 5-fold cross-validation grouped by UniProt protein family (entries with no family are their own group), seed 11. Thresholds for M1 and M2 are picked on training folds only (max segment F1). Negatives never used for training.
- Predicted segments = maximal runs of residues at or above threshold (M1, M2) or regex matches (M0).

## Metrics
- Residue-level AUPRC within positive proteins (M1 vs M2; M0 as a single point).
- Segment F1: recall = true NLS overlapped by any predicted segment; precision = predicted segments overlapping a true NLS.
- Secreted flag rate: fraction of negative proteins with >= 1 predicted segment (M1 at the median of its 5 fold thresholds, trained on all positives).
- 95% CIs: 2000 bootstrap resamples of proteins, paired.

## Success gates (declared before scoring)
- G1: M1 AUPRC - M2 AUPRC >= 0.05, CI lower bound > 0.
- G2: M1 segment F1 - M0 segment F1 >= 0.05, CI lower bound > 0.
- G3: M1 secreted flag rate <= M0 secreted flag rate.

## Caveats known upfront
Unannotated real NLSs inside positive proteins count as false positives, so precision is a lower bound for every method equally. All results reported pass or fail; any pivot is a timestamped amendment labelled post hoc.
