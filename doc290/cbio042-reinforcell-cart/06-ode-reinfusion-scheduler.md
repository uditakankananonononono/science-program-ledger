---
id: P13-06
title: "Reinfusion Scheduler: Mechanistic ODE-Guided Timing of Repeat CAR-T Dosing"
parent: "CBIO042 - ReinforCell: CAR-T Cell Optimization Solution (source abstract, 2026)"
---

# Reinfusion Scheduler

**Parent project:** CBIO042 ReinforCell (sequential clinical decisions under uncertainty).

## Premise
When CAR-T response fades, clinicians face a timing problem with no quantitative tool: reinfuse now while tumor burden is low (but the suppressive TME persists), or wait and recondition? Mathematical oncology has published tumor-immune ODE models, but they are rarely fit to real post-CAR-T kinetics. This project fits mechanistic tumor-immune-persistence ODE models to published CAR-T expansion/persistence time series (digital droplet PCR and flow-cytometry kinetics reported in trial supplements), then uses the fitted models as simulators to optimize reinfusion and lymphodeletion timing - a mechanism-first complement to ReinforCell's pure-ML agents, with interpretable parameters (carrying capacity, kill rate, exhaustion rate) that clinicians can audit.

## Data sources
- Published CAR-T cellular-kinetic time series from open-access trial supplements (qPCR/ddPCR persistence curves).
- Published tumor-burden kinetics (M-spike, LDH, imaging volumetrics) from the same cohorts where available.
- Parameter priors from the mathematical-oncology literature (public).
- Stan/pymc ecosystems for Bayesian ODE fitting (open tools).

## Method outline
1. Digitize >= 15 published CAR-T persistence curves with response annotations.
2. Implement a candidate family of tumor-immune ODE models (predator-prey with exhaustion terms; carrying-capacity models).
3. Bayesian-fit each cohort; select model class by leave-one-cohort-out predictive error.
4. Use the fitted ensemble as a simulator; optimize reinfusion timing and dose via dynamic programming under toxicity constraints.
5. Validate: does the optimized schedule retrospectively match outcomes in cohorts where redosing was reported?

## Success gates (locked before results)
- G1: fitted ODE predicts held-out persistence curves with normalized RMSE <= 0.25.
- G2: identifiable parameters (95% credible interval width < 50% of prior width) for >= 3 of the core parameters; if parameters are non-identifiable, that is reported as the boundary.
- G3: simulated optimal schedules differ meaningfully (> 2 weeks shift or > 30% dose change) from standard practice in >= 1 scenario class, or the honest result is that current timing is already near-optimal.
- G4: retrospective redosing cases directionally match model ranking in >= 70% of the (small) available set - reported with the sample-size caveat.

## Expected deliverable
A fitted open kinetic-model library, a reinfusion-timing simulator with clinician-readable parameter reports, and a boundary analysis of which parameters routine clinical data cannot identify (guiding what trials should measure).

## Failure/pivot rule
If ODE fitting fails identifiability (G2), pivot to a *measurement-design* study: simulate which additional measurements (e.g., weekly ddPCR vs. monthly) would restore identifiability cheapest - a trial-design tool with re-locked gates.
