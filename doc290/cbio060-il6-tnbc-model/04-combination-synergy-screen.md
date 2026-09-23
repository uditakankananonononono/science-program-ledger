---
id: P21-04
title: "Combo Screen: In Silico Drug Combination Synergy for IL-6 Pathway Blockade"
parent: "CBIO060 - A Mathematical Model of IL-6 in Breast Cancer (source abstract, 2023)"
---

# Combo Screen

**Parent project:** CBIO060 IL-6 TNBC Model (48-ODE model of IL-6 signal transduction in triple-negative breast cancer; sensitivity analysis and virtual drug-target screening).

## Premise
The parent screened single drug-target pairs. Pathway feedback (e.g., SOCS3 negative feedback, compensatory signaling) often blunts single agents, which is why combinations are standard in oncology. An ODE model can score thousands of combinations quickly, and public combination screens let us check predictions.

## Hypothesis
Model-predicted synergy (Bliss excess on IL-6 output) for JAK inhibitor + IL-6R antibody + chemotherapy-proxy combinations correlates with measured synergy in public screens for TNBC lines (Spearman rho >= 0.3).

## Data sources (free/public)
- DrugComb portal (public drug combination screening data, includes breast lines).
- NCI ALMANAC combination screen (public, includes breast lines).
- The parent's model and P21-02 reduced model.

## Method outline
1. Map drugs in DrugComb/ALMANAC to model targets (JAK1/2, STAT3, gp130, IL-6R, NF-kB, MEK, PI3K where modeled).
2. Simulate dose grids for all pairs; compute Bliss and Loewe synergy on IL-6 secretion and pSTAT3.
3. Compare predicted vs measured synergy for matched pairs in TNBC lines (measured on viability - note the output mismatch).
4. Rank untested combinations by predicted synergy and robustness across the P21-01 parameter ensemble.

## Success gates (locked before results)
- G1: >= 10 matched drug pairs with measured TNBC data; otherwise validation is declared underpowered.
- G2: Spearman rho >= 0.3 between predicted and measured synergy, or the null is reported.
- G3: top-ranked untested combos robust in >= 80% of parameter sets.

## Expected deliverable
A combination synergy atlas for the IL-6 pathway and a ranked list of untested pairs.

## Failure/pivot rule
If validation fails (G2), pivot to explaining the gap: add a simple viability module linking IL-6 signaling to growth and test whether the output mismatch explains it.
