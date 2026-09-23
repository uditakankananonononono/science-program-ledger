# 31 - GO semantic similarity for predicting physical protein interactions: simGIC vs Resnik

Locked before any similarity score is computed.

Data: GO go-basic.obo (release 2026-07-26; is_a + part_of), GOA human GAF (generated 2026-05-21), STRING v12 human physical links (detailed) + protein.info for symbol mapping.
Leakage control: drop NOT annotations, all IPI-evidence annotations, and GO:0005515 "protein binding" (these are derived from interaction data).
IC: -log(fraction of annotated genes carrying the term after propagation), per ontology.
Pairs: positives = STRING physical experimental score >= 700, both proteins with >= 1 BP annotation; 10,000 sampled (seed 31) from 37,036 eligible. Negatives = 10,000 pairs drawn from the positives' protein multiset (degree-matched), excluding any STRING physical link at any score. Proteins without annotations in an ontology score 0 in that ontology.
Annotation sets are reduced to their most specific terms before pairwise measures.

Measures (per ontology BP/MF/CC):
- Resnik-BMA (baseline; Resnik 1995, best-match average as in Pesquita et al. 2009 review), Resnik-max, Lin-BMA.
- simGIC (Pesquita et al. 2008): sum IC of shared propagated terms / sum IC of union.
- simGIC-ALL: simGIC over the union of all three ontologies (ancestors propagated within each).

Metric: AUROC on the 1:1 set; 95% CI from 1000 stratified bootstraps (seed 31).
Gates:
- G1 (headline): AUROC(simGIC-BP) - AUROC(Resnik-BMA-BP) >= 0.01, CI lower bound > 0.
- G2: AUROC(simGIC-ALL) - max over ontologies of AUROC(Resnik-BMA) >= 0.02, CI lower bound > 0 (the max is chosen on the full test set, which favours the baseline).
- G3: AUROC(simGIC-BP) - AUROC(Resnik-max-BP) > 0, CI lower bound > 0.
If G1 fails: one post-hoc pivot, locked and pushed before scoring.
Caveats declared: annotation-rich (well-studied) proteins get both more annotations and more reported interactions; degree-matched negatives reduce but do not remove this. STRING "experimental" includes curated-database evidence.
