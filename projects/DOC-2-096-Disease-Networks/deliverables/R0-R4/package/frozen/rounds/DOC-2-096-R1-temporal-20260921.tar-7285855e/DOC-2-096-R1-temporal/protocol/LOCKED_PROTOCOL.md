# DOC-2-096 R1 locked protocol

**Title:** Temporal Transport of Negative-Evidence Topology with Normalized ClinVar Conditions
**Locked:** 2026-09-21 22:32 IST before R1 submission outcomes

## Time semantics
`DateLastEvaluated` is an assertion evaluation date, not a biological event or submission date. The current `submission_summary` is a snapshot and cannot prove historical state deletion or resolution. R1 reconstructs cumulative *currently retained assertions* by evaluation year and explicitly audits whether this is adequate for temporal prediction. If withdrawn/superseded histories are unavailable, claims are limited to retrospective evaluation-date transport, not conflict resolution over calendar time.

## Condition normalization
Build a versioned crosswalk from current ClinVar variant rows: identifiers co-occurring within the same RCV phenotype slot link MedGen, MONDO, OMIM and Orphanet IDs. Use connected components only when a component contains at most one ID from each source; multi-ID components are ambiguous and retained unmapped. Submission `ReportedPhenotypeInfo` C identifiers map through MedGen. Report mapped, unmapped and ambiguous rates. Freeze crosswalk SHA-256 before trajectory outcomes.

## Assertion collapse and dependence
Unit is unique SCV version collapsed to base SCV accession; duplicate rows collapse by VariationID, base SCV, normalized condition and gene, preferring latest evaluation date. Submitter dependence is controlled by lab-level cluster counts and leave-top-submitter-out. Missing submitted gene uses variant-summary VariationID-to-gene linkage only when unique.

## Temporal design
Development: evaluation date <=2020-12-31. Holdout: 2021-01-01 through 2023-12-31. Future test: >=2024-01-01. For gene-condition edges present with >=2 assertions at development cutoff, compare raw counts, positive-only features and R0 reliability features for predicting later current-snapshot conflict presence and review-status upgrade. Never random split. Baseline is edge degree + assertion count.

## Metrics
Brier score, calibration slope/intercept, AUROC for ranking only, top-decile enrichment and decision-curve-like precision. Bootstrap clusters by condition and submitter. Gate requires >=10,000 development edges, >=1,000 future conflict/update events, reliability model improving Brier by >=5% versus raw counts in both holdout and future test, calibration slope 0.8-1.2, direction preserved across two identifier-source strata and leave-top-submitter-out, and both negative controls (date permutation within condition; ontology-label randomization) losing >=50% of enrichment.

If the current snapshot cannot reconstruct historical state or review upgrades without leakage, R1 stops as a temporal-identifiability failure and delivers the crosswalk/audit rather than a predictive claim.
