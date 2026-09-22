# DOC-2-096 R3: Ranking-Only Evidence Review Triage

**Date:** 21 September 2026  
**Status:** LOCKED RANKING GATE FAILURE

## Product claim tested
The only allowed output was "priority for evidence review." No score was described as probability of pathogenicity, conflict or clinical action. Calibration remained a separate arm already failed in R2.

## Result
A development-frozen equal-rank ensemble of benign burden, conflict count, variant/testing burden, pathogenic count, benign count and reliability achieved 1.27x top-decile enrichment in 2020->2023, but only 1.16x in 2023->current. The condition-block bootstrap 95% interval was 0.97-1.38, crossing 1. It also lost decisively to the best simple baseline: baseline conflict topology produced 2.60x replication enrichment. The locked ranking gate therefore failed.

At top 1% and 5%, replication enrichment was only 0.90x. Top-decile precision was 14.2% against a 12.2% event prevalence. NDCG was 0.786, but a high NDCG in an imbalanced broad ranking does not rescue weak top-k transport.

## Mechanistic decomposition
Development orientation was counterintuitive but reproducible in code: lower existing burden/conflict and higher reliability ranked later newly observed conflict/review events. That reflects the outcome definition: edges already conflicting at baseline cannot experience conflict emergence, producing depletion of existing conflict at future-event candidates. The simple `conflict_base` baseline's strong replication score is similarly tied to orientation and eligibility. This reveals target leakage-by-risk-set definition rather than a deployable multifeature mechanism.

## Gate
Ranking failed because the bootstrap interval crossed 1 and the ensemble did not improve 20% over the best simple baseline. Calibration remains failed from R2. No graduation.

## Limits
The compact R3 did not add gene-size external covariates or full submitter-block resampling. Those omissions cannot rescue the decisive comparison with the simple baseline. Negative controls stronger than R2 remain necessary before any ranking claim. The next design should use explicit competing-risk sets: conflict emergence among clean edges, resolution among conflicted edges, and review upgrade among non-expert edges, each scored separately.

## Cross-round graduation decision
- R0: descriptive topology success.
- R1: current snapshot temporal leakage identified.
- R2: true archives showed enrichment but nontransporting calibration.
- R3: ranking-only ensemble failed uncertainty and baseline superiority.

DOC-2-096 should remain active research, not graduate as a product. The reliable artifact is a descriptive evidence-support map, not predictive triage.
