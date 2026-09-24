# DOC-1-031F: Family-Aware AMP Model — GATES (locked before any scoring)

Follow-up to DOC-1-031 (documented boundary: homology-leakage-dominated benchmark; best
frozen ARM B 3-mer logistic MCC 0.3798; mechanism: learned signal real but family-specific,
disjoint DRAMP families missed). Parent-approved follow-up queue 2026-09-24 10:59:00;
approved sketch: "family-aware multi-head or motif-augmented model (explicit Cys/cationic
motif features + per-family calibration), frozen on family-disjoint DRAMP split. Gate:
frozen MCC >= 0.37 + 0.10." Fresh experiment, fresh gates; NOT a retry of any 031 gate
(008->METENG pattern).

## Eligibility findings (locked in as facts, verified pre-gate)
- Train/dev data re-downloaded and HASH-VERIFIED identical to 031's committed manifest
  (AmPEP train AMP 4ea306a654433e4b, nonAMP 00f6dffd1ccd9fee, iAMP-2L Supp-S2
  5ef4d00a679274e2).
- Frozen positives: 031's committed 2,068 sequences (results/dramp_frozen_pos.json) reused
  EXACTLY (pinned, no redraw).
- Frozen negatives: 031's exact negative set is unrecoverable (sandbox rebuild; the draw was
  not ID-pinned in 031's manifest - itself a reproducibility finding). Rebuilt under the
  locked procedure below; disclosed as a redraw. Same-draw ARM B control re-trained and
  scored on the SAME rebuilt negatives so every comparison is same-draw.
- DRAMP download site 404s as of 2026-09-24 (documented; not blocking: positives are pinned
  in-repo; decontamination spec adapted below).
- Family labels: no public DRAMP family annotation; families = 80%-identity single-linkage
  clusters over train AMPs (BLASTP-short), consistent with 031's 80% pruning granularity.

## Data
- TRAIN: AmPEP train 3,268 AMP + 166,170 non-AMP (identical to 031 ARM B's training set).
- DEV: iAMP-2L Supp-S2, 920 AMP + 920 NAMP.
- FROZEN: 2,068 pinned positives + 2,068 rebuilt negatives: UniProt reviewed segments,
  length-matched 1:1 per positive (same length), decontaminated at 80% identity (BLASTP-
  short) vs the 2,068 positives + 3,268 train AMPs + 920 dev AMPs; draw seed 42; procedure
  and seed locked here pre-draw.

## Arms
- ARM B-control: 031's ARM B (3-mer logistic) re-trained on identical data, scored on the
  rebuilt negatives (same-draw control; 031's committed 0.3798 is the cross-draw anchor).
- ARM C (the claim): ARM B features + 14 explicit motif/biophysical features: length; Cys
  count; Cys fraction; disulfide-pattern counts (CC, CXC, CXXC, CXXXC); net charge/length
  (K+R-D-E); cationic fraction (K+R); hydrophobic fraction (AILMFWYV); Gly fraction; Pro
  fraction; cationic-3mer density (counts of RIV,RFG,RDY,GRL per length); Cys-rich-3mer
  density (CCV,GYC,CSR,CCL,TCY per length). Logistic, same protocol as ARM B.
- ARM D (family-conditional): ARM C logit + shrunk family offset: offset_f = (sum of family
  train residuals)/(n_f + 10); family assignment = max BLASTP-short identity to any train
  AMP family member >= 80%, else offset 0.

## Gates
- G1 (sanity halt): ARM C dev MCC >= ARM B dev - 0.05 (ARM B dev 0.954 -> bar 0.904).
  Else incoherent - document, stop, report to parent.
- G2 (the claim, frozen): ARM C frozen MCC >= 0.47 (= 0.37 + 0.10 per the approved sketch)
  AND >= ARM B-control same-draw + 0.05.
- G3 (family mechanism, frozen): ARM D >= ARM C + 0.02.
- G4 (mechanism, runs regardless): frozen positives stratified by max identity to train
  AMPs (>=80% / 50-80% / <50%), per-stratum TPR for B-control/C/D; ARM C motif-feature
  coefficients vs 031's G4 (Cys-rich + cationic expectation); negative-set redraw
  sensitivity statement.
- G5: CLI amp_predict_family.py + prospective lab nomination.
- Failure tree: G1 fail -> halt to parent. G2 fail -> DOCUMENTED BOUNDARY (motif
  augmentation + family calibration ARE the mechanism-targeted fixes; no further rescue
  pre-registered). G3 fail with G2 pass -> report both; parent adjudicates (family
  calibration adds nothing over motif features would itself be the finding).

## Prospective lab nomination (locked)
A soil-microbiome group screening metagenomic AMP candidates: family-aware scorer that
reports the family-assignment provenance of each call, validated by spot synthesis of
top-scoring novel-family candidates.

## Scoring discipline
GATES + PROVENANCE committed BEFORE any training/scoring. Thresholds never relax after
seeing outcomes.
