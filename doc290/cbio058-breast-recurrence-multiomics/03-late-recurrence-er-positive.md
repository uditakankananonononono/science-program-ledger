---
id: P20-03
title: "Late Relapse: Predicting Recurrence More Than Five Years After ER+ Diagnosis"
parent: "CBIO058 - Deep-Learning to Predict Breast Cancer Recurrence (source abstract, 2023)"
---

# Late Relapse

**Parent project:** CBIO058 Breast Recurrence (AIME autoencoder integrating expression + CNV with ER-status confounder adjustment, random forest recurrence classifier, 25-gene list).

## Premise
The parent treated ER status as a confounder to remove. But ER+ and ER- cancers recur on different clocks: ER- mostly within 5 years, ER+ steadily for 20 years. Late ER+ relapse decides who should take extended endocrine therapy, and it is poorly predicted. Rueda et al. 2019 (Nature) showed METABRIC integrative clusters carry late-relapse risk. This project targets late relapse directly.

## Hypothesis
Multi-omic embeddings (expression + CNA) predict distant relapse after 5 years in ER+ patients who were relapse-free at 5 years, with C-index >= 0.62, beating clinical variables alone (CTS5-style) by >= 0.03.

## Data sources (free/public)
- METABRIC expression, CNA and long-term clinical follow-up (cBioPortal).
- Rueda 2019 integrative cluster assignments (public supplement).
- GEO ER+ tamoxifen cohorts with long follow-up (e.g., GSE6532).

## Method outline
1. Select ER+ METABRIC patients relapse-free and alive at 5 years; outcome = distant relapse from year 5 onward (competing risk: death without relapse).
2. Build embeddings with ER kept as a stratum rather than regressed out.
3. Fit Fine-Gray competing-risk and Cox models; compare clinical-only, omics-only and combined.
4. Test whether integrative cluster membership explains the omic signal.

## Success gates (locked before results)
- G1: combined model C-index >= 0.62 for late distant relapse (cross-validated, 95% CI).
- G2: beats clinical-only by >= 0.03 C-index.
- G3: validated in at least one GEO cohort, or external validation gap is stated plainly.

## Expected deliverable
A late-relapse risk model for ER+ patients and a comparison of learned embeddings vs integrative clusters.

## Failure/pivot rule
If omics add nothing beyond clinical (G2 fails), pivot to identifying the subgroup (by integrative cluster) where omics do add value, if any.
