# Amendment 1 - pivot to prefilter cascade (locked before cascade results were computed)

## Outcome of the original protocol (not re-scored, not re-tuned)
G1 FAIL (RA-SP +4.4 points over MH3, needed +5; McNemar p=0.0002), G2 FAIL (+6.0 twilight, needed +10), G3 FAIL (69% of SW accuracy). The primary hypothesis - that reduced-alphabet spaced-seed sketches substitute for alignment - is rejected. Every alignment-free method collapses in the twilight stratum (20-30% vs SW 85%).

## New direction
Alignment-free sketches are not a replacement for SW, but they may be a cheap candidate generator. Question: using a sketch similarity to shortlist the top-k references per query, then SW-reranking only those k, how small can k be while keeping near-SW accuracy, and does the spaced-seed reduced alphabet shrink k relative to plain MinHash?

Cascade(method, k): for each query, take the k most sketch-similar references (excluding itself), assign the family of the one with the highest normalised SW score. Same data, same LOO, same SW matrix.
k grid: 1,2,3,5,10,20,30,50,100,200.
Reported: accuracy vs k, twilight accuracy vs k, recall@k of any same-family member.

## Gates (A = amendment)
- A1: Cascade(RA-SP) reaches >= 0.95 x SW accuracy (>= 0.8811) at some k <= 50 (<= 5% of the all-vs-all alignments).
- A2: The smallest grid k reaching 0.8811 for RA-SP is <= 0.7 x the smallest such k for MH3 (if MH3 never reaches it within the grid, A2 passes if RA-SP does).
- A3 (twilight): Cascade(RA-SP) twilight accuracy at k=50 >= 0.95 x SW twilight accuracy (>= 0.803).
Failure policy unchanged.
