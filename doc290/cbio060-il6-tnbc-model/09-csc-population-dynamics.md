---
id: P21-09
title: "Stemness Loop: Coupling IL-6 Signaling to Cancer Stem Cell Population Dynamics"
parent: "CBIO060 - A Mathematical Model of IL-6 in Breast Cancer (source abstract, 2023)"
---

# Stemness Loop

**Parent project:** CBIO060 IL-6 TNBC Model (48-ODE model of IL-6 signal transduction in triple-negative breast cancer; sensitivity analysis and virtual drug-target screening).

## Premise
IL-6 is known to push breast cancer cells toward a stem-like state and to help convert non-stem cells into stem cells (Iliopoulos et al. 2011 PNAS). Stem-like cells resist chemotherapy and seed relapse. The parent's model stops at signaling; linking it to cell population dynamics asks the clinical question: does blocking IL-6 shrink the resistant pool?

## Hypothesis
A coupled signaling + two-population model predicts that IL-6 blockade combined with chemotherapy reduces the stem-like fraction after treatment by >= 30% relative to chemotherapy alone, consistent with published mammosphere and xenograft data.

## Data sources (free/public)
- Published quantitative data on IL-6-driven stem-cell conversion (Iliopoulos 2011; digitized figures).
- Single-cell TNBC atlas (GSE176078) for stem-like state markers and fractions.
- Parent model as the signaling module.

## Method outline
1. Build a two-population model (stem-like, non-stem) with division, differentiation and IL-6/pSTAT3-dependent dedifferentiation rates.
2. Couple pSTAT3 output from the parent (or reduced) model to the dedifferentiation rate.
3. Fit conversion parameters to digitized published data; simulate chemotherapy (kills non-stem faster) with and without IL-6 blockade.
4. Check predicted baseline stem-like fraction against atlas-derived fractions in TNBC tumors.

## Success gates (locked before results)
- G1: model reproduces published conversion dynamics within reported error bars.
- G2: predicted combination benefit on stem-like fraction >= 30%, robust in >= 80% of parameter sets, or the null is reported.
- G3: baseline stem-like fraction within the atlas-observed range.

## Expected deliverable
A coupled signaling-population model and predictions for combination schedules.

## Failure/pivot rule
If published data are too sparse to fit (G1 fails), report the specific measurements needed and give qualitative (sign-level) predictions only.
