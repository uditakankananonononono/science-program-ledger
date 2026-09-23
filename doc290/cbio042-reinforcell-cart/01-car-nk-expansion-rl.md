---
id: P13-01
title: "CAR-NK Bioreactor RL: Reinforcement-Learning Optimization of Natural Killer Cell Expansion"
parent: "CBIO042 - ReinforCell: CAR-T Cell Optimization Solution (ISEF 2026 Grand Award)"
---

# CAR-NK Bioreactor RL

**Parent project:** CBIO042 ReinforCell (CAR-T exhaustion optimization via RL manufacturing agents, in vivo prediction, and clinical action policies).

## Premise
ReinforCell optimizes CAR-T cells, but CAR-NK therapy is the faster-moving allogeneic modality: NK cells carry no graft-versus-host risk, can be manufactured off-the-shelf from cord blood or iPSCs, and suffer a *different* failure mode (short in vivo persistence rather than classical exhaustion). This project builds a reinforcement-learning agent that optimizes CAR-NK ex vivo expansion - cytokine pulsing (IL-2/IL-15/IL-21), feeder-cell ratios, and media exchange timing - fitted on a state-space dynamical model learned from published NK expansion time courses and single-cell persistence signatures. The twist on the parent: instead of minimizing T-cell exhaustion, the agent maximizes *in vivo persistence potential*, operationalized as a score built from single-cell markers of memory-like NK phenotypes.

## Data sources
- NCBI GEO / CELLxGENE: cord-blood and peripheral-blood NK single-cell RNA-seq datasets (including the Liu et al. NEJM 2020 cord-blood CAR-NK trial companion data where deposited).
- Published NK expansion kinetics (doubling-time and fold-expansion curves) from open-access manufacturing papers.
- ImmuneCELL/cell-surface marker panels from the Human Protein Atlas for persistence/exhaustion marker validation.
- IndPenSim public industrial fermentation simulation dataset as an RL training sandbox for control-policy pretraining before biological fitting.

## Method outline
1. Curate 20+ published NK expansion protocols with digitized growth curves; normalize to a common state representation (cell density, viability, nutrient proxies).
2. Fit a stochastic state-space model (Neural ODE or Gaussian-process dynamics) per protocol family; validate on held-out curves.
3. Derive a persistence-potential reward from scRNA data: memory-like NK score (e.g., high IL7R, low LAG3/TIM3/HAVCR2) vs. terminal-differentiation score.
4. Pretrain a soft-actor-critic RL agent in the IndPenSim sandbox, then fine-tune on the NK dynamics model with safety constraints (never drop viability below protocol floor).
5. Compare the learned policy against standard-of-care schedules on yield, viability, and persistence score; ablate each reward component.

## Success gates (locked before results)
- G1: dynamics model predicts held-out expansion curves with R^2 >= 0.80.
- G2: RL policy beats the best published static protocol by >= 20% on composite yield-persistence objective in silico across >= 3 protocol families.
- G3: learned policy never recommends a state with predicted viability < 90% of the standard-protocol floor.
- G4: ablation shows the persistence reward component contributes measurably (>= 5% objective delta) - if not, the finding is the boundary: persistence is not controllable via expansion scheduling, which is itself publishable.

## Expected deliverable
A simulator-validated CAR-NK expansion policy, an open "NK-expand" tool (input: starting cell source and target dose; output: recommended cytokine/feed schedule with confidence bounds), figures on policy behavior, and an honest-negative appendix if G4 fails.

## Failure/pivot rule
If expansion-schedule control proves weak (G2/G4 fail), pivot the project to *starting-material selection*: use the same scRNA data to predict which donor/source phenotypes yield the highest persistence score - gates amended and re-locked before any new results are read.
