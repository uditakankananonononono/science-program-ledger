---
id: P04-06
title: "Does the Model Find Known Mechanisms? A Mechanism-Recall Benchmark Against Curated Synergy Biology"
parent: "CBIO012 - The Usage of Gene Synergy to Predict Drug Synergy (source abstract, 2025)"
---

# Does the Model Find Known Mechanisms?

**Parent project:** CBIO012 - claims interpretability through function dimensions; interpretability claims need recall measurement against curated mechanism pairs.

## Premise
A genuinely mechanistic model should rediscover textbook synergy mechanisms (e.g., antifolate + thymidylate synthase inhibition, PARP + HRD context, PI3K/MEK vertical combos) and flag the functions literature already implicates.

## Hypothesis
The parent's top function-attributions for known synergistic pairs recover curated mechanisms with recall >= 50% at top-5, and outperform attribution shuffles.

## Data sources (free/public)
- DrugCombDB curated synergy annotations (public); literature-curated mechanism lists from reviews (public).
- GoBERT embeddings + the parent attribution method.

## Method outline
1. Curate a locked mechanism gold set: combinations with published mechanistic explanations and the specific functions/pathways implicated.
2. Run the parent framework; extract per-pair top-attributed functions; compute recall@k against the gold mechanisms.
3. Null: attributions from target-shuffled embeddings; report attribution specificity.

## Success gates (locked before results)
- G1: mechanism recall@5 >= 50% on the gold set, else interpretability is declared aspirational, not demonstrated.
- G2: real attributions beat shuffle null by >= 2x recall (p < 0.01).
- G3: gold set and attribution extraction frozen before evaluation.

## Expected deliverable
`mechrecall`: the curated mechanism gold set (released) + an evaluation harness giving any interpretable synergy model a mechanism-recall score.

## Failure/pivot rule
If recall is low, publish it: current function-attribution does not recover known biology - the framework's interpretability claim is downgraded with evidence.
