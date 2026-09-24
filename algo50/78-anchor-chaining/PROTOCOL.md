# algo50/78 - Colinear anchor chaining: DP vs greedy under spurious anchors

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55).

## Question
Minimap2-style chaining: given anchor matches (x=read pos, y=ref pos, len), find the best colinear chain. Greedy (take anchors in score order if colinear) vs full DP (max weight colinear chain): how much does greedy lose as spurious-anchor rate rises?

## Data (simulated, seed 71)
Read 2kb vs reference region: true chain = 30 anchors on a diagonal (with jitter +-20bp, inversions: 3 anchors on a shifted diagonal to model a small rearrangement). Spurious anchors: rate r in {0, 0.2, 0.5, 1.0} x #true, random positions, length 15-25. 200 replicates per r.

## Methods
- Anchors: (x, y, w=len). Colinear: x increasing AND y increasing.
- DP: sort by x; dp[i] = w_i + max over j<i colinear (with gap penalty -0.02*max(0,|(dx)-(dy)|-50) to prefer diagonal-consistent); O(n^2) fine at n<=60.
- Greedy: sort by w desc; accept if colinear with accepted set.
- Metric: fraction of TRUE anchors in chosen chain (recall) and spurious fraction (precision).

## Gates
- G1: DP recall >= 0.90 at r <= 0.5.
- G2: DP precision >= 0.95 at r <= 0.5.
- G3: greedy recall <= DP recall - 0.05 at r = 0.5 or 1.0 (greedy loses measurably somewhere).
- G4: DP recall at r=1.0 >= 0.75 (robustness).
PASS if G1+G2+G4; G3 boundary.

## Failure policy
Negatives preserved; pivots via locked amendments.
