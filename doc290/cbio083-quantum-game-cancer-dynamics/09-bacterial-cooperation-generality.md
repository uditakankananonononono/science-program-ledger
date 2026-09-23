---
id: P23-09
title: "Beyond Cancer: Testing Quantum Game Models on Microbial Cooperation Data"
parent: "CBIO083 - Quantum Game Theory to Simulate Cancer Dynamics (source abstract, 2026)"
---

# Beyond Cancer

**Parent project:** CBIO083 Quantum Game Theory Cancer Dynamics (Lindblad master-equation QGT model with leaky integrator fit to the Kaznatcheev alectinib/fibroblast NSCLC game assay; beat classical replicator models by 10-20%).

## Premise
If quantum game models capture something general about frequency-dependent evolution, they should also help outside cancer. Microbial systems offer clean, well-replicated game dynamics - for example, beta-lactamase-producing and non-producing E. coli under ampicillin (Yurtsev et al. 2013 Mol Syst Biol), or yeast sucrose-cooperation games (Gore et al. 2009 Nature). These give a generality test with known mechanisms.

## Hypothesis
QGT's advantage over memory-matched classical models is smaller (< 5%) in microbial systems with well-mixed, well-understood mechanisms than in the cancer assay.

## Data sources (free/public)
- Yurtsev et al. 2013 beta-lactamase cooperation frequency data (public supplement).
- Gore et al. 2009 yeast cooperation data (published figures/supplement; digitize if needed).

## Method outline
1. Extract frequency trajectories from each microbial dataset (digitizing figures where raw data are not deposited, documented).
2. Fit classical, memory-classical and QGT models with matched parameter budgets.
3. Compare prediction error across systems (cancer vs microbial).
4. Relate advantage size to system features (spatial structure, noise level, mechanism knowledge).

## Success gates (locked before results)
- G1: >= 2 microbial datasets fit with all three model families.
- G2: QGT advantage per system reported with CI; hypothesis supported if microbial advantage < 5% while cancer advantage persists.
- G3: digitization error estimated (repeat digitization) and propagated.

## Expected deliverable
A cross-system comparison table showing where quantum game models add value.

## Failure/pivot rule
If QGT wins in microbes too, report it as evidence of a general modeling advantage and move to identifying the shared data feature it captures.
