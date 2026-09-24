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

---

# AMENDMENT 1 (locked before pivot scoring)
G3 failed, and root-cause analysis showed the artifact-test harness, not the masker: 50 orthologous and 5 spurious implants were placed at independent random coordinates, so later implants overwrote earlier ones (only 44/50 orthologs survived placement intact) and the kmer-set metric counted corrupted placements as masker errors. Masking itself removed 100% of low-complexity regions (G1) but the metric could not see it.
Pivot P: identical methods and gates, but implants are placed at guaranteed non-overlapping coordinates (shuffled gap allocation, min 50 bp separation), ortholog survival verified at placement time.
- P1: 50/50 orthologs intact post-placement; recall >= 95%; false-mask <= 2%.
- P2: spurious shared-kmer removal >= 95%; ortholog retention >= 49/50.
PASS if P1+P2.

---

# AMENDMENT 2 (locked before re-scoring)
Amendment 1's collision-free placements still failed: (a) ortholog and spurious position pools were drawn independently and could overlap (4/50 orthologs corrupted); (b) set-based kmer bookkeeping counts stochastic flank-extension kmers (implant + 1-3 matching flanking bases by chance, ~2/3 per implant) as phantom shares - an expected ~33 artifacts, not masker error.
Pivot P2: position-based bookkeeping. Ortholog retention = fraction of the 50 placed ortholog positions whose 25-mer is fully unmasked in BOTH sequences. Spurious removal = fraction of 25-mers fully inside spurious regions absent from the post-mask kmer sets. All implant coordinates (ortholog + spurious) allocated from one collision-free pool per sequence (min 50 bp separation, all 55 intervals disjoint).
- Q1: recall >= 95% and false-mask <= 2% (recomputed, unchanged methods).
- Q2: spurious removal >= 95% AND ortholog retention >= 49/50.
PASS if Q1+Q2.
