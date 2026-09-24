# P19-03 Protocol and Gates - LOCKED BEFORE RESULTS (lane D, 2026-09-24 ~13:40 IST)

Spec: doc290/cbio056-helu-dti-drug-target/03-conformal-hit-prioritization.md. Spec gates kept; amendments
locked before any model is trained.

## Pre-locked amendments
- A1 data: DAVIS only (68 ligands x 442 kinases; DeepDTA release, same files as P19-02). BindingDB, BioSNAP and
  ChEMBL are not fetchable here (as in P19-02). Binary label: interaction iff pKd >= 7.0 (the common DAVIS
  threshold).
- A2 model: the P19-02 classical HeLU surrogate features (amino-acid + hashed 3-mer protein composition, Morgan
  r=2 512-bit) with a deterministic 3-mer hash (crc32; P19-02 used Python's salted hash()). Classifier:
  HistGradientBoostingClassifier (seed 0). No LM embeddings or knowledge graph (same limitation as P19-02).
- A3 splits (seed 0): random (pairs), cold-drug (ligands) and cold-target (kinases). Each split is
  60% train / 20% calibration / 20% test, where calibration and test are drawn the same way as the split type
  (disjoint ligands/kinases for cold splits).
- A4 conformal: split-conformal classification at alpha = 0.10 with LAC score s = 1 - p(true class), plus a
  Mondrian (class-conditional) variant. Set size != 1 (empty or both labels) = "low confidence".
- A5 G1: random-split marginal coverage within 0.90 +/- 0.02.
- A6 G2: coverage loss on cold splits reported. Pass iff >= 70% of point-prediction errors (argmax wrong) fall
  in low-confidence sets on BOTH cold splits (standard split-conformal).
- A7 G3: no post-cutoff ChEMBL release is fetchable, so the prospective test is NOT EVALUABLE. No substitute is
  used.
- A8 pivot (spec): if cold-split coverage < 0.85, run weighted conformal with similarity weights
  w = exp(max similarity of the test item to the calibration items of that axis / 0.1) (Tanimoto for ligands,
  cosine of protein features for kinases) and report how much coverage it restores. Reported, not gated.
