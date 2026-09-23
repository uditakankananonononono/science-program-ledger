---
id: P02-07
title: "Repurposing Approved Drugs as Ferroptosis Modulators in AD: A Signature-Reversal Screen"
parent: "CBIO006 - Biclonal Antibodies to Prevent Ferroptosis in AD (source abstract, 2025)"
---

# Repurposing Approved Drugs as Ferroptosis Modulators in AD

**Parent project:** CBIO006 - de novo antibody development; a repurposed brain-penetrant drug would reach clinic years faster.

## Premise
Approved drugs that reverse the AD ferroptosis transcriptional signature may already exist in public perturbation data.

## Hypothesis
>= 10 approved, brain-penetrant compounds sit in the top 1% of signature-reversal scores with mechanism-consistent enrichment (iron/GSH/lipid-peroxidation).

## Data sources (free/public)
- LINCS L1000 perturbation signatures (CLUE/iLINCS public); DrugBank; ChEMBL; published CNS-penetrant drug lists.
- AD ferroptosis signature from P02-01.

## Method outline
1. Compute the locked AD ferroptosis signature; query L1000 for anti-correlating compound signatures (reversal score).
2. Filter to approved drugs with brain-penetration evidence; rank by reversal strength, mechanism plausibility, safety class.
3. Validate top hits against independent AD transcriptomes and DepMap ferroptosis-dependency context; every hit traceable to raw signature IDs.

## Success gates (locked before results)
- G1: >= 10 approved brain-penetrant hits at top-1% reversal with consistent direction across >= 2 cell contexts, else screen declared empty at that bar.
- G2: hits enriched for iron/GSH/lipid-peroxidation mechanisms vs random approved drugs (p < 0.01).
- G3: full provenance per hit - reproducible end to end.

## Expected deliverable
`ferrorep`: signature-reversal screening toolkit (query/filter/rank/audit) with the frozen AD signature and a ranked, fully sourced hit list.

## Failure/pivot rule
An empty or mechanism-random screen is reported as such: no credible approved-drug ferroptosis reversers exist in L1000 at the locked bar - redirecting effort to de novo modalities.
