---
id: P14-10
title: "Exposure-Embryo Map: Environmental Exposures and Arrest Risk via Cohort + Perturbation Fusion"
parent: "CBIO043 - Digital Embryo: Multi-Omic Arrest Prediction (source abstract, 2026)"
---

# Exposure-Embryo Map

**Parent project:** CBIO043 Digital Embryo (perturbation engine validated against known in vitro compound effects).

## Premise
The Digital Embryo validated its perturbation engine against 85 compounds; this project aims perturbation logic at the exposure question couples actually ask: do air pollution, endocrine disruptors, and heavy metals measurably raise embryo-arrest risk? Published IVF-exposure cohorts (residential pollution, urinary EDC biomarkers) report outcome associations; NHANES provides population exposure distributions. This project fuses cohort epidemiology with mechanistic perturbation evidence: exposures whose molecular perturbation signatures match arrest programs get elevated from statistical association to mechanistically-supported risk - a triage of which environmental risks deserve intervention studies first.

## Data sources
- Published IVF-exposure cohort studies (air pollution, BPA/phthalates, metals; open-access result tables).
- NHANES biomonitoring data (public): population exposure distributions.
- Comparative Toxicogenomics Database (CTD, public): exposure-gene interactions.
- The parent's perturbation-validation compound set as the methodological anchor.

## Method outline
1. Systematically extract exposure-outcome associations from IVF cohort literature (PRISMA-style, but computational).
2. For each exposure, pull CTD gene-interaction signatures and test overlap with arrest programs from the parent's framework.
3. Classify exposures: association-only vs. mechanistically-supported vs. unsupported.
4. Dose-context: compare cohort effect sizes against NHANES population exposure levels (is the effect at real-world doses?).
5. Rank exposures by combined evidence for intervention-study prioritization.

## Success gates (locked before results)
- G1: >= 15 exposures systematically extracted with harmonized effect sizes.
- G2: >= 3 exposures achieve mechanistic support (signature overlap FDR < 0.05), or the certified finding is that cohort associations lack mechanistic corroboration - redirecting the field's alarm.
- G3: real-world dose analysis completed for all supported exposures; effects requiring supra-environmental doses are explicitly flagged.
- G4: publication-bias assessment (funnel analysis) reported for each exposure class.

## Expected deliverable
The exposure-embryo evidence map (interactive), a prioritized intervention-study ranking, an "ExposureTriage" tool (input: exposure; output: evidence class with mechanistic support score), and the dose-context report.

## Failure/pivot rule
If cohort extraction is defeated by incompatible outcome definitions, pivot to the harmonization-meta-science deliverable: show which exposure questions the current literature can and cannot answer, plus the reporting standard that would fix it - gates re-locked.
