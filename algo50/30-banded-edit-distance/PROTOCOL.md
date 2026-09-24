# algo50/30 - Banded vs full Levenshtein: correctness envelope and speedup

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study.

## Question
Banded edit-distance DP computes the exact distance only when the true distance fits the band. Map the correctness envelope: for random pairs and mutated copies at controlled divergence, when does banded == full, and what speedup does the band buy?

## Data (simulated, seed 1)
(a) 200 random pairs length 400 (expected distance ~large); (b) 200 pairs where B = A with substitutions+indels at total rate d in {0.05, 0.10, 0.20, 0.30}; length 400.

## Methods
- FULL: standard O(nm) Levenshtein DP (pure Python lists).
- BANDED(k): DP restricted to |i-j| <= k, k = ceil(d_est * n * 1.5) + 2 where d_est = the simulated divergence (oracle band); plus a self-tuning variant BAND-A: start k=8, double until the path stays inside the band (edge-touch test), max 512.
Metrics: fraction of pairs where banded distance == full distance; wall time ratio.

## Gates
- G1: BAND-A matches FULL on >= 99% of mutated pairs for d <= 0.20.
- G2: BAND-A wall time <= 30% of FULL at d=0.05 (per-pair median).
- G3: on random pairs, BAND-A still matches FULL on >= 95% (doubling absorbs large distances) OR returns "exceeds band" - either way no silent wrong answer: fraction of silent wrong answers = 0.
- G4: oracle BANDED at d=0.30 matches FULL >= 95%.
PASS if G1+G3; G2/G4 boundary.

## Failure policy
Negatives preserved; pivots via locked amendments.

---

# AMENDMENT 1 (locked before pivot scoring)
G3 failed: the "double until two successive results agree" stopping rule produced 1 silent wrong answer in 60 random pairs (both widths truncated identically).
Pivot P: BAND-P terminates when k >= d_k (the returned distance). Justification: an optimal path of cost d satisfies |i-j| <= d, so any band k >= d contains it; since banded results are overestimates (d_k >= d_true), k >= d_k implies exactness. 
- P1: BAND-P matches FULL on 100% of all pairs (mutated + random), zero silent wrong answers.
- P2: BAND-P median final band k <= 2x the true distance + 16 (efficiency sanity: band does not blow up to full width).
PASS if P1.
