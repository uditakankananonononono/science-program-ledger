---
id: P22-05
title: "How Many Labels: Minimal Annotation Budget to Adapt Cellpose to a New Tissue"
parent: "CBIO064T - Automated 3D Cell Visualization (source abstract, 2025)"
---

# How Many Labels

**Parent project:** CBIO064T Automated 3D Cell Visualization (Cellpose 2.0 auto-outlining of z-stack slices, cross-height/time cell linking, mesh rendering and side-by-side comparison).

## Premise
The parent removed manual tracing by using pretrained Cellpose. Pretrained models often fail on unusual tissues, so users still need to label some cells to fine-tune. Cellpose 2.0 introduced human-in-the-loop training, but how many labeled cells are needed, and which cells to label, is not well mapped across tissue types.

## Hypothesis
Fine-tuning on 50-200 labeled cells recovers >= 90% of the AP of a model trained on all labels, and choosing cells by model uncertainty needs half as many labels as random choice.

## Data sources (free/public)
- Cellpose dataset (public, research use) and TissueNet (Greenwald et al. 2022, public for non-commercial use).
- PlantSeg and CTC datasets for 3D-specific tissues.
- Cellpose 2.0/3.0 code (free).

## Method outline
1. For each of >= 5 tissue types, hold out a test set; start from pretrained Cellpose "cyto" models.
2. Fine-tune with 10, 25, 50, 100, 200, 500 labeled cells chosen randomly or by uncertainty (flow-field disagreement across augmentations).
3. Score AP@0.5 and learning curves; repeat with 5 random seeds.
4. For 3D data, compare labeling full cells vs labeling single slices.

## Success gates (locked before results)
- G1: learning curves reported for all tissues with seed CIs.
- G2: <= 200 labels reach >= 90% of full-label AP in >= 3 of 5 tissues.
- G3: uncertainty sampling saves >= 40% of labels vs random at the 90% level, or the null is reported.

## Expected deliverable
A labeling-budget guide and an active-learning plugin that tells users which cells to outline next.

## Failure/pivot rule
If uncertainty sampling does not help (G3 fails), test diversity-based selection (cluster embeddings, pick one per cluster) as the alternative.
