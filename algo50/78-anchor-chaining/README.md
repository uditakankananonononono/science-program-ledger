# algo50/78 - Colinear anchor chaining: DP vs greedy under spurious anchors

Lane RES-2. Algorithm study. Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`). Topic lane-chosen (no list past 55).

## Bottom line
DP chaining clearly beats greedy (P3: recall gap 0.16-0.19 at r=0.5/1.0, precision gap ~0.10) and holds precision >= 0.95 up to r=0.5 (G2). But two naive expectations failed: (1) weight-maximizing DP does NOT cleanly reject a 3-anchor rearrangement - only 62-70% of replicates exclude the shifted anchors, because the diagonal-consistency penalty (~5) is cheaper than a long anchor (~20): chains absorb rearrangements when the anchors are long; (2) even with zero spurious anchors, recall caps at ~0.86 - positional jitter (+-20bp) makes adjacent anchors mutually non-colinear. Both are documented boundaries on "chaining solves it."

## Gates
- Original (seed 71): G1 FAIL (0.80 < 0.90: structural cap from 3 shifted + jitter), G2 PASS, G3 PASS, G4 PASS.
- Amendment 1 (seed 73, recall over non-rearranged anchors + rejection metric): P1 FAIL (0.86 < 0.90: jitter cost), P2 FAIL (rejection 62-70% < 80%), P3 PASS (greedy gap at both r).
No third amendment: the rejection-vs-penalty balance is the finding; re-gating it would tune to seen data.

## Data
Simulated (seeds 71, 73): 2kb read, 30 true anchors (+-20bp jitter, 3 on a +300 shifted diagonal), spurious anchors at rate r x 30, 200 replicates per r.

## Caveats
- One penalty setting tested; minimap2's actual heuristic tunes gap costs to read length and identity.
- Rearrangement modeled as a 3-anchor +300 shift; larger structural variants need explicit split-alignment logic.

## Reproduce
`python3 code/run.py` (seed 71), `code/pivot.py` (seed 73); numpy only, <1 min.
