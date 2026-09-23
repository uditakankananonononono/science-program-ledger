# GATES v2 - pivot for G2 (locked 2026-09-23 ~23:15 IST, before any 2-hop computation)
G2 (1-hop LR co-neighborhood vs plain randoms) FAILED as-run; corrected matched-null
result pending under addendum-1. Pivot direction pre-named in GATES.md: 2-HOP
neighborhoods (Visium spots are ~100um apart - 1-10 cells per spot; paracrine signaling
range argues for 2-hop).
- V2 gate: median LR co-neighborhood correlation (ligand spot level vs 2-hop
  neighbor-mean receptor, expression-decile-matched null, 500 pairs) exceeds the null
  95th percentile.
- If v2 also fails: LR co-localization is a documented boundary for this section
  (spot-resolution Visium cannot resolve these 48 LR pairs above technical
  autocorrelation) - ships documented, counted only if G1's inverted claim is deemed a
  methodological result by the lead lane.
- G1 outcome (final, honest inversion per its locked clause): mean expression + dropout
  PREDICT per-gene Moran's I at r=0.716 on 500 held-out genes (null q95 0.085) -
  spatial autocorrelation in this Visium section is substantially a technical-covariate
  artifact. Any biological spatial claim must control for it.
