# ADDENDUM B - locked 2026-09-24 07:10 IST BEFORE any label parsing; SUPERSEDES Addendum A
Addendum A was written for the L1-Lindel mirror files, which turned out to be model-INPUT feature
vectors (per-sequence possible-indel indicators), not outcome labels - that data source cannot
yield outcome labels at all and is abandoned (files retained in results/local/ for the record).

New data source (eligibility verified by sheet names/headers only, no label analysis):
inDelphi SupplementaryData.xlsx (Shen et al., Nature 2018;563:646 - repo
github.com/maxwshen/indelphi-dataprocessinganalysis, 652,001 bytes):
- Dev: Supplementary Table 2 (LibA, 2000 guides): gRNA + 57nt Sequence Context + PAM +
  total readcount + TOTAL NUMBER OF UNIQUE INDELS (outcome complexity) in mESC and U2OS.
- Frozen sets (untouched until G2): (a) U2OS labels of the same LibA guides (cross-cell-type
  transport); (b) Supplementary Table 3 (designed repeat library, 2000 guides, different
  sequence design) mESC labels.

Labels (locked):
- y1 = log1p(unique indel count) - outcome complexity (regression, Spearman).
- y2 dropped (binary precise-class definition would require seeing the label distribution;
  replaced by the second frozen transport check, which is the stronger gate).
Features (locked): from the 57nt context (cut between positions 27|28, PAM at 28-30):
position-specific mono (57x4), dinucleotide counts (16), GC overall + PAM-proximal 10nt,
-4..-1 base indicators, microhomology features on the full context (max MH len, MH count,
Bae-style MH score - now exact, no spacer-only approximation).
Model: ridge (alpha 1.0, standardized), fit on mESC dev only.
Baseline (unchanged): Bae et al. 2014 MH score (Nat Methods 11:705).
Gates (bars unchanged from GATES.md): G1 dev 5-fold CV seed 7 Spearman > Bae + 0.05.
G2 frozen, single pass per frozen set: Spearman >= 0.45 absolute AND >= frozen Bae + 0.02
on EACH of U2OS-LibA and Table-3. G3/G4 as amended in Addendum A (precision determinants
vs literature; predict_precision.py CLI, 57nt context input; Parts lab nomination).
Failure tree unchanged (P1 HistGradientBoosting fixed hyperparams; P2 readcount-floor >= 500
restriction; all fail -> documented boundary). Thresholds never relax after outcomes.
