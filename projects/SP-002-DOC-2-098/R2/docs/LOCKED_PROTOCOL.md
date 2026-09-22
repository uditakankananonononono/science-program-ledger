# SP-002 / DOC-2-098 Round 2 locked protocol

**Locked:** 2026-09-22 00:21 IST, before any Round 2 endpoint modeling or candidate-score inspection.
**Round role:** prospective transport and mechanism test prompted by R1 G3/G4 failure. R1 is development evidence only and remains unchanged.

## Question
Can a simplified, model-agnostic validation-hazard detector, frozen from the R1 failure pattern, detect material naive-validation optimism across three new biomedical/life-science domains without post-outcome reweighting?

## Source gate
All three untouched domains must be reconstructed from versioned open releases with stable independent units, licenses, checksums, and enough positive/negative configurations. Failure of any source/unit gate stops modeling for that domain and is reported, never silently replaced after outcomes are inspected.

1. **Multi-site clinical:** UCI Heart Disease, Cleveland/Hungarian/Switzerland/Long Beach VA. Unit = patient row; domain group = contributing hospital. Endpoint = any angiographic disease (`num > 0`). Naive = pooled stratified rows; rigorous = leave-one-hospital-out. Hospital identity excluded as predictor.
2. **Wearable signal:** UCI Human Activity Recognition Using Smartphones v1.0. Unit/group = subject; endpoint = six activities. Naive = pooled stratified rows; rigorous = leave-subjects-out using the published subject identities. No subject identifier as predictor. Primary metric = macro-F1; secondary = balanced accuracy.
3. **Molecular generalization:** OGB `ogbg-molhiv`, release resolved and pinned during source audit. Unit = molecule; group = Bemis-Murcko scaffold. Endpoint = HIV activity. Naive = stratified random molecules; rigorous = scaffold split. Molecular representation fixed before modeling to transparent radius-2 Morgan fingerprints (2048 bits) if RDKit version/source gate passes; otherwise stop the domain rather than substitute learned embeddings.

Source gate minimums: >=3 valid sites for Heart with both classes where estimable; >=20 subjects and all six activities for HAR; >=30,000 molecules, >=1,000 positives, and >=1,000 distinct scaffolds for molHIV. No Round 2 outcome metric may be computed until manifests for all retained domains pass.

## Models and configurations
Each domain must include a prevalence/majority baseline, regularized linear/logistic model, random forest, and one prespecified nonlinear mature estimator where computationally feasible (histogram gradient boosting for tabular/signal; fixed fingerprint logistic and random forest for molHIV). Hyperparameters are fixed in code before outcome evaluation. Preprocessing is fit inside training folds only.

Per domain, generate at least 12 auditable configurations spanning valid pipeline, intentionally pooled-preprocessing diagnostic, missingness-indicator ablation, feature-shift-robust subset, and model family. Invalid diagnostic arms are labeled and never recommended.

## Outcome scale
Primary optimism is bounded to [-1,1]: naive minus rigorous performance on AUROC for binary domains and macro-F1 for HAR. Material optimism is fixed at >=0.05. Regression-style unbounded normalization from R1 is retired, not retrospectively changed.

## Audit dimensions
Compute six evidence dimensions without using Round 2 optimism labels: dependence/unit-overlap hazard, feature shift, missingness reliance, prevalence sensitivity, calibration drift (one-vs-rest where needed), and subgroup/site instability. Every dimension has an evidence trace to raw split/configuration identifiers. No composite is issued with fewer than five dimensions.

## Frozen detector candidates
R1 motivated the candidates but does not estimate new weights.

- **Primary: simplified mean** = unweighted mean of dependence, feature shift, missingness, and subgroup/site instability. Positive if score >=0.40.
- **Reference: R1 full mean** = unweighted mean of all six dimensions. Positive if score >=0.35.
- **Safety rule:** positive if any of dependence, feature shift, or subgroup/site instability >=0.80.

No threshold, dimension bound, model weight, or channel inclusion may change after Round 2 optimism is inspected. Prevalence and calibration remain in the dossier even though excluded from the primary score.

## Uncertainty and inference
Save raw per-unit predictions. Bootstrap patients within site, subjects, and molecules within scaffold for 5,000 replicates. Primary model contrasts are paired within identical evaluation units; Holm adjustment is applied across model/domain primary contrasts. Domain-cluster uncertainty is reported separately and acknowledged as weak with only three new domains.

## Locked gates, all required
1. Source/unit manifests pass for all three domains; at least 36 total configurations and at least 8 material-positive plus 8 material-negative configurations.
2. Primary simplified detector pooled sensitivity >=0.80 and specificity >=0.60; domain-balanced sensitivity >=0.75; no domain sensitivity below 0.60 where both classes exist.
3. Primary detector AUROC >=0.75 and exceeds the R1 full mean by >=0.02; its 5,000-replicate scaffold/subject/site-aware bootstrap median advantage is positive in >=95% of replicates.
4. At least two new domains contain a nontrivial model with optimism >=0.05, paired Holm-adjusted p<0.05, and a 95% unit-bootstrap interval excluding zero.
5. Complete frozen controls pass: rigorous label-shuffle refits at chance; random-group rebuild does not create systematic optimism; held-out-only batch indicator does not improve valid training; valid unit overlap is zero; duplicate injection is detected; corrupt/missing IDs fail closed.
6. Clean pinned-environment rerun reproduces raw prediction hashes or documents deterministic-library tolerance <=1e-6; summary/gate metrics within 1e-8 when prediction hashes match.
7. Product acceptance passes: deterministic schema; missing-dimension/corrupt-input rejection; provenance trace; runtime and peak-memory ledger; readable evidence dossier; explicit “review support only” boundary.

Any failed gate makes R2 negative. If G2 or G3 fails, universal scoring closes and the output becomes a non-scoring evidence dossier/checklist. No success paper or product-safety claim is allowed on partial passage.

## Commercial/use boundary
Intended user: biomedical ML validation lead deciding whether an evaluation needs redesign or external validation. The artifact may prioritize human review. It must not certify clinical safety, regulatory conformity, diagnosis, treatment, or deployment readiness. Public aggregate/open research data only; no patient re-identification attempt. Economics are measured reviewer time, defect yield, false reassurance rate, compute/storage, and integration effort; no invented ROI.
