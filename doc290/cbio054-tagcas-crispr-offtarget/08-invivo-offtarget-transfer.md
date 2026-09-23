---
id: P17-08
title: "DishToBody: Transferring Off-Target Models From Cell Lines to In Vivo Editing"
parent: "CBIO054 - 3D-Aware CRISPR Off-Target Prediction (source abstract, 2026)"
---

# DishToBody

**Parent project:** CBIO054 (validated in cultured cells; therapies edit living tissue).

## Premise
Off-target models are trained on cell-line assays; therapies edit liver, muscle, and blood in living organisms where chromatin states, editing kinetics, and cell-cycle context differ. Published in vivo off-target datasets (animal editing studies with genome-wide assays) are few but real, and ex vivo therapeutic programs (edited cells reinfused) sit in between. This project builds the transfer study the field lacks: cell-line model to ex vivo to in vivo, measuring the accuracy decay at each step and which features (dose, delivery, tissue chromatin) explain it. The deliverable is either a validated transfer correction or the honest measurement that in vivo prediction currently cannot be trusted - both change how trials screen.

## Data sources
- Published in vivo off-target studies (animal genome-wide assays; public deposits).
- Ex vivo therapeutic-program off-target data where published.
- crisprSQL + cell-line datasets: the training base.
- Published tissue epigenome references (ENCODE mouse/human tissue atlases).

## Method outline
1. Census all public in vivo and ex vivo off-target datasets with editing-context metadata.
2. Stepwise transfer evaluation: cell-line-trained model tested ex vivo, then in vivo.
3. Feature-correction search: which context features (dose, delivery, tissue ATAC) reduce decay.
4. Calibrate uncertainty for in vivo predictions explicitly.
5. Recommend per-program assay plans: when computation suffices, when empirical in vivo assays are non-negotiable.

## Success gates (locked before results)
- G1: transfer-decay curve measured across >= 2 context steps with CIs - the headline number.
- G2: >= 1 correction feature reduces decay measurably (>= 20% of the gap), or correction certified unsuccessful with the analysis.
- G3: assay-plan recommendations validated against published program decisions in >= 70% of cases.
- G4: honest-negative clause: certified in vivo unpredictability with the decay evidence is a full primary result.

## Expected deliverable
The transfer study (decay curves + corrections), DishToBody (editing protocol in; predicted in vivo risk with calibrated uncertainty + assay recommendation out), and the census of public in vivo off-target data.

## Failure/pivot rule
If in vivo datasets are too few for G1 (likely), pivot to the data-commons proposal: minimal reporting standards for in vivo off-target deposition, demonstrated by simulated power gains - gates re-locked.
