---
id: P20-06
title: "Protein Layer: Do Proteomics Add Recurrence Signal Beyond RNA and Copy Number"
parent: "CBIO058 - Deep-Learning to Predict Breast Cancer Recurrence (source abstract, 2023)"
---

# Protein Layer

**Parent project:** CBIO058 Breast Recurrence (AIME autoencoder integrating expression + CNV with ER-status confounder adjustment, random forest recurrence classifier, 25-gene list).

## Premise
The parent used gene expression, CNV, mutation and miRNA - all DNA/RNA layers. Proteins are what actually act, and RNA-protein correlation in tumors is often modest. CPTAC breast proteogenomics (Krug et al. 2020 Cell) and TCGA reverse-phase protein arrays (RPPA) are public. This project adds the protein layer.

## Hypothesis
Adding RPPA protein and phosphoprotein levels to expression + CNV improves recurrence C-index by >= 0.03 in TCGA-BRCA, and proteins not well predicted by their mRNA carry most of the gain.

## Data sources (free/public)
- TCGA-BRCA RPPA data (TCPA portal / GDC open tier).
- CPTAC breast proteogenomics (Proteomic Data Commons, public) for a smaller deep-proteome check.
- TCGA-BRCA expression and CNV; Liu 2018 endpoints.

## Method outline
1. Match TCGA-BRCA patients with RPPA, expression and CNV (about 800).
2. Compute per-protein mRNA-protein correlation; label proteins as "RNA-tracked" or "RNA-discordant."
3. Train survival models with and without proteins; separately with only RNA-discordant proteins.
4. In CPTAC, test whether deep proteomics clusters carry recurrence information (limited events; descriptive).

## Success gates (locked before results)
- G1: adding RPPA improves C-index by >= 0.03 (repeated CV, 95% CI excludes 0).
- G2: RNA-discordant proteins account for >= 50% of the gain.
- G3: CPTAC analysis labeled exploratory with event counts stated.

## Expected deliverable
A protein-layer contribution report and a short list of RNA-discordant proteins linked to recurrence.

## Failure/pivot rule
If proteins add nothing (G1 fails), report which pathway-level proteins are redundant with RNA - useful for deciding whether proteomic assays are worth running.
