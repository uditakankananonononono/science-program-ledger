# GATES v2 — PIVOT for failed G2 (locked 2026-09-23 ~22:17 IST, after G2 FAIL,
# before any pivot-direction computation)
G2 result (honest negative): targeted vs cytotoxic per-drug predictability does NOT
differ (median CV R^2 0.376 vs 0.369, Mann-Whitney p=0.187). Pathway class does not
explain which drugs are predictable.

Pivot question (new direction): is the expression signal just lineage in disguise?
A lineage-detector model would be a weak, confounded claim; quantifying the
extra-lineage margin per drug turns the G1 result into a defensible measured property
and a boundary map.

## Locked pivot gates
- P1: lineage-only model (one-hot TCGA_DESC + ridge, same 5-fold line-disjoint CV,
  same panel) achieves median relative RMSE reduction vs drug-mean baseline; GATE PASS
  requires expression model's median reduction (0.211, already computed under G1) to
  exceed the lineage-only median by >= 5 absolute points.
- P2: per-drug extra-lineage margin (expression rel. reduction minus lineage-only rel.
  reduction) > 0 for >= 50% of the 30 panel drugs.
- Failure policy: if P1 fails, the G1 claim downgrades to lineage-mediated prediction;
  the per-drug margin map still ships as the boundary payload (documented, counted
  only if P2 passes as a boundary result).
