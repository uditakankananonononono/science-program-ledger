# GATES ADDENDUM A — locked 2026-09-24 ~02:55 IST, BEFORE any valid G1 metrics.
# (The 02:31 g1_yeast8*.json files came from the invalid prototype scan, are
#  marked INVALID, and will be overwritten by the corrected pipeline.)

- A1 SOLVER: FBA solved with scipy.optimize.linprog (HiGHS dual simplex) instead of
  cobrapy's GLPK binding. Rationale: GLPK reproducibly HANGS (no return, >100 s) on
  specific knockout LPs - first found at gene YDR044W (HEM13) - stalling the scan.
  Equivalence verified BEFORE use: WT objective Yeast8 = 0.0811 under BOTH solvers
  (cobra/GLPK 0.0811 vs HiGHS 0.0811). Per-solve time_limit = 20 s.
- A2 GPR-AWARE KNOCKOUT: deleting gene g disables reaction r ONLY IF r's GPR rule
  evaluates False when g is set absent (cobra gpr.eval). Isozymes (OR rules) keep a
  reaction active. This supersedes the naive prototype (disable ALL reactions touching
  the gene), which over-disables isozyme reactions: prototype results/g1_yeast8_parts.json
  (275 genes) is DISCARDED and the full scan is rerun GPR-aware.
- A3 UNSOLVABLE RULE: a KO LP not returning optimal within 20 s is marked
  'unsolvable' and EXCLUDED from scoring for BOTH models (same gene removed from the
  common comparison set), with IDs reported in RESULTS. If unsolvable genes exceed 5%
  of the common scored set, G1 is an integrity FAIL -> documented boundary.
- A4 Essentiality threshold UNCHANGED from GATES.md: KO growth < 1% of WT growth =>
  predicted essential.
- A5 Truth set UNCHANGED: results/sgd_truth.json (6,266 genes) built before this addendum.
- A6 Common comparison set for G1 = intersect(Yeast8 genes, iMM904 genes, SGD truth,
  minus unsolvable). Yeast8 BA on its own wider intersect reported secondarily.
