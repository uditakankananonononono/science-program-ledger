---
id: P03-07
title: "Repurposing Approved Drugs for High-Risk Neuroblastoma: PRISM Screen Mining with Held-Out Validation"
parent: "CBIO008T - Deep Learning Pipeline for EZH2 Drug Discovery (source abstract, 2023)"
---

# Repurposing Approved Drugs for High-Risk Neuroblastoma

**Parent project:** CBIO008T - de novo design for NB; approved-drug repurposing could deliver candidates years sooner.

## Premise
The public PRISM drug-repurposing screens measured thousands of compounds across hundreds of cancer lines, including NB. Mining it with a trained model - validated on held-out lines - is a direct experiment, not a literature claim.

## Hypothesis
A model trained on PRISM viability + baseline omics identifies >= 5 approved/oncology drugs with NB-selective killing, and predictions validate in held-out NB lines at r >= 0.5.

## Data sources (free/public)
- PRISM Repurposing 19Q/24Q public datasets (DepMap portal).
- DepMap expression/copy-number; DrugBank approval status.

## Method outline
1. Build the NB line panel; compute per-drug NB-selectivity (viability in NB vs all other lineages, effect size + CI).
2. Train gradient-boosted models (drug features + line omics) predicting PRISM viability; leave-one-line-out validation restricted to NB lines.
3. Rank approved/oncology drugs by NB-selective predicted killing + mechanism plausibility; cross-check top hits against published NB screens.

## Success gates (locked before results)
- G1: >= 5 approved/oncology drugs with NB-selective effect (Cohen's d <= -0.5, FDR < 0.1), or the screen is declared empty at that bar.
- G2: held-out-line viability prediction Pearson r >= 0.5, else the model's ranking is declared unreliable.
- G3: hit list frozen before literature cross-check; agreement rate reported honestly.

## Expected deliverable
`nbrepurpose`: mined PRISM NB-selectivity atlas + the trained prediction tool and a ranked, fully sourced repurposing shortlist.

## Failure/pivot rule
If the screen is empty or prediction fails, publish the empty-screen result - NB shows no selective approved-drug vulnerability in PRISM - and quantify the power.
