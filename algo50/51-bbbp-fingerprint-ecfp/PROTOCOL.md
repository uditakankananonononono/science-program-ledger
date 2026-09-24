# algo50/51 - Blood-brain barrier penetration: boosted ECFP counts vs linear fingerprints vs Tanimoto lookup

Lane RES-1.

## Question
Small-molecule property prediction from structure alone. BBBP (MoleculeNet)
is the standard small classification benchmark. With fingerprints computed
from SMILES and a proper Murcko-scaffold split: does a boosted model on count
ECFP + physicochemical descriptors beat (a) a linear model on binary ECFP,
(b) the field's default 1-NN Tanimoto lookup, and (c) is its ranking useful
for triage?

## Data
BBBP from MoleculeNet mirrors (deepchemdata S3: BBBP.csv), ~2,039 compounds
with SMILES and binary permeant label (`p_np`). Molecules whose SMILES fail
to parse are dropped and counted. Raw CSV not committed; sha256 + retrieval
time in `data/`.

## Split
Murcko scaffold (Bemis-Murcko framework via RDKit) group split: 5 folds,
scaffolds assigned to folds greedily by descending scaffold size to balance
fold sizes (seed 0). No scaffold crosses folds. This is the MoleculeNet-hard
setting; random splits are reported nowhere in this study.

## Features
- B0: RDKit MolLogP + MolWt + TPSA only (3 features), logistic.
- B1: binary ECFP4 (Morgan radius 2, 2048 bits), logistic (L2, C in
  {0.1,1,10} by inner scaffold-grouped CV on training folds only).
- M1: count ECFP4 (2048) + MACCS keys + 8 physicochemical descriptors
  (MolLogP, MolWt, TPSA, HBD, HBA, RotB, aromatic fraction, fractionCSP3),
  histogram gradient boosting (fixed: max_iter 300, lr 0.06, 31 leaves,
  min_samples_leaf 20, L2 1.0).
- B2 (chemical-lookup baseline): 1-NN by Tanimoto on binary ECFP4 within
  training folds; score = neighbor's label (tie -> training base rate).

## Evaluation
5-fold scaffold-grouped CV (every compound scored exactly once from a model
that never saw its scaffold). Primary metric: pooled AUROC. Triage metric:
precision among the top 10% highest-scored compounds vs base rate.

## Gates (declared before any model is run)
- G1: AUROC(M1) >= AUROC(B1) + 0.02.
- G2: AUROC(B1) >= AUROC(B0) + 0.05.
- G3: AUROC(M1) >= AUROC(B2 Tanimoto 1-NN) + 0.02.
- G4: precision in M1's top-decile scores >= 1.5 x base rate.

## Pivot plan (only if gates fail, pre-registered as amendments before results)
- P1: if G1 fails, feature ablation: M1 on count ECFP alone (no descriptors):
  gate P1 = AUROC(M1-nodesc) >= AUROC(B1) + 0.02.
- P2: if G3 fails, k-NN ablation (k=5, distance-weighted): gate P2 =
  AUROC(M1) >= AUROC(5-NN) + 0.02.

## Honest-negatives policy
Every gate outcome is reported PASS/FAIL as declared. Failed gates stay in the
README with their numbers.
