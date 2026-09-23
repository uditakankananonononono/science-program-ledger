---
id: P17-06
title: "ContextShift: Cross-Cell-Type Transport of 3D Off-Target Models"
parent: "CBIO054 - 3D-Aware CRISPR Off-Target Prediction (ISEF 2026 Grand Award)"
---

# ContextShift

**Parent project:** CBIO054 TAG-Cas (trained and validated in K562 - one leukemic cell line stands in for every patient's tissue).

## Premise
TAG-Cas's 3D features come from K562; therapeutics edit T cells, hematopoietic stem cells, hepatocytes. Hi-C and ATAC landscapes differ across cell types, so a K562-trained accessibility gate may be wrong exactly where it matters. Public off-target datasets exist for a handful of cell types, and ENCODE/4DN provide matched epigenomes for many more. This project measures the transport penalty: train in one cell type, test in others, with and without cell-type-matched 3D features. The answer decides whether the field needs per-tissue off-target assays or can compute its way from one cell type to another.

## Data sources
- Published multi-cell-type off-target datasets (public; GUIDE-seq-class across cell lines).
- ENCODE (public): ATAC/DNase for dozens of cell types.
- 4D Nucleome (public): Hi-C for matched cell types.
- crisprSQL (public): cell-type metadata spine.

## Method outline
1. Map all public off-target datasets to cell types with available matched epigenomes.
2. Full transport matrix: train-cell-type x test-cell-type, with sequence-only vs. sequence+3D models.
3. Quantify how much matched 3D features recover of the transport penalty.
4. Identify the minimal epigenomic data (ATAC only? Hi-C needed?) for reliable transport.
5. Extrapolation confidence tool: given a new cell type's epigenome, predict model reliability.

## Success gates (locked before results)
- G1: transport matrix covers >= 4 cell types with CIs.
- G2: transport penalty quantified (AUC drop), and matched-3D recovery fraction measured - the headline number, either direction.
- G3: minimal-data verdict delivered (ATAC-sufficient vs. Hi-C-required) with statistical support.
- G4: honest-negative clause: "off-target models do not transport even with matched epigenomes" is a full result redirecting the field to per-tissue assays.

## Expected deliverable
The transport matrix study, the minimal-epigenome verdict, and ContextShift (new cell type epigenome in; expected model reliability + recommended assay plan out).

## Failure/pivot rule
If matched Hi-C is missing for most off-target datasets (data gap blocks G1), pivot to the ATAC-proxy study: how well ATAC-only features substitute for Hi-C in the transport setting - gates re-locked.
