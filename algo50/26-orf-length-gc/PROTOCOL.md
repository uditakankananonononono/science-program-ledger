# algo50/26 - Stop codons are AT-rich: does genome GC predict random-ORF length?

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study.

## Question
Stop codons (TAA, TAG, TGA) average 22% GC. In GC-rich genomes stops should be rarer and random ORFs longer. Does a mononucleotide-only iid model predict mean stop-to-stop ORF length across four genomes spanning 43-66% GC, and does it predict the length of real shadow ORFs (algo50/04 negatives)?

## Data
Genomes: NC_000913.3 (E. coli), NC_004741 (S. flexneri), NC_000964.3 (B. subtilis), NC_000962.3 (M. tuberculosis) - same GenBank files as algo50/04+10 (sha256 in data/). Shadow ORF lengths from algo50/04 data/sets.json (neg set, length-matched - noted as biased sample; used only for G3's bracket check with that caveat).

## Methods
- Prediction: P_stop = pT*pA*pA + pT*pA*pG + pT*pG*pA from genome mononucleotide frequencies; predicted mean ORF (codons) = 1/P_stop.
- Observed: mean stop-to-stop distance (codons) over the three forward frames of each genome (stop-bounded segments, both ends).
- Shadow: mean length (codons) of the algo50/04 shadow-ORF negative sets per genome.

## Gates
- G1: |observed/predicted - 1| <= 0.25 for all four genomes.
- G2: observed M.tb/E. coli ratio within +/-25% of predicted ratio.
- G3: shadow mean within [0.5x, 2x] of the random prediction per genome (4/4).
PASS if G1+G2; G3 boundary.

## Failure policy
Negatives preserved; pivots via locked amendments.

## Notes locked in advance
- The 04 negative set is length-matched to CDS, so G3 tests the bracket not exact equality; documented bias.
- Dinucleotide effects (e.g. TpA depletion) are the expected failure source for an iid model.
