# ADDENDUM A - locked 2026-09-24 07:09 IST BEFORE any label content is parsed
Implementation erratum discovered while validating data format (only file headers inspected):
the mirrored Lindel train/test txt files contain 20nt spacer + ~556 binary outcome-class PRESENCE
indicators - not read frequencies, no 65bp context, and the column->indel-class mapping is not
recoverable from the mirror (vendored gen_indel code requires 65bp input).

Consequences (locked):
- y1 REDEFINED: outcome complexity = number of distinct observed outcome classes per guide
  (row-sum of presence vector). Regression target, Spearman. This is the presence-analog of
  outcome precision (Lindel/inDelphi precision concept), not read-weighted frameshift fraction.
- y2 REDEFINED: precise guide = <= 3 observed outcome classes (binary), the design-relevant
  property for templated editing (precise guides enable predictable repair).
- Features REDEFINED to 20nt-spacer-computable: position-specific mono (80), dinucleotide
  counts (16), GC overall + PAM-proximal 6nt, -4..-1 base indicators (spacer positions 14-17,
  cut between 17|18), microhomology features computed on the 20nt spacer (max MH length around
  cut +/-10, MH count, Bae-style MH score). Flank-dependent MH events outside the spacer are
  missed - documented approximation; affects model and baseline equally.
- Named baseline unchanged: Bae et al. 2014 MH score (computed on 20nt approximation).
- Thresholds unchanged: G1 y1 Spearman > Bae + 0.05, y2 AUROC > Bae + 0.03 (5-fold CV seed 7);
  G2 frozen published test split, y1 Spearman >= 0.45 AND >= Bae + 0.02; y2 AUROC >= 0.70 AND
  >= Bae + 0.01. Read-count floor dropped (no read counts exist); zero-outcome guides dropped.
- G3 mechanism reframed: learned precision determinants vs literature (MH strength Bae 2014 /
  Shen 2018; spacer GC Allen 2019).
- G4 CLI: predict_precision.py (20nt spacer -> predicted complexity + P(precise)).
