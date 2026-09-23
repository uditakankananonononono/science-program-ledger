---
id: P13-03
title: "Spatial TME Trafficking Atlas: Predicting CAR-T Infiltration Failure From Spatial Transcriptomics"
parent: "CBIO042 - ReinforCell: CAR-T Cell Optimization Solution (ISEF 2026 Grand Award)"
---

# Spatial TME Trafficking Atlas

**Parent project:** CBIO042 ReinforCell (extending CAR-T efficacy to solid tumors; the tumor microenvironment as the obstacle).

## Premise
ReinforCell treats the tumor microenvironment as an uncertain external disturbance; this project makes the TME the object of study. The dominant reason CAR-T fails in solid tumors is physical: engineered cells never reach the tumor core. Public spatial transcriptomics atlases now contain thousands of tumor sections with immune coordinates. This project builds a computational model that predicts, from a tumor's spatial architecture alone (stroma barriers, vessel density, chemokine gradients, exclusion-zone geometry), whether infused T cells will infiltrate - then inverts the model to rank which microenvironment feature, if perturbed, would most improve trafficking for each tumor type.

## Data sources
- 10x Genomics public Visium datasets (breast, colorectal, lung tumor sections).
- Human Tumor Atlas Network (HTAN) public spatial data via the NCI Cancer Data Service.
- Broad Single Cell Portal: matched scRNA-seq references for cell-type deconvolution of spots.
- Human Protein Atlas pathology images for orthogonal validation of exclusion phenotypes.

## Method outline
1. Curate Visium sections labeled by immune phenotype (inflamed, excluded, desert) using deconvolution against scRNA references.
2. Extract spatial-architecture features: stroma-tumor interface length, perivascular T-cell density gradients, chemokine-expression fields (CXCL9/10/11), exclusion-zone thickness.
3. Train a graph neural network over tissue region graphs to classify exclusion phenotype; validate cross-cohort.
4. Build a counterfactual engine: perturb single features in silico (e.g., stroma density -30%) and re-predict infiltration, ranking actionable features per tumor type.
5. Compare counterfactual rankings against published combination-therapy outcomes (stromal-targeting + CAR-T studies) as external validation.

## Success gates (locked before results)
- G1: cross-cohort exclusion classification AUC >= 0.80 on >= 2 unseen datasets.
- G2: spatial features beat composition-only features (cell fractions without geometry) by >= 0.05 AUC - geometry must earn its place.
- G3: >= 60% of top-ranked counterfactual features match published intervention results where literature exists.
- G4: if G2 fails, the negative stands and the deliverable becomes a "composition is enough" boundary paper plus a cheaper tool.

## Expected deliverable
A "TME-Gate" tool (input: Visium section or H&E-derived region graph; output: infiltration-failure risk + ranked microenvironment targets), the cross-tumor spatial atlas of exclusion geometry, and figures showing per-tumor-type counterfactual rankings.

## Failure/pivot rule
If spatial geometry adds nothing over composition (G2), pivot to building the best possible composition-only exclusion predictor and quantify exactly when spatial data is worth its cost - amended gates locked before reading new results.
