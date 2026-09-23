---
id: P05-08
title: "Survival Associations, Honestly: Censoring-Aware, Multiplicity-Controlled mcSTR Prognosis Models"
parent: "CBIO013 - Micro-Changing Tandem Repeats in 10 Human Cancers (source abstract, 2023)"
---

# Survival Associations, Honestly

**Parent project:** CBIO013 - mcSTRs associated with survival (p < 0.05) across cancers; binary/time-naive tests inflate such claims.

## Premise
Prognostic STR claims need censoring-aware models, multiplicity control across 182 loci x 10 cancers, and out-of-cohort validation - the standard failure points of biomarker-prognosis literature.

## Hypothesis
After proper Cox modeling and FDR control, <= 20% of the reported survival associations survive; the survivors validate in an independent cohort.

## Data sources (free/public)
- TCGA clinical + genotypes (P05-01); PCAWG as external cohort.
- Pan-cancer survival endpoints (public Liu 2018 curated endpoints).

## Method outline
1. Lock endpoints per cancer (PFI preferred); Cox models per locus with age/stage/purity covariates.
2. Multiplicity: BH-FDR within cancer; hierarchical FDR across the full locus x cancer grid.
3. Survivors tested in PCAWG with locked direction and endpoint mapping.

## Success gates (locked before results)
- G1: the full tested grid published (all 1,820 tests), not just significant cells.
- G2: a prognostic claim requires FDR < 0.1 internally AND same-direction external validation; otherwise exploratory-only labeling.
- G3: censoring distribution and follow-up adequacy reported per cancer.

## Expected deliverable
`strsurv`: the complete survival-testing grid + a validated-locus shortlist + a template for honest biomarker-prognosis pipelines.

## Failure/pivot rule
If nothing survives FDR + validation, publish the corrected null - the survival-association claim does not hold at proper statistical standards.
