---
id: P04-10
title: "From Predicted Synergy to Testable Trials: A Safety-Filtered Combination Triage Tool"
parent: "CBIO012 - The Usage of Gene Synergy to Predict Drug Synergy (source abstract, 2025)"
---

# From Predicted Synergy to Testable Trials

**Parent project:** CBIO012 - ranks synergistic pairs; clinical usefulness needs safety, availability, and novelty filtering.

## Premise
A predicted synergy is only valuable if the pair is safe enough to test, not already established, and mechanistically non-obvious. Public DDI and trial data make that triage computable.

## Hypothesis
Applying locked safety/novelty filters to the parent's ranked list leaves >= 20 high-scoring, non-obvious, safety-cleared combinations, >= 5 of which have supporting evidence in later-published literature or trials (checked after freezing).

## Data sources (free/public)
- DrugBank DDI + contraindication data (open tier); ONCOKB/FDA-approved combination lists.
- ClinicalTrials.gov API (public) for existing combination trials; PubMed for post-freeze evidence checks.

## Method outline
1. Freeze the parent's ranked synergy list.
2. Apply locked filters: remove known DDIs (major), approved standard-of-care pairs, and pairs already in >= phase 2 trials.
3. Rank survivors by synergy score x mechanistic novelty (embedding distance between targets); freeze top-20; post-freeze literature/trial evidence check at a locked date.

## Success gates (locked before results)
- G1: >= 20 survivors after filters, else the triage concludes the model's top hits are mostly known or unsafe - reported as the finding.
- G2: >= 5 of top-20 with post-freeze supporting evidence (exploratory, reported with base rates).
- G3: every filter decision logged per combination - fully auditable.

## Expected deliverable
`combotriage`: a web tool - paste ranked synergy pairs, get the safety/novelty-filtered shortlist with per-pair audit trail.

## Failure/pivot rule
If filters empty the list, publish the conclusion that top model hits are dominated by known/unsafe pairs - a direct, useful critique of synergy-model novelty.
