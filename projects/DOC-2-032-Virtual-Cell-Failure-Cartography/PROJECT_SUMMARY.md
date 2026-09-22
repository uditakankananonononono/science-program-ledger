# DOC-2-032 - Virtual Cell Failure Cartography

## R0 verdict
Locked source-feasibility negative. The selected Adamson/scPerturb sample had enough perturbations and genes but only six control cells versus the frozen minimum of 200, so the outcome study stopped at F0.

## Useful result
The experiment exposed a source/sample mismatch before a three-control-per-half analysis could be promoted as evidence. The new metric-mirage estimand remains valuable: high absolute-expression correlation can coexist with failed perturbation-response sign recovery. R0 does not estimate its prevalence.

## What is new and why it matters
Rather than another average virtual-cell benchmark, this project defines explicit failure regimes and makes control-cell support a hard estimability condition. That is a grant-relevant design contribution because absolute-expression metrics can hide no-response predictors.

## Application
R0 supplies a metadata/source gate and a preregistered failure-taxonomy template. A future tool could issue model cards with metric-mirage, collapse and directional-failure rates, but no such tool graduates from this source-stop round.

## Top-lab/grant next question
Run metadata-only reconnaissance on a larger open perturbation cohort, then separately lock a study with no-response, additive and modern virtual-cell models, independent replication and pathway-level follow-up. The key funded question is whether failure taxonomy predicts when model-guided experimental prioritization is unsafe.

## Integrity notes
- The protocol file metadata precedes execution, but its human-readable lock timestamp says 13:02 IST while the returned archive/report was assembled around 13:01. Treat that clock string as inconsistent documentation; the worker and archive ordering indicate the protocol existed before the run, but future locks need machine timestamps and hashes.
- Downstream rows computed after F0 are diagnostics only and cannot count as outcome evidence.
- The raw H5AD is not included; its SHA-256 is recorded.

## Claim boundary
This counts only as a useful source-feasibility result. It does not validate metric-mirage prevalence, a virtual-cell model, or a deployable failure detector.
