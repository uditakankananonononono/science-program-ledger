# DOC-1-006C — structural-DL epitope arm on PRISTINE 6AL5 (parent-sanctioned 00:35)
# GATES locked 2026-09-24 ~01:07 IST, BEFORE downloading 6AL5, BEFORE any DL training.
# Parent condition: FRESH gates calibrated to the published field's 0.6-0.65 AUROC
# range, locked before results. 006B's 0.70 bar is NOT relaxed - this is a new
# experiment with a new (DL) hypothesis and its own pre-locked bar; no 006B result
# is re-judged.

## Data
- TRAIN: the 16 curated antibody-antigen PDB complexes from 006B (URLs+SHA in 006B
  provenance). PDB IDs fixed by 006B's feat.json inventory.
- FROZEN EXTERNAL TEST: PDB 6AL5 (B43 anti-CD19 scFv - CD19 complex). Never used in
  any prior fitting, selection, or threshold decision (006B addendum preserved it).
- Epitope label (locked): antigen-chain residues with any heavy atom within 4.0A
  of any antibody-chain (scFv) heavy atom. Standard structural-epitope definition.

## Features (per antigen residue, shipped featurizer)
SASA-relative, 10A contact number, half-sphere exposure, secondary structure
(PDB HELIX/SHEET records), Kyte-Doolittle hydrophobicity, Parker hydrophilicity,
Levitt propensity, window +-4 aggregates of all numeric features, plus a LEARNED
20-AA embedding (dim 8) inside the network.

## Model (DL actually trained; recipe fully frozen - no post-hoc tuning)
torch CPU. Window 9 residues. Embedding(20->8) concat numeric -> Conv1d(64,k=3,GELU)
-> Conv1d(64,k=3,GELU) -> center-token linear(64->32,GELU,dropout 0.3) -> linear(1).
BCE with pos_weight=neg/pos, Adam lr 1e-3, batch 256, weight_decay 1e-4,
FIXED 30 epochs, seed 20260924. Any recipe change requires a new addendum locked
before the outcomes it governs.

## Named published baselines (ISEF)
- BepiPred-1.0 (Larsen et al. 2006): Parker hydrophilicity, 7-mer rolling mean,
  sign as published.
- SASA-only structural baseline (classic).
- 006B GBM (prior arm) reported as comparator.

## Gates
- G1 (LOCO-CV over 16 complexes, complex=fold): mean AUROC reported honestly AND
  200 full-pipeline label permutations with observed > ALL nulls.
- G2 (frozen external, primary): train on all 16, apply ONCE to 6AL5:
  AUROC >= 0.62 (field-calibrated 0.6-0.65) AND beats BepiPred-1.0 on the same
  residues by >= 0.02 AND beats SASA-only by >= 0.02.
- G3 (mechanism): top predicted contiguous patch checked against published B43 /
  CD19 epitope literature; agreement or honest discrepancy documented.
- Tool + nomination: cart_epitope_score.py CLI (PDB+chain -> per-residue scores,
  smoke-tested) + top-3 predicted patch residues nominated for alanine-scan
  mutagenesis (only if G2 passes).
- Failure: if G2 fails -> documented boundary for the structural-DL angle.
  NO threshold relaxation after results (re-fishing clause per parent 00:35).
