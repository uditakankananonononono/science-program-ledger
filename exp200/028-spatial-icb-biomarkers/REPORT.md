# DOC-1-028: Identifying Spatial Biomarkers for Immunotherapy Response
**Claim** (locked pre-outcomes): a spatially-aware cholesterol-CD8 exclusion index separates aPD1
responders from non-responders (MC38 Visium, GSE284989) while pseudo-bulk cholesterol does not -
quantitative replication of the paper's spatial-sensitivity claim. **Verdict: DOCUMENTED BOUNDARY**
(G2 fail, pre-registered P1 fail, tree exhausted).

## Scores (tumor level = median over sections)
G1 sanity PASS: pseudo-bulk T-cell score ranks both responders top-2 of 8 (m16 #1, m15 #2) -
labels coherent. F2 (bulk cholesterol): both R in bottom 3 (m15 #6, m16 #8) - trends the published
direction but does not perfectly separate, consistent with the paper's weak bulk signal.
| feature | R ranks (of 8) | gate |
|---|---|---|
| F1 exclusion index | m16 #3, m15 #5 | G2 perfect sep (top 2): FAIL |
| P1 bivariate Moran's I | m16 #3, m15 #5 | FAIL (identical ordering) |

Both strongest-exclusion tails are NR (m10, m11, m14), and both R sit mid-pack: directionally
consistent with the paper but far from the locked exact-separation margin (p=1/28 required top-2).
G3 moot. Boundary per the locked tree.

## Mechanism (G4) - the payload
Section-level heterogeneity breaks tumor-level spatial biomarkers: within responder m16, per-section
CD8 mean spans 0.056-0.233 (4x) and CD8 spatial autocorrelation spans 0.13-0.22; m15's sections have
CD8 ~0.036 (below every NR tumor mean except m10) yet the mouse is a labeled responder. The paper's
response label is mouse-level histologic infiltration; any single-section or section-median spatial
statistic inherits that noise. The paper's own claim was spot-level (48,636 spots pooled), not
tumor-ranking level. Lesson locked for the program: clinical-label granularity vs section sampling
is an eligibility check for spatial-biomarker gates - require per-section labels or a pooled-spot
statistic matched to the label's granularity.

## Tool (G5)
code/spatial_biomarker.py - exclusion index + bivariate Moran for one Visium sample; smoke-tested
(reproduces pipeline values for m15s1 and m10 exactly). Honest scope in docstring.
## Prospective lab nomination (locked)
Immuno-oncology spatial core with neoadjuvant anti-PD1 Visium cohorts: apply the locked index with
per-section labels, marker-concordance readout.
