---
id: P14-03
title: "Receptivity Window Engine: Multi-Omic Timing of Endometrial Implantation"
parent: "CBIO043 - Digital Embryo: Multi-Omic Arrest Prediction (source abstract, 2026)"
---

# Receptivity Window Engine

**Parent project:** CBIO043 Digital Embryo (multi-omic prediction of embryo outcomes).

## Premise
The Digital Embryo studies the embryo; half of implantation failure is the other side of the interface - the endometrium's window of receptivity opening at the wrong time. Public endometrial transcriptome datasets across the menstrual cycle exist, and endometrial microbiome data is accumulating. This project builds a multi-omic (transcriptome + microbiome) receptivity-window predictor and tests the clinical claim that displaced-window diagnosis improves transfer timing, with a twist the parent would recognize: treat the window as a molecular state, not a calendar date, and quantify how much microbiome data adds over transcriptome alone.

## Data sources
- Public endometrial transcriptome time-series datasets on GEO (including the GSE58144 receptivity-array cohort and successor RNA-seq cohorts).
- Published endometrial/vaginal microbiome-IVF datasets (16S and shotgun, public via SRA).
- Human Endometrial Transcriptome project data (public).
- Published commercial receptivity-assay gene panels (public compositions) as baselines.

## Method outline
1. Harmonize cycle-staged endometrial transcriptomes; build a molecular window-phase classifier.
2. Quantify inter-dataset window-gene stability; define a robust minimal gene set.
3. Add microbiome features; measure incremental value over transcriptome alone.
4. Validate against published clinical outcome data (pregnancy rates by predicted vs. histological timing).
5. Benchmark against commercial panel genes as a fixed baseline.

## Success gates (locked before results)
- G1: window-phase classification cross-dataset balanced accuracy >= 0.80.
- G2: microbiome features add >= 0.03 AUC over transcriptome-only, or the certified result is that microbiome adds nothing (steering spending away from microbiome testing).
- G3: minimal gene set of <= 50 genes retains >= 95% of full-model accuracy.
- G4: outcome validation shows predicted-window discordance associates with outcome in the expected direction on >= 1 independent cohort, or is reported as unvalidated with a defined protocol.

## Expected deliverable
An open "WindowMap" predictor (input: endometrial biopsy transcriptome; output: molecular window phase with confidence), the robust window gene set, the microbiome incremental-value verdict, and comparison to commercial panels.

## Failure/pivot rule
If window genes prove unstable across datasets (G1 fails), pivot to the instability study: which processing choices create false window signatures - a methods-warning paper plus a preprocessing standard, gates re-locked.
