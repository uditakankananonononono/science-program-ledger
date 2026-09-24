# P21-06 Build Report: Patient-Specific Simulated pSTAT3 vs TNBC Outcome

**Parent:** CBIO060 IL-6 TNBC Model | **Spec:** doc290/cbio060-il6-tnbc-model/06-patient-specific-pathway-activity.md
**Built:** 2026-09-24 (lane D) | **Status:** BOUNDARY RESULT. G1 FAIL: the association is significant but in
the opposite direction to the pre-declared one. G2 FAIL: mechanistic modelling adds nothing over the simple
score. G3 reported. Protocol locked in `PROTOCOL_LOCK.md` (fd194dd5) before any data was fetched.

## What was built
`tool/patient_sim.py` pulls expression and outcomes from the public cBioPortal API. Cohorts: METABRIC TNBC
(ER/PR/HER2-negative, n = 320, 131 RFS events) and TCGA PanCan BRCA_Basal (n = 171, 25 PFS events). For each
patient it scales 5 P21-01 model parameters and the tissue STAT3 pool by that patient's z-scored IL6, IL6R,
JAK1, PTPN2, ADAM17 and STAT3 expression (multiplier 2^(s*z)). It then simulates steady-state tissue pSTAT3
and compares it with survival: Cox HR on a median split, and Harrell C-index against the simple pathway score
and raw IL6/STAT3.
Run from repo root: `python3 doc290/cbio060-il6-tnbc-model/p21-06-patient-pathway-activity/tool/patient_sim.py <out.json>` (~10 s + API).

## Results (primary s = 0.5)
| cohort | HR high vs low simulated pSTAT3 | p | C-index sim | simple score | raw IL6 | raw STAT3 |
|--------|------|------|------|------|------|------|
| METABRIC TNBC (RFS) | 0.59 | 0.004 | 0.435 | 0.433 | 0.485 | 0.438 |
| TCGA basal (PFS) | 0.70 | 0.38 | 0.493 | 0.476 | 0.473 | 0.472 |
(C-index < 0.5 means higher score = better outcome.)

| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | HR >= 1.5, p < 0.05 in >= 1 cohort, HR > 1 in the other (high = worse, pre-declared) | high simulated pSTAT3 = BETTER outcome: HR 0.59 (p = 0.004) METABRIC, 0.70 (ns) TCGA | **FAIL (documented discrepancy: opposite direction)** |
| G2 | C-index >= simple score + 0.02 in both cohorts | +0.002 METABRIC, +0.017 TCGA | **FAIL** - mechanistic modelling adds nothing here |
| G3 | sensitivity to scaling reported | s = 0.25 / 0.5 / 1.0: METABRIC HR 0.59 / 0.59 / 0.57; TCGA HR 0.71 / 0.70 / 0.74; C-index moves by <= 0.013 | **REPORTED** |

## What this means
1. **In TNBC, higher model-predicted pathway activity goes with better outcome, not worse.** The signal is
   significant in the larger cohort and has the same direction in the smaller one. It is almost entirely
   carried by total STAT3 expression: raw STAT3 alone reaches the same C-index (0.438), and the simulation
   mainly passes the STAT3 pool through. Because the direction was pre-declared the other way, this is recorded
   as a discrepancy, not a finding to claim. It needs a pre-registered follow-up (for example with protein-level
   pY705-STAT3) before it can be interpreted.
2. **The mechanistic layer adds nothing over a simple mean-z pathway score.** The deltas are 0.002 and 0.017,
   below the 0.02 bar in both cohorts. The model's saturation (P21-01) squeezes most expression variation into a
   narrow pSTAT3 range.
3. TCGA basal has only 25 PFS events, so it is underpowered for HR estimation.

## Honesty notes
- The TCGA "TNBC" set is the PAM50 basal proxy (IHC status not in the PanCan clinical table). METABRIC uses
  IHC/SNP-based receptor status.
- METABRIC expression is microarray intensity and TCGA is log2(RSEM+1). Both are z-scored within cohort.
- IL6ST is excluded (no synthesis parameter in the host model). Same surrogate-model caveat as P21-01.
- Data are fetched live from cBioPortal (brca_metabric, brca_tcga_pan_can_atlas_2018). Patient-level data are not
  committed; results.json holds the aggregate statistics.
