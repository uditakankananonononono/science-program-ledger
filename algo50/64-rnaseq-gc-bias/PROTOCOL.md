# algo50/64 - RNA-seq GC bias: detection and conditional-median correction

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55).

## Question
Simulated RNA-seq with a known GC-dependent amplification bias: can per-gene conditional-median normalization (the standard within-lane GC correction) recover true expression, and what does it do to genes whose GC content is confounded with condition (the known failure mode)?

## Data (simulated, seed 23)
2000 genes: true expression mu ~ lognormal; gene GC in [0.3,0.7]. Sequencing bias: observed counts ~ NB(mean = mu * b(GC)), b(GC) = exp(3*(GC-0.5)) (6x span). 100 genes are truly DE (2x up) - half drawn GC-biased-high (GC>0.6), half GC-neutral. Counts: negative binomial, dispersion 0.1, 3 replicates, depth 2M.

## Methods
- Correction: bin genes by GC (20 bins), compute bin median of log(count/mu-depth-normalized)... realistic version without truth: bin median of log-CPM ratio vs global median; subtract per-gene offset.
- Metrics: (a) correlation of log-fold-change estimates with truth before/after correction on the 1900 non-DE genes (should stay ~0 / low bias); (b) DE recovery: fraction of GC-neutral DE genes with |logFC-1| <= 0.3 after correction; (c) fraction of GC-biased-high DE genes with |logFC-1| <= 0.3 (correction may overcorrect if DE genes shift the bin median - test).

## Gates
- G1: on non-DE genes, correlation between GC and estimated log-expression drops from > 0.9 (raw) to < 0.1 (corrected).
- G2: GC-neutral DE recovery >= 90% within tolerance after correction.
- G3: GC-biased-high DE recovery >= 70% after correction (bin median robust to 5% DE fraction).
- G4: raw (uncorrected) GC-neutral DE recovery >= 90% - shows bias is GC-specific, not global noise.
PASS if all.

## Failure policy
Negatives preserved; pivots via locked amendments.
