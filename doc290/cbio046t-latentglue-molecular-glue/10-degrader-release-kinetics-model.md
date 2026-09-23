---
id: P16-10
title: "ReleaseSim: In Silico Design of pH-Responsive Degrader Delivery Particles"
parent: "CBIO046T - Expanding the Druggable Human Proteome Five-Fold (ISEF 2026 Grand Award)"
---

# ReleaseSim

**Parent project:** CBIO046T (calcium-alginate microparticles for oral glue delivery, validated in simulated GI fluids).

## Premise
The parent hand-built one delivery particle; this project turns that into computable design. pH-responsive oral delivery is a parameter search over polymer composition, crosslinking, coating, and particle size - and the literature holds decades of published release curves for alginate/chitosan systems that nobody has unified into a response surface. This project digitizes public release-kinetics datasets, fits mechanistic release models (diffusion-erosion families), and builds a simulator that proposes particle formulations meeting a target release profile (gastric protection, intestinal trigger) - compressing the parent's bench iteration loop into an in silico screen.

## Data sources
- Published alginate/chitosan microparticle release studies (open-access supplements with time-release curves).
- Polymer-property databases (public: PoLyInfo-class resources).
- Physiologically-based pharmacokinetic (PBPK) open frameworks for GI-transit modeling.
- The parent's own published particle parameters as an internal validation anchor.

## Method outline
1. Digitize >= 100 published release curves with formulation metadata into a harmonized database.
2. Fit mechanistic release-model families per formulation class; select by held-out curve prediction.
3. Build the inverse-design simulator: target profile in; ranked formulations + predicted curves out.
4. Validate against the parent's published particle behavior (blind on parameters where possible).
5. Uncertainty-first design: every proposal ships with predicted-curve confidence bands.

## Success gates (locked before results)
- G1: database covers >= 100 digitized curves with complete formulation metadata.
- G2: mechanistic models predict held-out release curves with <= 15% mean absolute error on cumulative release.
- G3: inverse design recovers formulations matching >= 3 distinct published target profiles (retrodiction test).
- G4: parent-particle validation: predicted release behavior consistent with the published pH 1.2/6.8 results within stated error - or the discrepancy investigated and reported.

## Expected deliverable
The open release-kinetics database, ReleaseSim (target profile in; formulations out), and the validation report including the parent-anchor analysis - a formulation-design tool for any oral bRo5 program.

## Failure/pivot rule
If literature curves prove too incomparable (G2 fails on assay heterogeneity), pivot to the reporting-standard deliverable: a minimal release-study metadata schema + the cleaned comparable subset, shown to restore model fit - gates re-locked.
