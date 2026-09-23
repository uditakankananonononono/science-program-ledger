# 006B GATES v2 — locked 2026-09-24 ~00:33 IST, BEFORE v2 results.
# Trigger: G1 v1 permutation PASSES (p=0.005, obs 0.585 > all 200 nulls) but the
# magnitude gate FAILS (CV AUROC 0.585 < 0.70). Real but weak linear predictability.
# v2 (pre-declared model arm): HistGradientBoostingClassifier (max_iter 300,
# learning_rate 0.05, max_depth 3, l2_regularization 1.0, frozen seed), same frozen
# features, same GroupKFold-by-complex protocol, same gates: CV mean >= 0.70 AND
# observed > ALL 200 full-pipeline permutation nulls. If v2 clears G1, the SAME v2
# model goes to the frozen 6AL5 evaluation (G2 >= 0.70 AUROC and >= +0.03 over the
# Parker-scale named baseline; G3 paratope sanity). If v2 also fails the magnitude
# gate: documented boundary for generic-scale epitope prediction, negatives preserved.
