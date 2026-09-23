---
id: P17-10
title: "TopologyTax: An Auditor for Whether 3D Features Earn Their Cost in CRISPR Models"
parent: "CBIO054 - 3D-Aware CRISPR Off-Target Prediction (ISEF 2026 Grand Award)"
---

# TopologyTax

**Parent project:** CBIO054 TAG-Cas (3D features improved prediction; Hi-C data is expensive and often unavailable).

## Premise
TAG-Cas showed 3D topology helps; it didn't answer when it helps enough to matter. Hi-C at useful resolution costs thousands of dollars per cell type and most clinical contexts will never have it. Meanwhile many published models bolt on structural features without rigorous ablation. This project builds the audit: a standardized ablation harness that measures the marginal value of 3D features across every public off-target dataset and model class, maps where 3D earns its cost (which guides, which chromatin contexts, which applications), and produces the decision tool: given your cell type, budget, and accuracy requirement, should you buy the Hi-C or not?

## Data sources
- crisprSQL + all public off-target datasets (public).
- ENCODE/4DN Hi-C at multiple resolutions (public) for the resolution-scaling arm.
- Published off-target models (open weights/code where available) for cross-model audit.
- Cost data from public Hi-C core-facility rate cards for the decision analysis.

## Method outline
1. Standardized ablation harness: identical training protocol, features toggled, across datasets.
2. Resolution-scaling arm: 1kb vs. 10kb vs. 50kb Hi-C - where does value saturate?
3. Context mapping: which chromatin environments show the largest 3D benefit (heterochromatin-adjacent guides?).
4. Cross-model audit: do published models' claimed 3D benefits replicate under the harness?
5. Decision tool: accuracy requirement + budget + cell-type data availability -> buy/compute/skip recommendation.

## Success gates (locked before results)
- G1: ablation harness runs across >= 5 datasets and >= 3 model classes with CIs.
- G2: resolution-saturation point identified (or certified absent) - the practical purchasing answer.
- G3: >= 1 published model's 3D benefit fails to replicate under standardized ablation, or all replicate - either way the audit report names numbers.
- G4: decision tool's recommendations validated against the measured benefit distribution (no recommendation regime unsupported by data).

## Expected deliverable
TopologyTax (audit harness + decision tool), the marginal-value map of 3D features across contexts, and the replication audit of published 3D claims - the cost-benefit referee for structural CRISPR modeling.

## Failure/pivot rule
If published models can't be run under the harness (broken code/no weights - itself a finding), pivot to the reproducibility report: which 3D-CRISPR claims are auditable at all - gates re-locked around the subset that is.
