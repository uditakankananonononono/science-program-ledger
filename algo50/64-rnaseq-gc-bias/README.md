# algo50/64 - RNA-seq GC bias: detection and conditional-median correction

Lane RES-2. Algorithm study. Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`). Topic lane-chosen (no list past 55).

## Bottom line
Conditional-median GC correction works for ABSOLUTE expression: GC-expression correlation drops 0.32 -> 0.01 and median |error| halves (0.43 -> 0.24 log2). But condition-independent GC bias CANCELS in differential analysis - raw log-fold-changes are already GC-unbiased, so correction is irrelevant (not harmful) for DE calls. The one real LFC distortion found is compositional: up-regulated DE genes inflate the treatment library, shrinking their own measured fold change by ~0.1 log2 (raw median LFC 0.84 vs true 1.0, P3 FAIL) - the known reason TMM/spike-in normalization exists, and NOT fixable by GC correction.

## Gates
- Original (seed 23): G1 FAIL (raw GC correlation 0.32, gate assumed >0.9 - lognormal expression spread dominates), G2/G3/G4 FAIL (+-0.3 LFC tolerance is noise-limited at 3 NB replicates: 46-50%). Gates miscalibrated, documented.
- Amendment 1 (fresh seed 24, re-aimed gates): P1 PASS (0.32->0.013), P2 PASS (non-DE within-0.3 recovery 1.7x), P3 FAIL (compositional shrinkage ~0.1 log2, documented above), P4 PASS (no error inflation).
Original FAILS on miscalibration; pivot PASSES except the genuinely-failing P3, which is the project's second finding.

## Caveats
- Single bias curve exp(3(GC-0.5)); real bias is sample-specific and fragment-length-dependent.
- Bin-median correction assumes <50% DE per GC bin (5% here); heavy DE+GC confounding breaks it (known failure mode, not triggered here).

## Reproduce
`python3 code/run.py` (original, seed 23) and `python3 code/pivot.py` (seed 24); numpy only, <30 s.
