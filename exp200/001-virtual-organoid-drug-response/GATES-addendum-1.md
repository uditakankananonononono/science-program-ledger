# GATES ADDENDUM 1 (locked 2026-09-23 ~21:52 IST, before any model evaluation or R^2 inspection)

1. Drug-panel rule correction applied literally: ">=300 cell lines having BOTH IC50 and
   expression" — panel selection happens AFTER the GDSC2 x DepMap expression join, not on
   IC50 counts alone. (An IC50-only provisional count was computed for plumbing checks
   only; no model was fit and no outcome metric was inspected from it.)
2. Permutation null: to fit the compute budget, each permutation reuses the outer-fold
   alpha selected on real labels (standard practice); inner CV is not re-run per
   permutation. Declared before use.
3. G2 class mapping (frozen): PATHWAY_NAME in {DNA replication, mitosis, genome integrity,
   metabolism} = CYTOTOXIC; all other pathway classes = TARGETED. Applied to the panel's
   PATHWAY_NAME values; drugs with missing pathway are excluded from G2 only.
4. CV R^2 per drug uses out-of-fold predictions pooled across the 5 folds.
