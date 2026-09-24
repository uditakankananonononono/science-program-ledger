# algo50/56 - de Bruijn assembly: contig N50 vs k, and the repeat-resolving limit

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study.
NOTE: no topic list exists past 55; topics for 56+ are lane-chosen (per main 13:50 IST) and documented here.

## Question
For single-end error-free reads, how does contig N50 from a de Bruijn graph depend on k, and does the empirical collapse point match the repeat structure of the genome (maximal exact repeat length R: k must exceed R to resolve it)?

## Data (simulated, seed 11)
Genome: 120 kb random base + 8 implanted exact repeats of lengths {200, 400, 800, 1600, 3200, 6400, 300, 500} at random positions (second copy, same orientation). Reads: every position, length 100, error-free (perfect double-stranded coverage; single strand).

## Methods
Build de Bruijn graph of k-mers from reads for k in {15, 21, 31, 51, 75, 99}: nodes = (k-1)-mers, edges = k-mers; unitigs = maximal non-branching paths. N50 over unitigs. Record: N50(k), number of unitigs, and for each repeat whether it creates a branch (unresolved) at each k.
Theory: a repeat of length R is resolvable iff k > R (unique flanking context enters the k-mer). Predict collapse: repeats longer than k-1 stay tangled.

## Gates
- G1: N50(k) is non-decreasing in k over the tested range within 10% tolerance (monotone-ish upward).
- G2: at k=99 (all repeats < 99? no - repeats up to 6400), correct behavior is: repeats with R >= k produce branching. Verify: fraction of repeats with R >= k that produce a branch >= 90% at every k <= 51.
- G3: N50 at k=15 <= 20% of N50 at k=99 (large dynamic range shows repeat-limited assembly).
- G4: genome fraction covered by unitigs >= 99% at all k (no sequence lost).
PASS if G2+G4 plus one of G1/G3.

## Failure policy
Negatives preserved; pivots via locked amendments.
