# SP-006: DOC-2-069 Drug Failure as Information - R0 Feasibility + Grounding

Verdict: GO. Locked-gate 7/7 PASS (protocol sha256 a53546da17fdebc37a6d0aed829a2040b155808f3766d5275b9d401aace87bf8).

- protocol/protocol.json + lock.json - all frozen design elements (cutoff 2024-06-01 AACT snapshot, typed temporal outcomes, mechanism-cluster unit, competing risks, missing-reason policy, baselines, controls, abstention, stop condition)
- report/report.md - findings + commercial/safety/provenance/monitoring/rollback/cost plan
- results/ - gate_evaluation_r0.json, leakage_audit.json (38,629 rows audited, 0 violations)
- data/raw/ctgov/ - status_probe_1.json, aact_selective_extract.json, demo tables (retractions/pending_results/documents), pubmed_grounding_r0.json (24 PMIDs)
- data/raw/licenses/ - fetched license pages + UniProt FTP LICENSE
