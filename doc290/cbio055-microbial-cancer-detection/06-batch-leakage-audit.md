---
id: P18-06
title: "Batch Leakage Audit: Separating Cancer Signal From Sequencing-Center Signal"
parent: "CBIO055 - Early Cancer Detection Using Microbial Information (source abstract, 2023)"
---

# Batch Leakage Audit

**Parent project:** CBIO055 Microbial Cancer Detection (taxonomy + microbial function features from >2000 tumor and blood samples; 18% synergy gain in tissue, weaker in cfDNA).

## Premise
In TCGA, cancer type is heavily confounded with tissue source site, plate and sequencing center. A classifier that "detects cancer type" from microbial reads may partly be detecting which lab processed the sample. The parent's 82% tissue accuracy has never been split into biology vs batch. This project puts a number on it.

## Hypothesis
At least 30% of the parent-style model's balanced accuracy comes from center/plate structure, measurable as the drop when training and testing are restricted to different centers.

## Data sources (free/public)
- Poore 2020 processed tables with TCGA metadata (center, plate, platform) from the public supplement.
- GDC open-tier clinical and biospecimen metadata (sample source site, plate IDs).
- ComBat / ConQuR (microbiome batch correction) and MMUPHin R packages.

## Method outline
1. Predict sequencing center from microbial features alone; if accuracy is high, batch is a live threat.
2. Retrain cancer-type classifiers under three splits: random, center-held-out, plate-held-out.
3. Apply ConQuR and MMUPHin correction; re-evaluate.
4. Decompose accuracy: random minus center-held-out = batch-attributable share.

## Success gates (locked before results)
- G1: center-prediction accuracy reported against chance; above 2x chance means batch is a declared confounder.
- G2: center-held-out tissue accuracy >= 60% balanced for the combined model, or the drop is the headline.
- G3: batch-attributable share reported with 95% CI whatever its size.

## Expected deliverable
A batch-decomposition table per cancer type, split definitions others can reuse, and a corrected accuracy estimate for the parent-style model.

## Failure/pivot rule
If center-held-out splits are impossible for some cancers (single center), restrict to cancers with >= 2 centers and publish the coverage map of which TCGA microbiome claims can ever be batch-tested.
