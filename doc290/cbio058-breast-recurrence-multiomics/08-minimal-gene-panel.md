---
id: P20-08
title: "Clinic-Ready Panel: Shrinking Multi-Omic Recurrence Prediction to a Small Gene Panel"
parent: "CBIO058 - Deep-Learning to Predict Breast Cancer Recurrence (source abstract, 2023)"
---

# Clinic-Ready Panel

**Parent project:** CBIO058 Breast Recurrence (AIME autoencoder integrating expression + CNV with ER-status confounder adjustment, random forest recurrence classifier, 25-gene list).

## Premise
Multi-omic profiling costs too much for routine care. Commercial recurrence tests (Oncotype DX 21-gene, MammaPrint 70-gene) work with small RNA panels. The parent's pipeline gives 25 genes, but chosen for importance, not for portability or panel size. This project asks: how few genes keep most of the multi-omic model's performance?

## Hypothesis
A panel of <= 15 genes, measurable on any expression platform, keeps >= 90% of the full multi-omic model's C-index in external cohorts.

## Data sources (free/public)
- TCGA-BRCA (training), SCAN-B GSE96058 and METABRIC (external).
- Published gene lists of Oncotype DX and MammaPrint (public in original papers) for comparison scores.

## Method outline
1. Train the full multi-omic survival model in TCGA as the teacher.
2. Select panels of 5-50 genes by stability selection and by distilling the teacher's risk score.
3. Freeze weights; score SCAN-B and METABRIC with no refitting.
4. Compare with Oncotype-like and MammaPrint-like scores computed from public gene lists, and with random panels.

## Success gates (locked before results)
- G1: <= 15-gene panel keeps >= 90% of teacher C-index in SCAN-B and METABRIC.
- G2: panel is not worse than the Oncotype-like score by more than 0.02 C-index; beating it is reported only with CI excluding 0.
- G3: beats >= 95% of random 15-gene panels.

## Expected deliverable
A panel-size curve, a frozen scoring formula, and a head-to-head with public commercial-test gene lists.

## Failure/pivot rule
If small panels lose too much (G1 fails), report the smallest size that reaches 90% and which omic layer's information is lost when going to RNA only.
