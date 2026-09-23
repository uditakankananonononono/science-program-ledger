---
id: P23-01
title: "Is It Quantum or Memory: Ablating the Leaky Integrator and Matching Model Complexity"
parent: "CBIO083 - Quantum Game Theory to Simulate Cancer Dynamics (source abstract, 2026)"
---

# Is It Quantum or Memory

**Parent project:** CBIO083 Quantum Game Theory Cancer Dynamics (Lindblad master-equation QGT model with leaky integrator fit to the Kaznatcheev alectinib/fibroblast NSCLC game assay; beat classical replicator models by 10-20%).

## Premise
The parent's best quantum model includes a leaky integrator - a memory term - and beats classical replicator models by 10-20%. But the classical baselines had no memory. The gain could come from memory, from extra parameters, or from genuinely quantum structure (coherence, interference). A fair test gives the classical model the same memory and the same parameter budget.

## Hypothesis
A classical replicator model with an identical leaky integrator and matched parameter count closes >= 70% of the gap to the quantum model.

## Data sources (free/public)
- Kaznatcheev et al. 2019 Nat Ecol Evol game assay data and code (github.com/kaznatcheev/GameAssay).
- QuTiP (free) for Lindblad dynamics; SciPy for classical ODEs.

## Method outline
1. Reproduce the parent's classical EGT baselines and best QGT model on the Kaznatcheev data (four environments).
2. Build classical models with the same leaky integrator (fitness driven by a decaying memory of past frequencies), and with delay-differential and stochastic variants.
3. Match free parameters; compare with AIC/BIC and leave-one-replicate-out prediction error.
4. Remove coherence from the quantum model (fully dephased Lindblad limit) to test whether quantum terms matter.

## Success gates (locked before results)
- G1: reproduction of the parent's 10-20% advantage within its reported range, or the discrepancy documented.
- G2: memory-matched classical model closes >= 70% of the gap (hypothesis supported) or < 30% (quantum structure supported); in between is reported as mixed.
- G3: dephased-quantum ablation result reported; all comparisons with bootstrap CIs over wells.

## Expected deliverable
An open model zoo (classical, memory-classical, quantum, dephased) with a fair comparison table.

## Failure/pivot rule
If quantum structure keeps its advantage (G2 favors quantum), pivot to identifying which data features coherence captures, by simulating synthetic data where the true generator is known.
