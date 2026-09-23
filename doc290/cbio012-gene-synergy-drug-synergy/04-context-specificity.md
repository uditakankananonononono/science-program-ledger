---
id: P04-04
title: "One Cancer, One Answer? Cross-Cell-Line Transport of Synergy Predictions Across Tissues"
parent: "CBIO012 - The Usage of Gene Synergy to Predict Drug Synergy (source abstract, 2025)"
---

# Cross-Cell-Line Transport of Synergy Predictions

**Parent project:** CBIO012 - gene-function embeddings are universal by construction; real synergy is context-dependent.

## Premise
The parent's universality is a testable scientific claim: if function embeddings capture mechanism, predictions should transfer across cell lines within a tissue and degrade measurably across tissues.

## Hypothesis
Measured synergy itself replicates across lines of the same tissue at r >= 0.4 but drops across tissues; the parent's predictions mirror this hierarchy - and where they do not, context-free embeddings are the cause.

## Data sources (free/public)
- DrugComb multi-line screens; NCI-ALMANAC (60 lines, fixed grid).
- DepMap lineage annotations.

## Method outline
1. Quantify empirical synergy reproducibility: same combination across lines/tissues (correlation matrices, lineage-stratified).
2. Evaluate the parent pipeline trained on line A tested on line B, within- vs across-tissue.
3. Add cell-line expression context as a feature; measure whether context features close the across-tissue gap.

## Success gates (locked before results)
- G1: empirical within-tissue synergy correlation r >= 0.4, else label noise bounds all models - reported as the ceiling.
- G2: across-tissue transfer AUC drop quantified with CI; context features must recover >= 50% of the drop or are declared non-sufficient.
- G3: tissue-level results reported individually, never pooled.

## Expected deliverable
`contextmap`: a transport matrix tool for synergy models - input a model, get its within/across-tissue certificate plus the empirical reproducibility ceiling.

## Failure/pivot rule
If empirical synergy is irreproducible even within tissue, publish the noise ceiling - an honest bound on what any synergy model can achieve.
