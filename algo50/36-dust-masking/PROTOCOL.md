# algo50/36 - DUST-style low-complexity masking

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study.

## Question
Does a DUST-style triplet-complexity scorer recover implanted low-complexity regions at high sensitivity with low false-masking, and does masking remove spurious high-scoring self-similarity hits?

## Data (simulated, seed 7)
Background: 200 kb iid uniform DNA. Implant 40 low-complexity regions (len 100-600): 20 homopolymer/dinucleotide/tandem-motif repeats, 20 partial-bias regions (one base at 70%). Also 20 kb of pure random sequence as negative control.

## Methods
DUST-style: sliding window w=64, score = sum over triplet counts of c*(c-1)/2 scaled by window; threshold chosen at score > mean + 3*sd measured on a held-out 20 kb random pilot (threshold fixed before test scoring - recorded in results). Mask windows above threshold (merge overlapping).
Metrics: per-region recall (>=50% of region bases masked = detected), false-mask fraction on negative control, and alignment artifact test: count of exact 25-mer matches between two unrelated 50 kb sequences (a) unmasked vs (b) after masking, where 5 spurious low-complexity-mediated match clusters are implanted in low-complexity segments.

## Gates
- G1: recall >= 95% of 40 implanted regions.
- G2: false-mask fraction on negative control <= 2%.
- G3: masking removes >= 95% of spurious 25-mer matches while removing <= 1% of a set of 50 implanted orthologous 25-mers in high-complexity regions.
PASS if all three.

## Failure policy
Negatives preserved; pivots via locked amendments.
