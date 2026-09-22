# DOC-2-096 R2 locked temporal archive protocol

**Locked:** 2026-09-21 22:39 IST before archive downloads/outcomes.

Snapshots: ClinVar tab-delimited December 2020, December 2023, and current September 2026, exact URLs and hashes frozen. Unit: gene-normalized-condition edge. Each snapshot rebuilt only from its own variant and submission tables. Development normalization uses 2020 phenotype co-occurrence only; ambiguous components (more than one ID/source) unmapped. Later unknown IDs remain self/unmapped.

Duplicate assertions collapse to VariationID + base SCV + gene + condition, one submitter contribution. 2020 features: P/B/conflict/VUS counts, lab count, review status, gene and condition degree, testing burden. Outcome at 2023/current: conflict emergence among edges non-conflicting at baseline, resolution among conflicting edges, or review upgrade. Current identifiers never backfill earlier features.

Minimums: >=10,000 baseline edges, >=1,000 conflict/resolution/update events in each transition, >=200 events per source stratum. Models: raw counts, positive-only, R0 reliability. Evaluate Brier, calibration slope and top-decile enrichment prospectively 2020->2023; locked replication 2023->current. Reliability must improve Brier >=5% over raw in both transitions, slope 0.8-1.2, replicate in two sources and survive leave-top-submitter-out. Date/label permutation and ontology-label randomization must lose >=50% enrichment. If snapshot schemas cannot reconstruct comparable assertion states, stop.

Claim is evidence-triage prioritization, never clinical classification.
