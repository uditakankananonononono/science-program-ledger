---
id: P18-01
title: "Clean Signal Audit: How Much Tumor-Microbiome Signal Survives Rigorous Decontamination"
parent: "CBIO055 - Early Cancer Detection Using Microbial Information (source abstract, 2023)"
---

# Clean Signal Audit

**Parent project:** CBIO055 Microbial Cancer Detection (taxonomy + microbial function features from >2000 tumor and blood samples; 18% synergy gain in tissue, weaker in cfDNA).

## Premise
The parent built on TCGA-derived microbial profiles, the resource whose headline cancer-microbiome results were challenged by Gihawi et al. 2023 (mBio) for human-read misclassification and normalization artifacts. Before anyone extends the synergy claim, the field needs to know how much survives a clean pipeline. This project rebuilds taxonomic and functional features on decontaminated profiles and measures how much of the 82% accuracy / 0.92 AUROC result is left.

## Hypothesis
Functional features lose less accuracy than taxonomic features under strict decontamination, because contaminant taxa inflate taxonomic separability more than function-level separability.

## Data sources (free/public)
- Poore et al. 2020 processed TCGA microbial tables (public supplement), raw and decontaminated versions.
- Gihawi et al. 2023 mBio reanalysis tables and code (public).
- Narunsky-Haziza et al. 2022 Cell pan-cancer mycobiome tables (public supplement).
- Reagent-contaminant genus lists (Salter et al. 2014); decontam R package.
- Raw TCGA reads are dbGaP controlled-access and out of scope; processed open tables only.

## Method outline
1. Reproduce parent-style taxonomy-only, function-only and combined classifiers on the original tables as the baseline.
2. Apply three decontamination levels: none, contaminant-list removal, Gihawi-style strict filtering.
3. Rebuild functional profiles from surviving taxa only, so function cannot carry removed taxa.
4. Re-train with sequencing-center-stratified splits; record accuracy and AUROC drop per level.
5. Track which of the parent 190 taxonomic and 118 functional biomarkers survive each level.

## Success gates (locked before results)
- G1: reproduction baseline within 5 points balanced accuracy of the parent, or the gap is documented as a result.
- G2: under strict filtering, the combined model keeps AUROC >= 0.75 on center-stratified splits, or the collapse is the headline finding.
- G3: function-only AUROC drop is smaller than taxonomy-only drop by >= 0.03 (paired bootstrap p < 0.05).
- G4: all claims per cancer type with 95% CIs; pooled-only claims prohibited.

## Expected deliverable
A reproducible decontamination benchmark (code + tables), a "survivor list" of biomarkers robust to cleaning, and a writeup comparing parent-era and clean-era numbers.

## Failure/pivot rule
If nothing survives strict filtering (G2 fails), pivot to a positive-control study: plant simulated microbial signal into clean profiles at known effect sizes and measure the smallest effect this data type can detect.
