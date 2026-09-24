# algo50/24 - PWM log-odds vs consensus best-match for motif scanning

Lane RES-2. Algorithm study. Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`).

## Bottom line
- PWM beats consensus consistently but modestly: AUROC 0.872 vs 0.819 on uniform-strength instances (G1 PASS, +0.053; G4 PASS), and under heterogeneous instance strength 0.617 vs 0.599 with TPR@1%FPR 0.094 vs 0.053 (+77% relative).
- But the locked margin gates mostly FAIL: TPR@1%FPR ties on the uniform set (0.245 both), the weak-set edge is +0.020 (gate +0.05), and the heterogeneous-set margins miss too (P1+P2 FAIL). The PWM edge is real but small; it does not blow consensus matching away at any operating point tested.
- Lesson: when instances are uniformly strong, a consensus string already captures most of the signal; PWM's advantage concentrates in weak/heterogeneous instances and mid-ROC operating points.

## Data
Simulated: 400x500 bp iid GC 0.45 background; 8-mer motif CACGTGCA, match-probability profile 0.62/0.80/0.95/0.98/0.98/0.95/0.80/0.62; 200 planted/200 not; standard (scale 1.0), weak (0.85x uniform), heterogeneous (per-instance U(0.55,0.95), seed 2).

## Gates
- G1 PASS (+0.053). G2 FAIL (0.245 = 0.245). G3 FAIL (+0.020 < +0.05). G4 PASS (0.872 >= 0.85).
- Pivot (heterogeneous): P1 FAIL (+0.018), P2 FAIL (+0.041 < +0.10).

Original FAILS G2/G3; pivot FAILS P1/P2. Documented: PWM > consensus in direction everywhere, below gated margins in magnitude.

## Caveats
- One motif shape, one background GC, one length; effects are motif-specific.
- AUROC over sequence-max scores; per-site scanning (the production setting) has a different FPR geometry.
- PWM used the true generative probabilities (oracle); a learned PWM from few sites would do worse.

## Reproduce
`python3 code/run.py` (needs numpy, scikit-learn; ~1 min).
