# DOC-2-096 R1: Temporal Identifiability and Ontology Normalization

**Date:** 21 September 2026  
**Status:** CLEAN STOP BEFORE PREDICTIVE OUTCOMES

## Decision
R1 cannot honestly test whether early negative-evidence topology predicts later conflict resolution from the current ClinVar `submission_summary` and `variant_summary` alone. The submission file is a current snapshot of retained submissions with `DateLastEvaluated`; it does not provide the assertion state visible at a 2020 cutoff, withdrawn/superseded histories, or former review status. Using rows whose evaluation date is later as outcomes while retaining their current classifications would leak future/current state into development. No temporal model, AUROC, Brier score or calibration claim was produced.

## Completed crosswalk
A versioned crosswalk was frozen before trajectory work. It linked identifiers co-occurring inside the same ClinVar phenotype slot and allowed a canonical component only when there was at most one identifier per source. Results: 31,993 identifiers, 944 multi-source/single-source components, 54 ambiguous components, and 2,651 identifiers in unambiguous cross-source components. Ambiguous components remain unmapped. The low mapping yield is itself useful: most identifiers do not have a unique cross-source co-occurrence in the current variant table.

## Why this is not a negative prediction result
The question requires historical releases or assertion-version events. `DateLastEvaluated` is neither submission availability nor biology. A current SCV evaluated in 2018 may have been updated, withdrawn, replaced or only later incorporated into a review state. Current aggregate and review labels cannot be projected backward. Date permutation would not fix this leakage.

## Preserved protocol
The locked design specifies development through 2020, holdout 2021-2023, test >=2024, SCV-base collapse, submitter clustering, lab-dependence controls, calibration and negative controls. It should be executed unchanged against monthly/yearly archived ClinVar releases or a versioned SCV event feed.

## Next executable route
Obtain checksum-frozen ClinVar release snapshots from at least 2020, 2023 and current. Rebuild edges independently in each release, normalize conditions with a crosswalk frozen from development only, and define outcomes as actual changes between snapshots. Then compare raw counts, positive-only and R0 reliability models with condition and submitter cluster bootstrap. Without those releases, temporal transport is unidentified.

## Contribution
R1 prevents a common error: treating current assertion evaluation dates as a longitudinal dataset. It also delivers an ambiguity-aware condition crosswalk and exact hashes so future snapshots can use a stable normalization policy.
