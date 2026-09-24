# algo50/66 - Progressive MSA: does guide-tree order matter?

Lane RES-2. Algorithm study. Protocol + Amendments 1-2 hashed before the results they gate (`results/lock.txt`). Topic lane-chosen (no list past 55).

## Bottom line
Three-stage answer: (1) at low divergence (t=0.05) every order reaches >=0.95 SP accuracy - ordering is irrelevant; (2) at high divergence (t=0.30) progressive alignment collapses to ~10% SP accuracy for EVERY order, true tree included - ordering cannot rescue a broken regime; (3) at intermediate divergence (t=0.15) order-to-order spread (0.09-0.16 within one dataset) dwarfs any systematic true-order advantage (mean gap +0.01 over 3 seeds, gate +0.02 not met). Practical conclusion: guide-tree refinement is second-order; the high-divergence collapse is the dominant failure mode of progressive alignment.

## Gates
- Original (seed 29): G1 FAIL (random orders beat true at t=0.05), G2 FAIL (gap at t=0.30 = -0.01; the +0.077 gap appeared at t=0.15 instead), G3 PASS.
- Amendment 1 (seed 31): P1 FAIL (gap not replicated: -0.004), P2 PASS (collapse replicated, all orders <= 0.146), P3 PASS (easy regime + order-independence).
- Amendment 2 (seeds 41/43/45): Q1 FAIL (mean gap +0.010 < 0.02), Q2 PASS (spread >= 0.05 in 3/3), Q3 informational (3/3 gaps positive but tiny).
Net: documented negative on the systematic ordering effect; robust positives on the two regime boundaries.

## Data
Simulated evolution (subs JC69-ish rate t, indels at 0.1t geometric) on 8 sequences, root length 300; true alignment from simulation columns. Progressive profile alignment (sum-of-pairs +2/-1/-2) in true vs 5 random leaf orders.

## Caveats
- The evolution tree is approximated by equal-depth independent 2-edge paths per cherry pair (documented in code); a shared-trunk tree would give sequences more shared signal and possibly a larger ordering effect.
- SP accuracy counts only columns where both sequences have residues; insertion columns excluded.

## Reproduce
`python3 code/run.py` (seed 29), `code/pivot.py` (seed 31), `code/pivot2.py` (seeds 41/43/45; gate print bug - scores computed from results/pivot2_metrics.json, bug documented). numpy only; ~5 min total.
