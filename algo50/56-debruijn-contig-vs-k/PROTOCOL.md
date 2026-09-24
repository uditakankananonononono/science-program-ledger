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

---

# AMENDMENT 1 (locked before pivot scoring)
G3+G4 failed for theory reasons, not implementation: (a) the 8 implanted repeats (200-6400 bp) exceed every tested k (15-99), so none resolve anywhere in the original range and N50(k) is nearly flat - the interesting dynamics need k spanning the repeat lengths; (b) G4's >=99% genome-fraction gate ignored that collapsed repeats are represented once by construction (sum of unitig lengths / genome length caps at ~1 - repeat_fraction = 0.89 here).
Pivot P: k in {15, 51, 99, 250, 600, 1500, 7000} (spanning all repeat lengths); hash-based graph (64-bit rolling hash) for the large k.
- P1: unresolved-repeat count == #{implanted repeats with R >= k} exactly at every k.
- P2: N50 strictly increases whenever k crosses a repeat length (k=99 -> 250 -> 600 -> 1500 -> 7000 each cross >= 1).
- P3: corrected coverage - sum(unitig lengths) / (genome length - collapsed repeat copies) >= 99% at every k.
PASS if P1 + P3, P2 boundary.

---

# AMENDMENT 2 (locked before re-scoring)
Amendment 1 scored with two measurement defects (documented, not hidden): (a) the unresolved-repeat probe placed the test k-mer at a+R/2, which falls OUTSIDE the repeat when R < 2k - undercounting unresolved repeats at mid k (5 vs 7 at k=250); correct probe position is a + (R-k)//2; (b) the corrected-coverage formula lacked the per-unitig (k-1) length padding, giving impossible values > 1.
Amendment 2: probe fixed; P3 replaced by a crisp endpoint criterion that needs no coverage invariant.
- P1: unresolved-repeat count == #{R >= k} exactly at every k in {15,51,99,250,600,1500,7000} (fixed probe).
- P2: N50 strictly increases at each repeat-length crossing (99->250->600->1500->7000). (scored under Amd 1: PASS - 18.0k, 18.3k, 31.9k, 33.7k, 120.0k)
- P3: at k=7000 (exceeds the longest repeat, 6400) the assembly is a single contig (n_unitigs == 1).
PASS if P1+P3.
