---
id: P14-05
title: "Cumulus Readout: Oocyte Quality Prediction From Surrounding-Cell Transcriptomics"
parent: "CBIO043 - Digital Embryo: Multi-Omic Arrest Prediction (source abstract, 2026)"
---

# Cumulus Readout

**Parent project:** CBIO043 Digital Embryo (predicting developmental failure from molecular state).

## Premise
Embryo quality is decided before fertilization, at the oocyte - but oocytes cannot be biopsied non-destructively. Their surrounding cumulus cells, stripped and discarded at every IVF cycle, carry a transcriptional echo of oocyte competence. Published cumulus-cell datasets with downstream outcome labels exist. This project builds a cumulus-transcriptome predictor of blastocyst formation and implantation, and - in the parent's spirit of testing integration value - asks whether adding granulosa-cell or follicular-fluid layers beats cumulus alone, or whether the discarded cells already carry all recoverable signal.

## Data sources
- GEO: cumulus-cell transcriptome datasets with oocyte/embryo outcome labels (multiple public IVF studies).
- Follicular-fluid proteomics/metabolomics public datasets where deposited.
- Human oocyte/early-embryo scRNA references (GSE36552 and successors) for competence-program anchoring.
- Published candidate cumulus biomarkers (public) as fixed baselines.

## Method outline
1. Harmonize cumulus datasets with harmonized outcome tiers (fertilization, blastocyst, implantation).
2. Train per-tier predictors; leave-one-study-out validation.
3. Benchmark against published candidate biomarkers individually and as a panel.
4. Test incremental value of follicular-fluid features over cumulus-only.
5. Derive a minimal RT-qPCR-compatible gene panel for clinical translation.

## Success gates (locked before results)
- G1: cross-study AUC >= 0.70 for blastocyst formation, or certified ceiling.
- G2: minimal panel <= 20 genes retains >= 90% of full-model performance.
- G3: published biomarkers fail to beat the learned panel by any margin, or the hybrid panel (learned + published) is adopted with the delta reported.
- G4: implantation-tier results reported separately with honest sample-size caveats (known thin data).

## Expected deliverable
A "CumulusScore" panel (gene list + open classifier), the harmonized cumulus-outcome dataset, and the incremental-value verdict on additional omic layers.

## Failure/pivot rule
If cross-study transport collapses (G1), pivot to the confounder audit: stimulation protocol as the dominant batch axis - quantify and publish which protocol-stratified models do transport, gates re-locked.
