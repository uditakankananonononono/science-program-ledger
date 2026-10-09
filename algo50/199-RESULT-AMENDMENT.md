# 199 RESULT - AMENDMENT 1 (wording; original 199-RESULT.md unchanged)
Applied after the verification lane's independent rerun, which matched every published key.
1. F: the 95% CI of the label-free stack minus fba_min is [-0.053, 0.013] and includes 0. Read the F line as: no evidence that label-free stacking beats fba_min (point estimate lower, CI includes 0). The statement that the ensemble's gain over fba_min comes from the supervised GNN/CNN/k-mer layers is an inference from F; it is consistent with F, not proved by it. Replace "adds nothing" with the wording above.
2. "The stacker that made the committed ensemble is undocumented" applies to the v1 stacker only (no script in the repo regenerates results/ensemble_oof.csv). The later v2 stacker scripts exist.
3. The A2 window (+-0.01) was set blind. A miss of +0.041 in the favourable direction is a failed reproduction of the committed number, not evidence the ensemble is "better than claimed".
4. data/gerdes_labels.csv contains one conflicting duplicate bnumber (b2088). It is not among the 1,249 genes of the aligned file (checked), so it did not affect A1.
Ledger-summary sentence to keep verbatim: all of the ensemble's gain over FBA is consistent with coming from supervised layers whose leakage vs the stacker is unquantified.
