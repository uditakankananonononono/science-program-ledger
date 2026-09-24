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
