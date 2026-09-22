# SP-002 Protocol Draft - Universal Confounder Stress Test for Bio-AI

**State:** DRAFT, NOT FROZEN. No endpoint modeling has begun.

## Scientific claim under test
A model-agnostic stress-test suite can detect optimism caused by dependence, cohort/batch structure, missingness, prevalence shift, and subgroup instability, and its audit score will predict the magnitude of performance loss under genuinely independent evaluation.

## Domains
1. Operational tabular: UCI Diabetes 130-US Hospitals, binary 30-day readmission. Unit is unique patient; recurrent encounters create a known leakage pathway.
2. Multi-study transcriptomics: curatedBreastData/MetaGxData candidate, endpoint and cohorts to be finalized only after metadata feasibility. Unit is patient/sample; study accession is external-validation group.
3. A third independent domain is required before freeze, preferably another multi-cohort biological dataset with explicit study or center labels and open redistribution.

## Locked-analysis intent
- Compare naive random row split against patient/group split, leave-study-out split, and order/time-proxy split where defensible.
- Baselines: prevalence-only, regularized logistic regression, random forest/gradient boosting only if computationally justified.
- All preprocessing, imputation, feature filtering, encoding, and correction must fit only on training data. A deliberately leaky pooled-preprocessing arm will quantify avoidable optimism but never be presented as a valid model.
- Primary quantity per domain: naive-minus-rigorous discrimination delta with cluster/bootstrap uncertainty.
- Audit dimensions: duplicate/dependence leakage, group/cohort delta, missingness reliance, prevalence sensitivity, subgroup worst-case gap, calibration drift, and train-test feature shift.
- Ablations: remove each audit dimension; compare composite against single checks.
- Negative controls: shuffled labels; random group labels; synthetic batch indicator injected after split only for test harness validation (not scientific evidence).

## Proposed success gate (not frozen)
All required:
1. Across at least three real domains, the audit risk score predicts external/generalization loss with Spearman rho >= 0.60 and cluster-bootstrap 95% lower bound > 0.
2. At least two domains show a preregistered, statistically supported optimism delta under naive versus rigorous evaluation, demonstrating the suite catches real rather than hypothetical failure.
3. A fixed audit threshold achieves >=80% sensitivity for materially optimistic configurations (delta >=0.05 AUROC or equivalent) with >=60% specificity under nested held-out configuration evaluation.
4. The full audit outperforms every single-dimension ablation on configuration-level AUROC for detecting material optimism.
5. Reproducibility and product acceptance tests pass; no data leakage in the valid arms.

Failure policy: failure of any required gate makes SP-002 a negative experiment. Preserve all results, figures, diagnostics, and lessons; no success paper.

## Statistical principles
The independent unit is the patient or study, never repeated predictions. Bootstrap and permutation tests respect those units. Multiple primary comparisons use Holm control. Confidence intervals accompany all deltas. No post hoc threshold selection on the evaluation domains.

## Product target
A command-line/library audit that accepts predictions, labels, group IDs, timestamps/order, subgroup fields, and optional feature summaries, then emits machine-readable findings and a professional evidence report. Product usefulness is evaluated separately from scientific success; commercial framing cannot rescue a failed scientific gate.
