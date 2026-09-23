---
id: P18-10
title: "Cross-Kingdom Networks: Bacterial-Fungal Co-occurrence Structure as a Cancer Biomarker"
parent: "CBIO055 - Early Cancer Detection Using Microbial Information (source abstract, 2023)"
---

# Cross-Kingdom Networks

**Parent project:** CBIO055 Microbial Cancer Detection (taxonomy + microbial function features from >2000 tumor and blood samples; 18% synergy gain in tissue, weaker in cfDNA).

## Premise
The parent treated each taxon and function as an independent feature. But tumors are ecosystems: Narunsky-Haziza et al. 2022 found fungi co-occur with specific bacteria and immune states. Features that describe how microbes co-occur - network edges, not nodes - may carry signal that abundance tables miss.

## Hypothesis
Sample-level network features (edge presence scores from bacterial-fungal co-occurrence) add >= 0.03 AUROC over abundance features for cancer-type discrimination.

## Data sources (free/public)
- Narunsky-Haziza 2022 Cell processed fungal + bacterial tables (public supplement).
- Decontaminated tables from P18-01 where available.
- SpiecEasi and FlashWeave (free network inference tools).

## Method outline
1. Infer per-cancer co-occurrence networks on training folds only, to avoid leakage.
2. Turn networks into per-sample features (edge consistency scores, module abundances).
3. Train abundance-only, network-only and combined models; center-stratified splits.
4. Name the top bacterial-fungal edges that separate cancer types.

## Success gates (locked before results)
- G1: combined beats abundance-only by >= 0.03 AUROC (paired bootstrap p < 0.05).
- G2: >= 3 cross-kingdom edges replicate in an independent (non-TCGA) cohort from the same paper.
- G3: per-cancer 95% CIs; null result reported as the finding.

## Expected deliverable
Per-cancer bacterial-fungal networks, an edge-feature library, and a benchmark against abundance models.

## Failure/pivot rule
If network features add nothing (G1 fails), pivot to using the networks for biology only: test whether replicated edges link to immune-cell fractions estimated from open-tier TCGA expression.
