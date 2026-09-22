# DOC-2-096 R2: Archived Temporal Validation

**Date:** 21 September 2026  
**Status:** LOCKED-GATE FAILURE

## Answer
Archived ClinVar snapshots solved R1's identifiability problem but falsified the simple transport claim. A model using R0 reliability improved Brier score by 4.50% versus raw counts in development (2020->2023), below the locked 5% gate. In locked replication (2023->current) it was 0.16% worse than raw counts. Replication calibration slope was 0.132, far outside the required 0.8-1.2. Negative controls lost only about 19% of top-decile enrichment, not the required 50%. The reliability signal ranks some future changes but does not provide stable calibrated triage across release eras.

## Data integrity
Exact December 2020 and December 2023 variant and submission archives were downloaded from NCBI, checksummed and retained locally. Current data came from R0's checksum-frozen snapshot. Each release's gene-condition edges were built solely from its own variant table. No current IDs or review statuses were backfilled.

The ontology crosswalk was developed from 2020 only: 24,565 identifiers with 255 ambiguous components. Later identifiers not present in 2020 stayed unmapped/self-labeled. This preserves prospective semantics at the cost of later fragmentation.

## Temporal cohorts
The 2020->2023 cohort had 30,990 baseline edges and 5,132 later conflict-emergence or review-upgrade events. The 2023->current replication had 49,548 edges and 6,062 events. Both exceeded the minimum event gates.

## Models and prospective metrics
Models were fit on 2020->2023 and applied unchanged to 2023->current.

| Model | Development Brier | Replication Brier | Replication calibration slope | Replication top-decile enrichment |
|---|---:|---:|---:|---:|
| Raw counts | 0.1369 | 0.1089 | 0.822 | 0.47x |
| Positive-only | 0.1379 | 0.1077 | 2.629 | 0.57x |
| R0 reliability | 0.1308 | 0.1090 | 0.132 | 2.30x |

The striking combination of 2.30x enrichment and poor Brier/calibration means the score can rank a volatile subset while its absolute probabilities do not transport. It must not be used as a calibrated decision threshold.

## Negative controls
Within-source label permutation and ontology-score randomization produced mean top-decile enrichment near 1.0. Because the development reliability enrichment was only 1.24x, this is a loss of about 19%, not 50%. The locked control gate failed.

## Interpretation
ClinVar growth and curation changed between eras. The meaning of an edge's benign/pathogenic ratio is not stationary as submission volume, review practices, disease mapping and laboratories change. Reliability weighting remains useful for descriptive topology and perhaps ranking, but not as an era-invariant calibrated predictor.

## Limits
Aggregate variant tables, not fully reconstructed SCV trajectories, drove edge states. Review-upgrade and conflict-emergence are combined outcomes. Submitter-blocked bootstrap and gene-size covariates remain incomplete and therefore cannot rescue the failed result. Condition self-labeling for post-2020 unknown IDs fragments some trajectories. The failure is already decisive on the locked transport/calibration gates.

## Next round
Separate ranking from calibration. Test era-specific recalibration with a third archived snapshot while preserving temporal order; add SCV-level lab trajectories and gene testing burden; model ontology arrival as censoring. A successful tool should say "high-priority for review," not output a clinical probability.
