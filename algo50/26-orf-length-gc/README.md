# algo50/26 - Stop codons are AT-rich: does genome GC predict random-ORF length?

Lane RES-2. Algorithm study. Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`).

## Bottom line
- Direction confirmed and quantified: mean stop-to-stop ORF length grows with genome GC (B. subtilis 43.5% GC: 20.9 codons; E. coli/Shigella 51%: 24.8/25.0; M. tuberculosis 66%: 52.0), and the mononucleotide model predicts the mtb/ecoli ratio (1.87) within 12% of observed (2.09).
- But the iid model underpredicts length 13-27% (worst at extreme GC) - G1 FAILS narrowly on M. tuberculosis (1.27 vs 1.25 gate). Dinucleotide correction (TpA depletion means fewer stops) flips to slight overprediction and passes: ratios 0.88-0.98 (P1 PASS), ratio-of-ratios within 10% (P2 PASS).
- Shadow ORFs (stop-free, >=150 nt, containing no CDS) average 105-123 codons - 2.3-4.5x the corrected random prediction (P3 FAIL): living between genes is not explained by stop statistics; coding-in-other-frames structure dominates.
- G3 as locked was void by construction (the 04 negative set is CDS-length-matched) - documented, superseded by P3 on freshly enumerated shadows.

## Data
NC_000913.3, NC_004741, NC_000964.3, NC_000962.3 GenBank (sha256 `data/SHA256_raw.txt`); stop-spacing over forward frames; shadow ORFs enumerated as in algo50/04.

## Gates
- G1 FAIL (mtb 1.27 > 1.25; others within). G2 PASS (2.09 vs 1.87). G3 FAIL (void by construction, documented).
- Pivot: P1 PASS, P2 PASS, P3 FAIL (shadows 2.3-4.5x prediction).

Original FAILS G1/G3; pivot PASSES P1/P2. Net: GC sets the stop budget, dinucleotides set the correction, and shadow-ORF length is a selection/structure phenomenon, not a stop-statistics one.

## Caveats
- Forward frames only for stop spacing (strand-symmetric in expectation).
- The dinucleotide model ignores codon-level correlations beyond nearest neighbor.
- Shadow ORF definition (no CDS wholly inside) biases toward intergenic-ish ORFs; alternative definitions shift the mean.

## Reproduce
`python3 code/run.py` (needs biopython, numpy; ~2 min).
