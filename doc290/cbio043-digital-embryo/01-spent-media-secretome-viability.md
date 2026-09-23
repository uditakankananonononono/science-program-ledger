---
id: P14-01
title: "Secretome-Only Viability: Non-Invasive Embryo Arrest Prediction From Spent Culture Media"
parent: "CBIO043 - Digital Embryo: Multi-Omic Arrest Prediction (ISEF 2026 Grand Award)"
---

# Secretome-Only Viability

**Parent project:** CBIO043 Digital Embryo (six-omic integration predicting embryo arrest with a perturbation engine).

## Premise
The Digital Embryo's six-omic stack is scientifically powerful but clinically unusable: no IVF lab will biopsy an embryo for six omic layers. The one measurement clinics could adopt tomorrow is non-invasive analysis of spent culture media - the embryo's secretome and metabolome accumulate in the droplet it grew in. This project isolates that single omic layer: how much of the arrest signal is recoverable from secretome/metabolome data alone, using public spent-media datasets and the parent's own multi-omic concordance logic as the ceiling reference. The twist: instead of asking "can we add more omics," it asks "how much can we remove and still predict."

## Data sources
- Published spent-culture-media metabolomics and secretomics datasets on GEO/MetaboLights (public IVF media studies).
- Human embryo scRNA-seq references (Yan et al. 2013 GSE36552; Petropoulos et al. 2016 E-MTAB-3929) to define the transcriptomic ceiling.
- MetaboLights/Metabolomics Workbench public embryo-mendelian media studies.
- Published non-invasive PGT-A / spent-media cfDNA datasets for cross-signal comparison.

## Method outline
1. Harmonize public spent-media metabolomic/secretomic datasets with arrest/blastocyst/implantation labels.
2. Train compact classifiers (XGBoost + logistic) per dataset; leave-one-dataset-out validation.
3. Compute the information ceiling: compare single-layer AUC against the parent's reported multi-omic gain (+0.116 AUC) using matched-outcome logic.
4. Identify the minimal analyte panel (top-k metabolites/proteins) that retains >= 90% of full-panel performance.
5. Stress-test batch effects: media brand, incubator, and lab as confounders; report a confounder-robustness analysis.

## Success gates (locked before results)
- G1: cross-dataset AUC >= 0.70 from secretome/metabolome alone, or certified ceiling documented.
- G2: minimal panel of <= 12 analytes retains >= 90% of full-panel AUC.
- G3: performance survives media-brand stratification (degradation <= 0.08 AUC), or the confounder boundary is the published result.
- G4: all claims per-dataset with CIs; pooled-only claims prohibited.

## Expected deliverable
An open "MediaScore" panel predictor (input: targeted metabolite panel values; output: arrest-risk band with confidence), the harmonized spent-media dataset, and the information-ceiling analysis vs. multi-omic prediction.

## Failure/pivot rule
If media-brand confounding dominates (G3 fails), pivot to a standardization study: which normalization/analyte-reference scheme makes spent-media prediction portable across labs - gates re-locked around a cross-lab normalization benchmark.
