# SP-002 / DOC-2-098 Round 2 technical report

**Date:** 22 September 2026  
**Verdict:** Negative, stopped before endpoint modeling because the supplied lock is insufficient to reproduce an unchanged detector/configuration run.

## Executive result
The supplied protocol file was verified before work began: SHA-256 `1e4fd59df50e558be7ed7dbae866a2313cd083aa60d932a370adf5b3ad11185f`, 6,762 bytes. Fresh official-source reconstruction passed every stated source minimum for Heart, HAR, and molHIV. However, the locked artifact does not contain the exact fixed hyperparameters, frozen configuration matrix, dimension formulas and bounds, split/fold seeds, robust feature subsets, pooled-preprocessing/missingness-ablation mechanics, or R1 detector implementation. Those are outcome-driving parts of the experiment. Choosing them during R2 would change the protocol while claiming “UNCHANGED.” No endpoint metric was inspected, and no post-outcome choice was made.

## Source audit

| Domain | Reconstructed result | Source gate |
|---|---:|---|
| UCI Heart | 920 rows; Cleveland 303 (164/139), Hungarian 294 (188/106), Switzerland 123 (8/115), Long Beach VA 200 (51/149), negative/positive | Pass |
| UCI HAR | 10,299 observations; 30 subjects; six classes; counts 1,722/1,544/1,406/1,777/1,906/1,944 | Pass |
| OGB molHIV | 41,127 molecules; 1,443 positive; split 32,901/4,113/4,113; 19,083 distinct Murcko scaffold strings; 7 RDKit-invalid SMILES | Pass |

The seven invalid SMILES are explicitly preserved and assigned an invalid/fail-closed scaffold marker in the audit. They were not silently dropped or repaired. RDKit 2025.03.6 and OGB 1.3.6 are pinned. Morgan radius 2 / 2,048-bit fingerprints were not computed because modeling was stopped before endpoint work once the frozen-specification gap was confirmed.

## Source hashes
- Heart ZIP: `b17cd273da9ce1caa4710fce80227ea454d4dbf9fcbc8e6a9121672751563adc`
- HAR ZIP: `c00b803081a5c797cd5e4b83700a9810b38d53d9d84e01917e090e1fdbc81031`
- molHIV ZIP: `47d747664b9e1653de5aac99bf26c015d88a3daa474f5a32f3fe5c014111375b`

Official records and acquisition URLs are recorded in `manifests/licenses_and_sources.md`. UCI records state CC BY 4.0. The OGB archive identifies release v1 (4 May 2020); OGB code is MIT licensed and the data derive from MoleculeNet, so downstream users must check underlying data terms.

## Protocol-compliance blocker
The locked text defines estimator families but not hyperparameters. It names five configuration classes but not the >=12 exact configurations/domain. It names six evidence dimensions but not their equations, bounds, aggregation across folds/sites/subjects/scaffolds, missing-data behavior, or trace construction. It gives score thresholds, but a threshold is not reproducible without the score inputs. It requires paired tests and Holm adjustment but does not identify the finite family of primary contrasts. It requires label shuffle/random-group/batch-indicator/duplicate/ID controls but does not freeze their generation procedures or seeds.

These omissions are load-bearing for G1-G6. Filling them now could turn sensitivity, specificity, detector AUROC, or optimism composition in either direction. The correct unchanged action is to stop, document the gap, and preserve the negative.

## Outputs produced
- Verified protocol and hash
- Fresh acquisition commands, source hashes, source manifest, licenses/source ledger
- Pinned Python environment
- Audited reconstructed counts and groups
- Deterministic review-support dossier validator plus five passing tests
- Gate evaluation and explicit universal-scoring closure
- Technical and paper-form writeups

No raw predictions, bootstrap outputs, paired comparisons, Holm results, or modeling figures exist, because creating them would require unprespecified choices. The absence is intentional and auditable, not missing reporting.

## Defensible novelty and grant readiness
**Potential novelty.** The defensible research idea is prospective cross-domain transport of a frozen validation-hazard detector. The present run does not validate that novelty empirically; it demonstrates that protocol completeness itself is a prerequisite for testing it.

**Why it matters.** A credible universal validation auditor could help biomedical ML validation leads identify evaluations that need redesign or external validation before false reassurance reaches downstream work. It must remain review support, not clinical-safety or regulatory certification.

**Significance.** Validation optimism from unit leakage, site/subject/scaffold shift, missingness, and subgroup instability can overstate biomedical model performance. A detector that transfers prospectively across unrelated data types would address a recurring review bottleneck.

**Innovation.** The proposed innovation is a frozen, model-agnostic hazard detector tested without Round 2 label-driven reweighting across clinical, wearable, and molecular transport settings. This is a method-audit contribution, not a biological discovery.

**Approach.** First archive an executable protocol bundle that fully specifies configuration IDs, hyperparameters, seeds, splits, dimension equations, controls, contrasts, and output schemas. Then rerun the same three untouched domains from the recorded source archives, freeze predictions before labels are joined to audit outputs, execute clustered 5,000-replicate inference, and evaluate all seven gates without edits.

**Risks and alternatives.** Three domains give weak domain-cluster uncertainty. molHIV has class imbalance and RDKit-invalid records. HAR observations are dense within subject. Heart sites differ sharply in prevalence and missingness. Alternatives belong in a prospectively locked amendment: add more domains, predeclare invalid-record handling, and separate detector development from external confirmation. They must not be introduced into this stopped R2.

**Milestones.** (1) Complete executable lock and independent protocol audit. (2) Clean-environment deterministic dry run on synthetic data. (3) Three-domain blinded execution. (4) Independent reproduction. (5) Only after gate passage, larger external multi-lab study.

**Compute/data resources.** The current data are public and fit commodity CPU/RAM, but the full 5,000-replicate clustered bootstrap across >=36 configurations, especially molHIV fingerprints/refits, needs a measured compute plan and possibly cached predictions rather than bootstrap refitting. The lock must specify which.

**Reproducibility.** Archive source bytes/hashes, dependency lock, configuration registry, code commit, raw unit predictions, deterministic-tolerance policy, bootstrap seeds, logs, peak memory, and a machine-readable gate report. Require independent clean-environment reproduction before claims.

**Translation boundary.** Review support only. The artifact must not certify clinical safety, regulatory conformity, diagnosis, treatment, or deployment readiness.

**Evidence for a larger grant.** A larger grant would be justified by full G1-G7 passage under an executable lock, independent reproduction, stable performance across more external domains, measured reviewer-time/defect-yield benefits, and a bounded false-reassurance rate. Current evidence is weak: R1 motivated the detector, while this R2 produced source feasibility and a protocol-completeness failure, not transport performance.

**Exact next experiment a top lab should fund.** Fund an independently audited, containerized “R2b” using the same three source snapshots but only after a signed executable specification fixes every omitted element listed above. Have one team create the complete lock without outcome access, a second team execute it blinded, and a third reproduce hashes and gate calculations. Add no domain or estimator after outcomes are inspected. If that passes, fund a new untouched 8-12-domain external study rather than calling this run successful.

## Independent adjudication note
The delivered test log records five passing pytest tests. Independent rerun in the adjudicator environment was not possible because pytest is not installed there; direct unittest discovery is inapplicable because the tests import pytest. The source tests are included and the pinned environment specifies pytest 8.4.2. Generated pytest caches and bytecode were removed from the source package, and the deliverable manifest was rebuilt and verified.
