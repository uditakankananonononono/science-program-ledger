# ADDENDUM 1 (locked 2026-09-23 ~22:47 IST, before any outcome computation)
1. Condition: UNSTIMULATED cells only (frozen choice) - the TCR-stimulated condition is a
   different biological regime; mixing would confound. Stimulated analysis is a possible
   later experiment, not opened now.
2. Perturbation unit = target gene (guides pooled), per the gate's "targeting a gene".
3. If the h5ad X matrix is raw counts, normalize as CPM + log1p on selected genes only;
   if already log-normalized, use as-is. This is a data-format branch, not an outcome choice.
