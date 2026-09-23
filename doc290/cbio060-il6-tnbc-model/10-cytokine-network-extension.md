---
id: P21-10
title: "Beyond IL-6: Extending the Model to the IL-6 / IL-8 / TNF Cytokine Network in TNBC"
parent: "CBIO060 - A Mathematical Model of IL-6 in Breast Cancer (source abstract, 2023)"
---

# Beyond IL-6

**Parent project:** CBIO060 IL-6 TNBC Model (48-ODE model of IL-6 signal transduction in triple-negative breast cancer; sensitivity analysis and virtual drug-target screening).

## Premise
TNBC cells secrete several inflammatory cytokines together, and they feed each other: TNF and IL-1 induce IL-6 via NF-kB, and IL-8 (CXCL8) is often co-secreted with IL-6. Blocking IL-6 alone may be offset by the rest of the network. This project extends the parent's model into a small cytokine network and asks whether IL-6 is the right node to target.

## Hypothesis
In a network model of IL-6, IL-8 and TNF signaling, NF-kB inhibition reduces combined cytokine output more than any single cytokine blockade, and IL-6 blockade alone raises IL-8 through compensatory feedback.

## Data sources (free/public)
- Published IL-6, NF-kB and TNF pathway models (BioModels) for structure and parameters.
- TCGA and METABRIC TNBC expression for co-expression of IL6, CXCL8, TNF and their receptors.
- LINCS L1000 and MCF10A ligand data (TNF, cytokine perturbations) for checks.

## Method outline
1. Merge the parent's IL-6 model with published NF-kB/TNF modules; add IL-8 production as an NF-kB/STAT3 output.
2. Calibrate shared nodes on public perturbation data; hold out one ligand condition for testing.
3. Simulate single blockades (IL-6R, IL-8R/CXCR1-2, TNF) and NF-kB or JAK inhibition; track all cytokine outputs.
4. Check tumor co-expression patterns for evidence of the predicted compensation.

## Success gates (locked before results)
- G1: merged model predicts the held-out ligand condition with normalized RMSE <= 0.25.
- G2: compensation (IL-8 rise after IL-6 blockade) predicted robustly (>= 80% of parameter sets), or reported absent.
- G3: NF-kB vs single-blockade comparison reported with ensemble uncertainty.

## Expected deliverable
A cytokine network model for TNBC and a node-level target ranking that accounts for compensation.

## Failure/pivot rule
If the merged model cannot fit held-out data (G1 fails), keep modules separate and report pairwise interaction predictions only.
