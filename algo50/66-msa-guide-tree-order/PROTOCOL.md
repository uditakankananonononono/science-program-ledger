# algo50/66 - Progressive MSA: guide-tree order effect on alignment quality

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55).

## Question
Progressive alignment (Clustal-style) merges sequences along a guide tree; errors propagate. Does aligning in true-tree order beat random-leaf order, and does the gap grow with divergence?

## Data (simulated, seed 29)
Birth-death-free approach: 8 sequences evolved on a fixed balanced tree ((1,2),(3,4)),((5,6),(7,8)) with branch length t per edge, t in {0.05, 0.15, 0.30} (JC69 substitutions, no indels - isolates the ordering effect from indel placement). Root sequence length 300. True alignment = the evolved columns (no indels => trivially known).

## Methods
- Pairwise identity from unaligned? With no indels, "alignment" is column identity; instead simulate WITH indels: indel rate 10% of substitution rate, length geometric(0.5). True alignment recorded during simulation.
- Progressive MSA: pairwise edit-distance-based UPGMA guide tree from k-mer distances (k=3, Jaccard), then star-progressive alignment by guide order using pairwise NW profile alignment (sum-of-pairs +2/-1/-2, profile = column frequencies).
- Compare: guide order = TRUE tree vs 5 random leaf orders.
- Metric: sum-of-pairs accuracy vs true alignment (fraction of true homologous column pairs recovered).

## Gates
- G1: true-order accuracy >= random-order accuracy in >= 4/5 random comparisons at every t.
- G2: gap (true minus mean random accuracy) at t=0.30 >= 0.05 (matters at high divergence).
- G3: at t=0.05 all orders >= 0.95 accuracy (easy regime sanity).
PASS if all.

## Failure policy
Negatives preserved; pivots via locked amendments.

---

# AMENDMENT 1 (locked before pivot run on FRESH seed 31)
Original G1+G2 failed as locked, and the pattern is the finding: the guide-order effect is non-monotone in divergence - nothing to lose at t=0.05 (random orders slightly WIN, 0.972 vs 0.956), a real +0.077 gap at t=0.15, and total collapse at t=0.30 (~10% SP accuracy for ALL orders - progressive alignment itself breaks, order irrelevant).
Pivot P (fresh seed 31, same simulator):
- P1: true-order accuracy - mean(random-order accuracy) >= +0.03 at t=0.15.
- P2: at t=0.30, accuracy <= 0.20 for true AND all random orders (collapse replicated).
- P3: at t=0.05, all orders >= 0.95 (easy regime; order-independence: |true - mean random| <= 0.03).
PASS if all.

---

# AMENDMENT 2 (locked before pivot run on FRESH seeds 41/43/45)
Amendment 1's P1 failed: the +0.077 true-order gap at t=0.15 (seed 29) did not replicate on seed 31 (-0.004). Within-seed order-to-order spread (~0.10 between random orders) exceeds any systematic true-order advantage - the effect, if real, is smaller than run noise. P2+P3 passed and stand.
Pivot Q (seeds 41,43,45; t=0.15 only; true order + 5 random orders per seed):
- Q1: mean gap (true - mean random) over 3 seeds >= +0.02.
- Q2: within-seed random-order spread (max-min) >= 0.05 in >= 2/3 seeds (variance dominance).
- Q3: gap positive in >= 2/3 seeds.
PASS if Q1+Q2; Q3 reported.
