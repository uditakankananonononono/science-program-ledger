# algo50/14 - Shine-Dalgarno signal at annotated starts vs shadow ORF starts

Lane RES-2. Algorithm study (not counted toward the flagship 100). Protocol hashed and timestamped before scoring (`results/lock.txt`).

## Bottom line
- The plain AGGAGG best-match count in -20..-5 separates real translation starts from shadow-ORF starts at AUROC 0.79 (E. coli) and 0.92 (B. subtilis), with 26%/66% of real starts carrying a >=5/6 match at 8x/17x the shadow rate. Primary gates PASS.
- Position gate narrowly FAILS: the signal is enriched 1.37x over the -60..-45 control window (gate 1.5x) - the SD signal spreads broader than the canonical window rather than sitting tightly in it.
- Boundary (not gated): M. tuberculosis AUROC only 0.66 with mean score 3.71 - visibly weaker SD usage, consistent with its leaderless/atypical translation initiation reports.

## Data
NC_000913.3, NC_000964.3, NC_000962.3 GenBank (sha256 `data/SHA256_raw.txt`; same accessions as algo50/04). Positives: 100 nt upstream of annotated CDS starts; negatives: upstream of shadow-ORF 5' ends (>=150 nt ORFs containing no annotated CDS), 1:1 seed-1 subsample.

## Results (results/results.json)
| genome | M1 AUROC (-20..-5) | M2 AUROC (control) | frac >=5/6 real | frac >=5/6 shadow | mean M1 | mean M2 |
|---|---|---|---|---|---|---|
| E. coli | 0.788 | 0.478 | 0.259 | 0.031 | 3.97 | 2.88 |
| B. subtilis | 0.924 | 0.505 | 0.664 | 0.038 | 4.79 | 2.92 |
| M. tuberculosis | 0.661 | 0.483 | 0.209 | 0.034 | 3.71 | 3.13 |

## Gates
- G1 PASS: E. coli M1 AUROC 0.788 >= 0.70.
- G2 PASS: 0.259 >= 2x 0.031.
- G3 FAIL: mean M1/M2 ratio 1.375 < 1.5 (SD signal broader than the canonical window).
- G4 PASS: B. subtilis 0.924 >= 0.65. M. tuberculosis 0.661 reported as boundary.

Project PASSES (G1+G2).

## Caveats
- Shadow ORF starts are stop-to-stop 5' ends, not true start-codon candidates; a harder negative set would be in-frame ATGs inside real genes.
- Match-count to a single consensus is the crudest scorer; spacing-aware or energy-based scorers were not tested.
- Upstream windows truncated at contig edges drop a few loci.

## Reproduce
`python3 code/run.py` (needs biopython, numpy, scikit-learn; ~1 min).
