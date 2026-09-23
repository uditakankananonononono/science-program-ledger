---
id: P13-09
title: "Pre-Infusion Triage: Predicting CAR-T Response From Routine Blood Panels"
parent: "CBIO042 - ReinforCell: CAR-T Cell Optimization Solution (source abstract, 2026)"
---

# Pre-Infusion Triage

**Parent project:** CBIO042 ReinforCell (patient-specific outcome prediction; making CAR-T more accessible).

## Premise
ReinforCell's prediction engine uses single-cell data that most treatment centers will never have. Real-world CAR-T decisions are made from routine labs: CBC with differential, LDH, CRP, ferritin, albumin. Published real-world cohorts report these alongside outcomes. This project asks the pragmatic question: how much of CAR-T response is predictable from the cheapest possible pre-infusion data, and where exactly does the cheap model run out of information? The deliverable is a triage tool any community hospital could run, plus an honest information ceiling that tells centers when expensive profiling actually adds predictive power.

## Data sources
- Published real-world CAR-T outcome cohorts with pre-infusion lab values (open-access supplements from US and EU multicenter studies).
- MIMIC-IV (public): general hematology-oncology lab-outcome structure for feature pretraining.
- Published inflammatory-index literature (CAR-HEMATOTOX and similar scores - public definitions) as baselines.

## Method outline
1. Harmonize published cohort lab/outcome tables into a common schema with explicit missingness handling.
2. Implement published baseline scores (CAR-HEMATOTOX etc.) exactly as defined; benchmark them cross-cohort first.
3. Train gradient-boosted and logistic models on pooled cohorts with leave-one-cohort-out validation.
4. Measure the information ceiling: prediction vs. feature-cost curve (labs only -> +cytokines -> +flow cytometry) using published paired data.
5. Calibrate decision thresholds for triage use (flag-for-profiling vs. proceed) with net-benefit analysis.

## Success gates (locked before results)
- G1: labs-only model achieves cross-cohort AUC >= 0.70, or the certified finding is that routine labs cannot triage (with the measured ceiling).
- G2: the model beats published baseline scores by >= 0.03 AUC or matches them with better calibration - matching is a valid result given simplicity.
- G3: feature-cost curve shows a measurable information gain from expensive profiling (>= 0.05 AUC), justifying the triage design - or shows it does not, which redirects spending.
- G4: all reported with per-cohort CIs; no pooled-only claims.

## Expected deliverable
An open "CART-Triage" calculator (input: routine pre-infusion labs; output: response-risk band with confidence and a recommend-profiling flag), the harmonized cohort dataset, and the feature-cost information-ceiling analysis.

## Failure/pivot rule
If cohort harmonization collapses on incompatible lab reporting, pivot to the reporting-standard proposal: a minimal common dataset for real-world CAR-T registries, validated by showing which published cohorts could have answered the triage question had they used it.
