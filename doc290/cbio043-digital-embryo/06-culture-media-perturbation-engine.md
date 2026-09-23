---
id: P14-06
title: "MediaFormulator: In Silico Culture-Media Optimization via Perturbation Modeling"
parent: "CBIO043 - Digital Embryo: Multi-Omic Arrest Prediction (source abstract, 2026)"
---

# MediaFormulator

**Parent project:** CBIO043 Digital Embryo (perturbation engine validated against 85 compounds).

## Premise
The Digital Embryo's perturbation engine simulates compounds on an embryo's omic profile; this project points that engine at the variable clinics actually control: culture-media formulation. Commercial embryo media are proprietary black boxes chosen by brand loyalty, yet decades of published media-comparison studies (and mouse/human embryo responses to specific components - glucose, amino acids, antioxidants, growth factors) are public. This project builds a composition-to-outcome response surface from every published media-comparison dataset, then uses the perturbation approach to propose formulation tweaks ranked by predicted arrest-risk reduction - computational formulation science for a market that has never had it open.

## Data sources
- Published media-comparison RCTs and cohort studies (open-access supplements with outcome rates).
- MetaboLights/Metabolomics Workbench: embryo response-to-media metabolomics.
- Mouse embryo media-response datasets on GEO (dose-response to individual components).
- Published commercial-media composition disclosures (patent literature, public).

## Method outline
1. Extract component-level outcomes from published media comparisons into a formulation-response database.
2. Fit dose-response surfaces per component (mouse data for density, human for anchor points).
3. Build a composition simulator: predicted arrest/blastocyst rate for arbitrary formulations under uncertainty.
4. Rank single-component changes and small combination changes by predicted effect; cross-check top predictions against published head-to-head trials not used in fitting.
5. Flag unsafe directions (components with known toxicity thresholds) as hard constraints.

## Success gates (locked before results)
- G1: formulation-response database covers >= 15 components and >= 30 studies.
- G2: simulator reproduces the direction of effect for >= 70% of held-out published comparisons.
- G3: >= 3 proposed formulation changes ranked high are NOT already standard in commercial media (novelty check) - or the finding is that current media are already near the surface optimum, which redirects the field.
- G4: all proposals labeled in-silico; safety constraints never relaxed by the optimizer.

## Expected deliverable
The open formulation-response database, the "MediaFormulator" simulator with ranked formulation proposals, and the validation report against held-out trials.

## Failure/pivot rule
If published comparisons are too confounded for G2 (clinic effects dominate media effects), pivot to a meta-science result: quantify how little the media literature can actually say about formulations - plus the minimal experiment design that would fix it.
