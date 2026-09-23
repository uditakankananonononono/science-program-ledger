---
id: P21-05
title: "Tumor-Stroma Loop: A Multicellular IL-6 Model With Fibroblasts and Macrophages"
parent: "CBIO060 - A Mathematical Model of IL-6 in Breast Cancer (source abstract, 2023)"
---

# Tumor-Stroma Loop

**Parent project:** CBIO060 IL-6 TNBC Model (48-ODE model of IL-6 signal transduction in triple-negative breast cancer; sensitivity analysis and virtual drug-target screening).

## Premise
The parent modeled IL-6 inside tumor cells. In real tumors, much IL-6 comes from cancer-associated fibroblasts and macrophages, and tumor cells signal back to them - a feedback loop between cell types. A single-cell-type model cannot capture that. Single-cell RNA-seq atlases of TNBC now give cell-type-specific expression of IL6, IL6R and IL6ST to constrain such a model.

## Hypothesis
A three-compartment model (tumor, fibroblast, macrophage) predicts that blocking fibroblast IL-6 lowers tumor pSTAT3 more than blocking tumor-cell IL-6, and scRNA-seq-derived ligand-receptor levels support fibroblasts as the dominant source.

## Data sources (free/public)
- Wu et al. 2021 Nat Genet breast cancer single-cell atlas (public, GEO GSE176078), including TNBC tumors.
- CellPhoneDB / LIANA ligand-receptor resources (free).
- Parent model as the tumor-cell compartment.

## Method outline
1. From the TNBC subset of the atlas, estimate per-cell-type expression of IL6, IL6R, IL6ST and key feedback genes; set relative production and receptor levels.
2. Build tumor, fibroblast and macrophage compartments linked by shared extracellular IL-6 (and soluble IL-6R for trans-signaling).
3. Simulate blocking IL-6 from each source, IL-6R antibody, and JAK inhibition.
4. Compare model source dominance with ligand-receptor inference scores.

## Success gates (locked before results)
- G1: model steady state matches atlas-derived relative IL-6 source ranking.
- G2: source-blocking predictions robust across +/- 50% parameter perturbation (reported as fraction of runs).
- G3: trans-signaling contribution quantified; if negligible, stated.

## Expected deliverable
A multicellular SBML model, scRNA-derived parameter table, and a source-blocking prediction set for future testing.

## Failure/pivot rule
If atlas data contradict fibroblast dominance (G1 differs), follow the data: re-center the model on the actual dominant source and report the corrected picture.
