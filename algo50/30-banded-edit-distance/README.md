# algo50/30 - Banded vs full Levenshtein: correctness envelope and speedup

Lane RES-2. Algorithm study. Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`).

## Bottom line
A fixed oracle band matches full DP 100% at all divergences tested (0.05-0.30) and runs at 15-22% of full-DP wall time. But the intuitive self-tuning rule "double the band until two successive results agree" is UNSOUND: 1/60 random pairs returned a silently wrong distance (both band widths truncated the same way). The pivot rule - terminate when the band k >= the returned distance d_k - is provably exact (any optimal path of cost d stays within |i-j| <= d, and banded results overestimate: k >= d_k implies exact) and matched full DP on 300/300 pairs with median final band only 1.19x the true distance.

## Data
Simulated (seed 1): 60 mutated pairs/level at d in {0.05,0.10,0.20,0.30}, length 400; 60 random pairs.

## Gates
- Original: G1 PASS (100% match d<=0.20), G2 PASS (15% wall time), G3 FAIL (1 silent wrong answer, rule unsound), G4 PASS (oracle band 100% at d=0.30).
- Pivot (Amendment 1): P1 PASS (300/300 exact), P2 PASS (median k/d = 1.19).
Original FAILS on G3; pivot PASSES. Net: banded edit distance is exact and ~5-6x faster when the termination rule is k >= returned distance, not "stable across doublings."

## Caveats
- Pure-Python DP; absolute times inflated, ratios meaningful.
- The provable rule needs banded results to be overestimates of the true distance (true for a truncated minimization DP on the same recurrences).

## Reproduce
`python3 code/run.py && python3 code/pivot.py` (stdlib only, ~2 min).
