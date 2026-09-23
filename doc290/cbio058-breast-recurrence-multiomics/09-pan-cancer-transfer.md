---
id: P20-09
title: "Beyond Breast: Testing the Recurrence Pipeline Across Other Cancer Types"
parent: "CBIO058 - Deep-Learning to Predict Breast Cancer Recurrence (source abstract, 2023)"
---

# Beyond Breast

**Parent project:** CBIO058 Breast Recurrence (AIME autoencoder integrating expression + CNV with ER-status confounder adjustment, random forest recurrence classifier, 25-gene list).

## Premise
The parent ends by saying the approach "can be expanded to include other cancer types." That claim is testable now. TCGA has open-tier multi-omics and curated progression-free intervals for many cancers, and Liu et al. 2018 rated which endpoints are reliable per cancer. This project runs the same confounder-adjusted integration pipeline across cancers and reports where it works.

## Hypothesis
The pipeline reaches C-index >= 0.65 for PFI in at least 5 of 10 TCGA cancers with reliable PFI endpoints, and performance tracks event count more than cancer biology.

## Data sources (free/public)
- TCGA open-tier expression, CNV, miRNA, mutation for 10 cancers with recommended PFI (e.g., LUAD, COAD, KIRC, LIHC, HNSC, BLCA, STAD, OV, UCEC, PRAD).
- Liu 2018 TCGA Pan-Cancer Clinical Data Resource.

## Method outline
1. Apply the same pipeline per cancer, with a cancer-appropriate confounder (e.g., stage or a key clinical marker) in place of ER.
2. Evaluate with repeated CV; compare against clinical-only models per cancer.
3. Regress C-index on event count, sample size and number of omic layers across cancers.
4. Test cross-cancer transfer: train on pooled cancers, test on a held-out cancer.

## Success gates (locked before results)
- G1: C-index >= 0.65 in >= 5 of 10 cancers.
- G2: omics beat clinical-only by >= 0.03 in >= 3 cancers; otherwise "omics add little" is the result.
- G3: event-count relationship reported with CI.

## Expected deliverable
A pan-cancer table of where multi-omic recurrence prediction works, with open code.

## Failure/pivot rule
If results are driven by event count only, publish a sample-size planning guide: events needed for a given C-index gain.
