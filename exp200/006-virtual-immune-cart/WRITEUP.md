# DOC-1-006 — Virtual Immune System for CAR-T: infusion-product response classifier
**Verdict: DOCUMENTED BOUNDARY (candidate useful negative - adjudication requested).**

## Design (gates locked first, v1 + v2 both pre-registered)
Patient-level CAR-T fitness classifier: GSE151511 (Deng 2020 Nat Med, scRNA of 24
infusion products, 3-month PET/CT labels; CR vs PD, n=22: 9 CR / 13 PD). Frozen
22-marker panel (memory/exhaustion/cytotoxic/proliferation), frozen per-patient
aggregation (T-cell gated fractions + mean log-CPM, 24 features), logistic (v1) and
regularized MLP (v2, DL arm). Permutation discipline with the full pipeline inside
every shuffle. External cohort GSE197268 designated frozen but never touched - no
panel earned transport.

## Results
| gate | result | verdict |
|---|---|---|
| G1 v1 logistic | repeated-CV AUROC 0.552 +/- 0.097; obs 0.530 vs 200 nulls (max 0.855), p=0.42 | FAIL |
| G1 v2 MLP | CV 0.530 +/- 0.081; obs 0.427, p=0.70 | FAIL |

## Honest finding
Deng et al.'s published response correlate (memory-rich infusion products do better)
is NOT recoverable as simple patient-level marker-fraction aggregates at n=22 under
honest full-pipeline permutation testing. Null AUROCs reach 0.855 at this sample size:
any unpermuted CV number here would have been meaningless without the shuffle test.
This matches the PPD lesson at a smaller n: single-cohort CV is not evidence.

## Shipped
- code/aggregate.py: streaming 10x -> frozen per-patient marker features (validated,
  processes a 60MB infusion-product matrix in ~6s on 2 CPU).
- results/patient_features/*.json (22 patients), results/g1_metrics.json,
  g1_v2_metrics.json, GATES.md + GATES_v2.md (SHA-256'd).
- No CLI and no lab nomination shipped: nothing validated to ship. Aggregate tooling
  is reusable for any 10x cohort.

## Proposed re-angle (for main/user decision, NOT self-started)
Docking/interface arm under the same topic: predict CAR scFv-antigen interface from
sequence with a trained model, validated against the real FMC63-CD19 complex structure
(PDB 6AL5) - "which CAR designs bind best" as a structural-prediction experiment with a
named baseline (BepiPred/Discotope-class epitope predictors). Requires fresh gates.
