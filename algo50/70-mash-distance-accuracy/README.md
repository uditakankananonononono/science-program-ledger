# algo50/70 - Mash-style k-mer distance: accuracy vs true divergence

Lane RES-2. Algorithm study. Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`). Topic lane-chosen (no list past 55).

## Bottom line
One variable explains the whole accuracy landscape: E = L(1-p)^k, the expected shared k-mer count. |median error| <= 0.005 when E >= 10000; 0.009-0.014 at E ~ 4000-8000; up to 0.023 at E ~ 1800; and the estimator SATURATES to +inf (zero shared k-mers, log 0) only when E ~< 3 - not at the originally gated E <= 50 (Poisson: with E=24 expected shared, P(zero) ~ e^-24 ~ 0). Monotone-in-p at every k where finite. Two locked gate sets failed on boundary miscalibration; the dose-response itself is crisp and reported as the finding.

## Gates
- Original (seed 43): G1 FAIL (err 0.0143 at p=0.15/k=21 vs 0.01 gate), G2 FAIL (ties at +inf), G3 FAIL with wrong predicted DIRECTION (saturation is +inf, not underestimation), G4 PASS (k=31 error > k=11 at p=0.30).
- Amendment 1 (seed 47, E-regime gates): P1 FAIL (E~1800 cells err 0.023 > 0.02), P2 FAIL (E<=50 cells mostly NOT saturated; true threshold E~<3), P3/monotone PASS at all k.
Stopping re-gating here per protocol discipline: further E-boundary amendments would be tuned to seen data. The E dose-response stands as the reported result.

## Data
Simulated (seeds 43, 47): 50 kb random ancestor, descendants at p in {0.01..0.40}, 20 replicates, full k-mer sets (no sketching), k in {11,15,21,31}.

## Caveats
- Full k-mer sets; MinHash sketching adds sampling variance on top (not tested).
- Independent-site substitutions only; clustered mutations would break the (1-p)^k conservation model.

## Reproduce
`python3 code/run.py` (seed 43), `code/pivot.py` (seed 47); numpy only, ~1 min each.
