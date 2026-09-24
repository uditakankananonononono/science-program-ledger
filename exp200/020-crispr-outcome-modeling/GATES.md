# DOC-1-020 GATES - locked 2026-09-24 07:09 IST BEFORE any outcome data is parsed
Topic: Fine-Tuning Evo 2 for Gene Editing Guide Design.
Feasibility check (done pre-gates, metadata only): Evo 2 smallest checkpoint is evo2_1b_base (1B params,
25 layers - huggingface.co/arcinstitute/evo2_1b_base). Fine-tuning 1B params is impossible on
2 CPU / 1.9GB RAM (weights alone 2-4GB); even int8 inference is marginal. Per the locked pivot rule
(parent approved 07:07): execute a feasible guide-DESIGN arm that is NOT another efficiency scorer
(algo50/43 already did Doench efficiency, Spearman-on-activity, in the same repo).

## Pivot arm (locked): Cas9 repair-outcome modeling
Predict the STRUCTURE of editing outcomes per guide - frameshift fraction and dominant-outcome class -
from the 65bp local sequence context. Different label family, dataset, and baselines from algo50/43.

## Data (locked)
Lindel dataset (Chen, Willinghan et al., Nucleic Acids Res 2019;47(15):8275 - the published Lindel
training/test data, mirrored in github.com/gtrevnenski/L1-Lindel data/):
- Dev: Lindel_training.txt (~64MB; parsed streaming). Frozen: Lindel_test.txt (6.5MB) - the PUBLISHED
  test split, untouched until G2.
- Parsed per guide: 65bp context + per-indel outcome frequencies. Derived labels:
  y1 = frameshift fraction = sum freq of outcomes with |indel length| mod 3 != 0 (regression target).
  y2 = dominant outcome is microhomology-mediated deletion (binary).
  Drop guides with total outcome reads below a locked floor of 100 (label noise); report drop count.

## Named published baseline (locked)
Bae et al. 2014 (Nat Methods 11:705) microhomology score - the original published repair-outcome
scoring rule, computed from sequence alone (pattern score of MH-mediated deletions, length*weight
scheme per Bae). This is the baseline inDelphi and Lindel both benchmark against.

## Model (locked)
Features: position-specific mononucleotides over 65bp (65x4), dinucleotide counts, GC overall and
in PAM-proximal 10bp, microhomology feature set (max MH length, Bae MH score, MH count), -4..-1
PAM-distal base indicators (the known 1bp-insertion determinants, Shen 2018).
Ridge (alpha 1.0) for y1; LR (L2 C=1.0, class_weight balanced) for y2. Standardized, fit on dev only.

## Gates
G1 (dev, 5-fold CV seed 7): y1 Spearman of ridge > Bae-score Spearman + 0.05; y2 AUROC of LR >
  Bae-score AUROC + 0.03. Document loss per target otherwise.
G2 (frozen published test split, fit on dev only, single pass, no refit): y1 Spearman >= 0.45
  absolute AND >= frozen Bae + 0.02; y2 AUROC >= 0.70 absolute AND >= frozen Bae + 0.01.
G3 (mechanism vs literature): top learned features compared to known determinants (MH strength,
  -4 base for insertions, GC; Shen 2018 / Allen 2019): report top-10 features per target and check
  consistency; frameshift fraction should anti-correlate with dominant in-frame MH deletions.
G4: predict_outcome.py CLI (65bp context -> predicted frameshift fraction + P(dominant MH deletion))
  smoke-tested on 3 locked sequences + prospective lab nomination (Leopold Parts lab, Sanger -
  FORECasT co-author, repair-outcome modeling).

## Failure tree (locked)
G1 fail -> P1: HistGradientBoosting (fixed hyperparams, same features). P2: restrict to guides with
>=500 reads. If no arm beats Bae by locked margins -> documented boundary: sequence-alone outcome
structure saturates at the MH score in this envelope. Evo 2 head-to-head = Addendum E1 if a
GPU-capable lane ever runs it (metrics locked here). Thresholds never relax after outcomes.
