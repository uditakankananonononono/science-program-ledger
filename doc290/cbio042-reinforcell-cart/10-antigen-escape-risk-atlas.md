---
id: P13-10
title: "Antigen-Escape Atlas: Predicting Target-Antigen Loss Before Choosing the CAR"
parent: "CBIO042 - ReinforCell: CAR-T Cell Optimization Solution (source abstract, 2026)"
---

# Antigen-Escape Atlas

**Parent project:** CBIO042 ReinforCell (extending CAR-T to solid tumors and predicting patient-specific outcomes).

## Premise
CAR-T's most fundamental failure is the target disappearing: antigen escape causes a large share of relapses after CD19 therapy, and in solid tumors target heterogeneity means the antigen was never uniformly there. Single-cell tumor atlases now let us measure, per tumor type, the co-expression structure of candidate target antigens - which pairs are co-expressed on the same cells, which are mutually exclusive, which are lost under therapy. This project builds a pan-cancer antigen-escape risk atlas from public single-cell tumor data and turns it into a target-selection tool: for a given tumor profile, recommend single vs. dual-target CAR design with a quantified escape-risk estimate.

## Data sources
- CELLxGENE Census and Single Cell Portal: pan-cancer scRNA-seq tumor atlases (>= 10 tumor types).
- Published relapse/escape case series with pre/post antigen measurements (open-access).
- Human Protein Atlas: protein-level confirmation of RNA-measured antigen expression.
- DepMap (Broad, public): essentiality context for candidate antigens.

## Method outline
1. Curate candidate CAR target antigens from the clinical-trial literature (CD19, BCMA, GD2, HER2, mesothelin, GPC3, etc.).
2. Quantify per-tumor-type single-cell expression: fraction positive, expression variance, co-expression correlation matrix across antigen pairs.
3. Build an escape-risk score combining heterogeneity, stem-like compartment expression, and (where data exists) pre/post-therapy loss rates.
4. Validate against published escape case series: does the score rank high-escape tumor-antigen pairs correctly?
5. Derive dual-target pairing recommendations by minimizing joint escape risk under expression-coverage constraints.

## Success gates (locked before results)
- G1: atlas covers >= 10 tumor types and >= 15 candidate antigens with complete co-expression matrices.
- G2: escape-risk score directionally ranks published escape case series correctly in >= 75% of comparisons (with n reported honestly).
- G3: dual-target recommendations provably reduce predicted escape risk vs. best single target in >= 3 tumor types in silico.
- G4: if validation data is too thin for G2, ship the atlas plus a clearly-labeled unvalidated score and a defined validation protocol - the atlas stands alone as the deliverable.

## Expected deliverable
The pan-cancer antigen co-expression atlas (data + interactive explorer), an "EscapeRisk" target-selection tool (input: tumor type or scRNA profile; output: ranked single/dual targets with escape-risk estimates), and the validation report.

## Failure/pivot rule
If RNA-level expression proves unreliable vs. protein (checked against Human Protein Atlas), pivot the atlas to a quantified RNA-protein discordance study for CAR targets - itself an unpublished, useful boundary - with gates re-locked around protein-validated subsets.
