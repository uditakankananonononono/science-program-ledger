---
id: P13-04
title: "CRS Timing Policy: Learned Intervention Scheduling for Cytokine Release Syndrome"
parent: "CBIO042 - ReinforCell: CAR-T Cell Optimization Solution (source abstract, 2026)"
---

# CRS Timing Policy

**Parent project:** CBIO042 ReinforCell (the Clinical Action agent timing interventions under biological uncertainty).

## Premise
ReinforCell's clinical agent targets exhaustion; the deadlier acute problem is cytokine release syndrome (CRS), where the intervention question is brutally concrete: when to give tocilizumab or corticosteroids - too early may blunt CAR-T efficacy, too late risks ICU-level toxicity. Published cohorts report serial cytokine and clinical-grade trajectories. This project fits a stochastic deterioration model from those published trajectories and learns an intervention-timing policy that trades toxicity risk against efficacy preservation, turning an art practiced differently at every center into an auditable decision policy with quantified uncertainty.

## Data sources
- Published longitudinal cytokine panels from pivotal CAR-T trials and real-world cohorts (digitized from open-access supplements: ZUMA-1 biomarker studies, UPenn CART19 cohorts).
- ASTCT consensus CRS grading definitions (public) as the outcome schema.
- Open MIMIC-IV ICU data for calibration of generic inflammation-deterioration dynamics (pretraining only).
- Published tocilizumab-timing retrospective comparisons for external policy validation.

## Method outline
1. Digitize and harmonize published serial cytokine/grade trajectories into a common timeline format with outcome labels.
2. Fit a hidden Markov / neural point-process model of grade escalation conditional on interventions recorded.
3. Pretrain on MIMIC inflammation trajectories; fine-tune on CAR-T cohorts.
4. Learn a conservative contextual-bandit/RL timing policy with explicit safety constraints (never delay past grade-3 onset predictors).
5. Off-policy evaluate with doubly-robust estimators; stress-test on the most dissimilar held-out cohort.

## Success gates (locked before results)
- G1: escalation model predicts next-24h grade worsening with AUC >= 0.78 held-out.
- G2: learned policy's off-policy value estimate exceeds observed physician policy with lower 95% confidence bound > 0 improvement (doubly-robust).
- G3: policy agrees with published high-evidence timing recommendations in >= 80% of canonical scenarios (safety sanity check).
- G4: if off-policy confidence bounds are too wide to certify improvement, the deliverable becomes the quantified statement of how much more data CRS timing science needs - an honest data-deficit map.

## Expected deliverable
A validated escalation-prediction model, an auditable timing policy with uncertainty bounds, a "when-to-toci" decision-support report per scenario class, and the harmonized public CRS trajectory dataset (itself a reusable contribution).

## Failure/pivot rule
If published trajectories prove too sparse/harmonization-incompatible (G4 path), pivot to the data-deficit map as the primary deliverable: which measurements at which cadence would make CRS timing learnable - gates re-locked around the map's validation against center-level practice variation.
