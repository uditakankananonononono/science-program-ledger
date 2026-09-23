---
id: P21-01
title: "Which Conclusions Hold: Parameter Identifiability and Uncertainty in the IL-6 ODE Model"
parent: "CBIO060 - A Mathematical Model of IL-6 in Breast Cancer (source abstract, 2023)"
---

# Which Conclusions Hold

**Parent project:** CBIO060 IL-6 TNBC Model (48-ODE model of IL-6 signal transduction in triple-negative breast cancer; sensitivity analysis and virtual drug-target screening).

## Premise
A 48-equation ODE model has many rate constants, and most are rarely measured in TNBC cells. Many parameter sets fit the same data equally well ("sloppy" models, Gutenkunst et al. 2007). If drug-target rankings from the sensitivity analysis change across equally good parameter sets, they are not yet reliable. This project measures which conclusions survive parameter uncertainty.

## Hypothesis
Fewer than half of the 48-ODE model's parameters are practically identifiable from realistic data, but the top-5 sensitivity-ranked targets stay in the top 10 across >= 80% of plausible parameter sets.

## Data sources (free/public)
- Published IL-6/JAK/STAT3 ODE models in BioModels (public SBML) as the structural reference and parameter source.
- Public STAT3 phosphorylation time courses in breast/TNBC lines (GEO/PRIDE, literature figures digitized with WebPlotDigitizer).
- Tools: AMICI or PEtab/pyPESTO (free) for fitting, profile likelihood and sampling.

## Method outline
1. Encode the 48-ODE model in SBML/PEtab.
2. Structural identifiability check (e.g., StructuralIdentifiability.jl).
3. Practical identifiability via profile likelihood against the available time-course data.
4. Sample the plausible parameter ensemble (MCMC or multi-start); redo sensitivity analysis for each set.
5. Report rank stability of drug targets across the ensemble.

## Success gates (locked before results)
- G1: identifiability status reported for all parameters (structural and practical).
- G2: top-5 targets remain in top 10 for >= 80% of ensemble members, or the unstable ranking is the headline.
- G3: model fits held-out time points with normalized RMSE <= 0.2.

## Expected deliverable
An SBML/PEtab version of the model, an identifiability table, and a robustness-scored target ranking.

## Failure/pivot rule
If rankings are unstable (G2 fails), design the minimal set of new measurements (optimal experimental design) that would most reduce ranking uncertainty.
