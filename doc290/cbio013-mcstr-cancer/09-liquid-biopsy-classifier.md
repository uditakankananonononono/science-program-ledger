---
id: P05-09
title: "HCC Liquid Biopsy Classifier: STR Features from Plasma with Locked External Validation"
parent: "CBIO013 - Micro-Changing Tandem Repeats in 10 Human Cancers (source abstract, 2023)"
---

# HCC Liquid Biopsy Classifier from Plasma STR Features

**Parent project:** CBIO013 - 8-locus HCC panel at 97.8% tumor-vs-normal accuracy and plasma detection of mcSTR1 - on small n, no external validation.

## Premise
97.8% on tens of samples is not a diagnostic. A classifier built on public HCC cfDNA cohorts with a locked external test is the honest version of the same idea.

## Hypothesis
A panel of the top HCC mcSTR loci + fragment-length features achieves AUC >= 0.80 on internal CV and stays >= 0.70 on a fully external cohort - or the panel is not yet diagnostic-grade.

## Data sources (free/public)
- Public HCC cfDNA WGS/WES cohorts (SRA: e.g., published HCC plasma studies, plus pan-cancer cfDNA sets with HCC arms).
- Tissue-derived HCC mcSTR panel from the parent + P05-01.

## Method outline
1. Feasibility-gate loci by P05-03 coverage analysis before inclusion.
2. Train a classifier (STR deviation + fragmentomics features) with patient-level CV; freeze; evaluate on the external cohort untouched until lock.
3. Report sensitivity at locked specificity (95%, 99%) - the clinically meaningful operating points.

## Success gates (locked before results)
- G1: external AUC reported as the headline; internal CV labeled exploratory.
- G2: sensitivity at 95% specificity >= 60% externally, else early-detection utility is rejected at this stage.
- G3: external cohort untouched until model freeze (repo tag + hash as proof).

## Expected deliverable
`hcc-str-liquid`: the trained classifier with its freeze certificate + external validation report + an API for scoring new cfDNA samples.

## Failure/pivot rule
If external performance fails, publish the internal/external gap - the exact overfitting magnitude of small-sample cfDNA panels - with the panel released for community iteration.
