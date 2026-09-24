# algo50/38 - Benjamini-Hochberg vs Bonferroni in genome-scale testing

Lane RES-3. Algorithm study. Protocol hashed before scoring (`results/lock.txt`).

## Bottom line
- With 1,000 tests and 100 true signals (shift 3 SD), BH at q=0.05 finds 61% of true signals vs 18% for Bonferroni (3.4x), while keeping FDR at 4.3%.
- Under strong positive correlation (rho=0.5) BH FDR stays at 3.9%, consistent with PRDS theory.
- Uncorrected p<0.05 finds 91% but a third of its hits are false (FDR 33%).

## Results (results/results.json, 500 replicates each)
| regime | method | FDR | power |
|---|---|---|---|
| independent | UNC | 0.327 | 0.914 |
| independent | BONF | 0.004 | 0.182 |
| independent | BH | 0.043 | 0.612 |
| rho=0.5 | UNC | 0.197 | 0.918 |
| rho=0.5 | BONF | 0.0004 | 0.195 |
| rho=0.5 | BH | 0.039 | 0.587 |

## Gates
| gate | rule | value | verdict |
|---|---|---|---|
| G1 | indep BH FDR <= 0.055 | 0.043 | PASS |
| G2 | indep BH power >= 2x BONF | 0.612 vs 0.182 | PASS |
| G3 | rho=0.5 BH FDR <= 0.055 | 0.039 | PASS |
| G4 | indep UNC FDR >= 0.20 | 0.327 | PASS |
Project PASSES (all gates). This is a reproduction of a known result, not a new method.

## Caveats
- Only the mean FDR is gated; under correlation the per-replicate false discovery proportion is much more variable (not reported as a gate).
- Single effect size, single signal fraction (10%); BH gain shrinks as signals get sparser.
- Simulated Gaussian z-scores, one-sided; real screens have heavier tails and nonuniform nulls.

## Reproduce
`python3 code/run.py` (numpy, scipy; ~5 s).
