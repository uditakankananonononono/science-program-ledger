---
id: P16-06
title: "bRo5 Navigator: Property Prediction for Beyond-Rule-of-5 Degraders"
parent: "CBIO046T - Expanding the Druggable Human Proteome Five-Fold (source abstract, 2026)"
---

# bRo5 Navigator

**Parent project:** CBIO046T (oral microparticle delivery was needed because glues/degraders sit beyond rule-of-5 space).

## Premise
The parent's pH-responsive microparticles are a workaround for a deeper problem: degraders violate every oral-drug property rule, and standard ADME models trained on conventional drugs mispredict them. Public bRo5 datasets now exist with measured permeability, solubility, and exposure for large polar molecules. This project builds degrader-specific property models (permeability, oral bioavailability proxies), quantifies exactly where conventional models fail on degraders, and produces a design-stage filter: will this candidate need formulation heroics (like the parent's microparticles), or is it conventionally developable?

## Data sources
- Public bRo5/PROTAC property datasets (published measured-permeability and PK sets).
- TDC ADME benchmarks (public).
- ChEMBL (public): property records for large molecules.
- Published PROTAC clinical-candidate structures + disclosed PK (open literature).

## Method outline
1. Assemble measured property data for degraders/bRo5 molecules with strict assay harmonization.
2. Benchmark conventional ADME models on degraders; map the failure region.
3. Train degrader-specific models (descriptor + pLM/fingerprint hybrids) with calibrated uncertainty.
4. External validation on disclosed clinical PROTAC PK.
5. Build the developability triage filter with formulation-needed flags.

## Success gates (locked before results)
- G1: conventional-model failure on degraders quantified (error inflation vs. conventional drugs, with CIs) - publishable standalone.
- G2: degrader-specific model improves permeability prediction R^2 by >= 0.15 over conventional baselines, or certified that public data cannot yet beat them.
- G3: clinical-PROTAC external validation: prediction intervals cover measured values for >= 80% of disclosed candidates.
- G4: triage filter agreement with known formulation-heavy vs. conventionally-oral degraders >= 80%.

## Expected deliverable
The bRo5 Navigator tool (candidate SMILES in; developability verdict + property predictions + formulation flag out), the failure-map of conventional ADME on degraders, and the harmonized property dataset.

## Failure/pivot rule
If public data proves too small for G2, pivot to the data-deficit quantification: exactly which measurements, on which compound classes, would unlock degrader ADME modeling - an agenda paper with power analysis, gates re-locked.
