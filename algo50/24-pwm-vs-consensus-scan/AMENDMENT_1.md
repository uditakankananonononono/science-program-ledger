# algo50/24 - AMENDMENT 1: heterogeneous instance strength

Locked after original scoring (G1+G4 PASS - PWM AUROC +0.053 over consensus; G2 FAIL - TPR@1%FPR tied 0.245; G3 FAIL - weak-set edge +0.020 < 0.05), before heterogeneous-set results are inspected. Original gates stand; no re-thresholding of scored results.

## Method
Same background and scanning methods. New set (seed 2): per-instance strength multiplier U(0.55, 0.95) applied to the base match-probability profile (mixed strong and weak instances, the realistic case for a regulon). 200 planted / 200 not.

## Gates (locked)
- P1: PWM AUROC >= CONS AUROC + 0.05.
- P2: PWM TPR at 1% FPR >= CONS TPR at 1% FPR + 0.10.
Pivot PASSES if P1 and P2 pass.
