---
id: P04-09
title: "Cross-Domain Test: Do Gene-Function Embeddings Predict Antibiotic Combination Synergy?"
parent: "CBIO012 - The Usage of Gene Synergy to Predict Drug Synergy (source abstract, 2025)"
---

# Cross-Domain Test: Antibiotic Combination Synergy

**Parent project:** CBIO012 - oncology-only evaluation; a mechanism-based framework should transfer to bacterial combination therapy, where synergy data and need are both large.

## Hypothesis
Bacterial ortholog function embeddings predict antibiotic synergy in public screens with AUC >= 0.70, and the transferable features are core metabolism/repair functions rather than species-specific ones.

## Data sources (free/public)
- Public antibiotic combination screens (e.g., Brochado/EMAP-style datasets, GEO-linked screens).
- EggNOG/bacterial GO annotations (public); GoBERT-equivalent embeddings computable on bacterial genomes with public models.

## Method outline
1. Assemble the locked antibiotic synergy dataset with standardized labels (FICI/Bliss).
2. Compute function embeddings for drug-target orthologs; replicate the parent cosine-similarity framework; train classifier with held-out-drug splits.
3. Feature analysis: which function categories drive predictions; cross-species transfer test (train E. coli, test Salmonella/Acinetobacter subsets).

## Success gates (locked before results)
- G1: held-out-drug AUC >= 0.70, else cross-domain transfer is declared failed at this bar.
- G2: cross-species transfer AUC drop <= 0.10, else the framework is species-bound.
- G3: function-category attribution published with the same negative controls as P04-07.

## Expected deliverable
`abxsynergy`: the harmonized antibiotic-combination benchmark + trained predictor with a cross-species certificate.

## Failure/pivot rule
If transfer fails, publish the domain boundary of function-embedding synergy prediction - defining where the method applies is a real contribution.
