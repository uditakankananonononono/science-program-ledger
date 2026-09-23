---
id: P21-03
title: "Model Meets DepMap: Checking Model-Predicted IL-6 Targets Against Genetic Dependencies in TNBC Lines"
parent: "CBIO060 - A Mathematical Model of IL-6 in Breast Cancer (source abstract, 2023)"
---

# Model Meets DepMap

**Parent project:** CBIO060 IL-6 TNBC Model (48-ODE model of IL-6 signal transduction in triple-negative breast cancer; sensitivity analysis and virtual drug-target screening).

## Premise
The parent's sensitivity analysis names pathway components whose inhibition should most reduce IL-6. A model prediction is only a hypothesis. DepMap has CRISPR knockout screens across dozens of breast cancer lines, including many TNBC lines. If a model-predicted target matters, knocking it out should hurt TNBC lines, especially those with high IL-6 pathway activity.

## Hypothesis
Model-ranked top targets show stronger CRISPR dependency in IL-6-high TNBC lines than in IL-6-low lines (difference in Chronos score <= -0.1, p < 0.05) for at least 2 of the top 5.

## Data sources (free/public)
- DepMap public release: CRISPR (Chronos) gene effects, expression, and cell line annotations.
- CCLE secretome/cytokine data where available; IL6 and IL6R expression as proxies.
- PRISM drug-repurposing screen for JAK/STAT3 inhibitor sensitivity.

## Method outline
1. Classify breast lines as TNBC by annotation; split by IL-6 pathway score (IL6, IL6R, IL6ST, JAK1, STAT3 target genes).
2. Compare Chronos scores for each model-ranked component between IL-6-high and IL-6-low lines.
3. Compare PRISM sensitivity to JAK/STAT3 inhibitors across the same split.
4. Check whether model ranking correlates with dependency ranking (Spearman) across all modeled components.

## Success gates (locked before results)
- G1: >= 2 of top-5 targets show IL-6-context-specific dependency (p < 0.05, FDR-adjusted within the set).
- G2: rank correlation between model sensitivity and dependency reported with CI; negative or null is kept.
- G3: line counts per group stated; groups with < 5 lines labeled exploratory.

## Expected deliverable
A model-vs-DepMap concordance table and a short list of targets supported by both.

## Failure/pivot rule
If no concordance (G1 fails), test whether the model's predictions match dependency in co-culture or cytokine-stimulated conditions using public perturbation data, since DepMap screens lack paracrine IL-6.
