---
id: P21-02
title: "Minimal IL-6 Model: Reducing 48 Equations to the Core That Drives Predictions"
parent: "CBIO060 - A Mathematical Model of IL-6 in Breast Cancer (source abstract, 2023)"
---

# Minimal IL-6 Model

**Parent project:** CBIO060 IL-6 TNBC Model (48-ODE model of IL-6 signal transduction in triple-negative breast cancer; sensitivity analysis and virtual drug-target screening).

## Premise
Large ODE models are hard to fit, share and test. Often a handful of reactions controls the outputs that matter - here, IL-6 secretion and STAT3 activity. Model reduction (time-scale separation, sensitivity-based lumping) finds that core. A small model is easier to calibrate to real data and easier for others to reuse.

## Hypothesis
A reduced model with <= 12 equations reproduces the full model's IL-6 and pSTAT3 dynamics (normalized RMSE <= 0.1) and preserves the top-5 drug-target ranking.

## Data sources (free/public)
- The parent's 48-ODE model (rebuilt from its published equations) and BioModels IL-6 pathway models.
- Public pSTAT3 time-course data (see P21-01) for checking reduced-model fits.
- Tools: COPASI, Tellurium, or python-libsbml (free).

## Method outline
1. Run global sensitivity (Sobol) on the full model for IL-6 secretion and pSTAT3 outputs.
2. Remove or lump low-sensitivity species; apply quasi-steady-state assumptions to fast reactions.
3. Compare full vs reduced trajectories under baseline and under each simulated drug.
4. Refit the reduced model to public data and compare fit quality with the full model (AIC).

## Success gates (locked before results)
- G1: reduced model <= 12 equations with normalized RMSE <= 0.1 vs full model across 20 simulated conditions.
- G2: top-5 targets preserved (same set, any order).
- G3: reduced model fits public data with AIC no worse than the full model.

## Expected deliverable
A reduced SBML model, a reduction map (which parts matter), and a side-by-side validation.

## Failure/pivot rule
If no small model preserves rankings (G2 fails), report which pathway modules cannot be removed - that itself identifies where the biology is complex.
