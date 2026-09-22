# SP-006 (DOC-2-069, Drug Failure as Information) - Round 0: Open-Data Feasibility + Grounding

**Verdict: GO.** Locked-gate OVERALL PASS 7/7. Protocol sha256 a53546da17fdebc37a6d0aed829a2040b155808f3766d5275b9d401aace87bf8 (locked before any outcome inspection). Product scope: review priority for a translational pharmacology team's manual repurposing review - never treatment advice.

## What R0 established

**1. Versioned trial data is accessible and cut off cleanly (G1, G2).**
ClinicalTrials.gov API v2 is live for schema probing and status counts, with AREA[LastUpdatePostDate] and AREA[CompletionDate] RANGE filters for cutoff-anchored harvests. AACT monthly snapshots are downloadable without auth: the 2024-06-01 export (1,829,799,788 bytes, 47 tables) and the 2025-12-01 / 2026-06-01 / 2026-09-01 validation candidates all probe-verified (HTTP 206). Snapshot availability is patchy per month, so the design anchors only to probe-verified dates. Selective in-zip extraction works: retractions (662 rows), pending_results (27,966), documents (10,501) were pulled from inside the 1.83GB remote zip via HTTP range requests + central-directory parsing - R1 never needs a full 1.8GB download to reach any single table.

**2. The cutoff snapshot does not leak the future (stop condition check).**
Date audit over 38,629 extracted rows: pending_results max event_date 2024-05-30 (0 violations); retractions "2031" hits are a page number in a 2012 citation; documents "2025/2026" hits are primary-key IDs. Zero real post-cutoff content. API responses carry a versionHolder stamp (2026-09-21), so API data is reserved for schema/probing only - never as-of-cutoff facts.

**3. Failure modes are distinguishable at scale (G3).**
Live status taxonomy (drug interventional studies): COMPLETED 120,384; TERMINATED 18,904; WITHDRAWN 7,536; SUSPENDED 641; UNKNOWN 26,805; plus 7 rarer values. whyStopped free text is filled in 93/100 of a TERMINATED sample, with visibly heterogeneous reasons (enrollment, sponsor decision, FDA hold, administrative) - confirming that termination != efficacy failure and that a frozen reason taxonomy with an abstain class is required. Withdrawn (7,536) and UNKNOWN (26,805) cohorts are large enough to matter as competing-risk classes; missing results are a posting state, never evidence of efficacy failure.

**4. All data sources are legally reusable, with two exclusions (G4).**
Quoted live on 2026-09-22: ClinicalTrials.gov + MeSH - US government works, public domain (NLM web policies); UniProt - CC BY 4.0 (FTP LICENSE); ChEBI - CC BY 4.0; ChEMBL - CC BY-SA 3.0 (ShareAlike: any redistributed derived database must carry CC BY-SA 3.0 + attribution - written into the commercial workflow below); MONDO - CC-BY 4.0. Excluded: DrugCentral (license text not verifiable from its JS-gated pages at grounding time) and DrugBank (proprietary).

**5. Publication and retraction linkage exists as-of-cutoff (G5).**
API records carry referencesModule with DERIVED PMIDs; the snapshot carries study_references, retractions (PMID + NCT pairs), pending_results (release events with dates), and documents (protocol/CSR links) - all as of 2024-06-01, so post-cutoff linkage accrual cannot leak in.

**6. The full design is frozen before outcomes (G6).** Historical cutoff (2024-06-01 snapshot), typed temporal outcomes, independent unit (NCT record; mechanism cluster = intervention-target x condition, cluster-preserving splits), competing risks (six typed classes, never a binary failure), missing-reason policy (reason-missing is a class, never imputed; missing results never efficacy evidence; UNKNOWN tracked as stale), frozen reason taxonomy (8 classes incl. unclear->abstain), baselines (literature priors + snapshot base rates + frozen logistic), mechanistic-contradiction features from open sources, calibration/ranking gates (Brier/ECE, PR-AUC, lift@k vs baselines), controls (withdrawn-before-enrollment negatives; post-cutoff-success positives; label-noise audit), abstention as first-class output, and the three-armed stop condition.

## G7 operational plan

**Commercial workflow.** Input: periodic mechanism-review queue for the pharmacology team. Pipeline: snapshot-pinned extract -> mechanism clustering -> frozen reason classification (rules + abstain) -> calibrated ranking vs baselines -> review queue with per-mechanism evidence cards (typed status history, reason class, contradiction features, retraction/publication links, abstention flags). Licensing posture: CT.gov/MeSH/UniProt/ChEBI/MONDO outputs are attribution-only; any redistributed ChEMBL-derived mapping carries CC BY-SA 3.0 - the product ships per-customer derived tables with that license attached, or uses UniProt-only mappings where ShareAlike is commercially awkward. No DrugBank/DrugCentral dependencies.

**Safety/regulatory.** Output is a research-review priority list with evidence cards, explicitly labeled "not treatment advice, not a clinical decision"; no patient data exists anywhere in the pipeline (registry metadata only); abstention and reason-missing classes are always shown, never silently dropped; retraction-linked evidence is visually flagged. Human review is the endpoint of every queue - the system never auto-advances a mechanism.

**Provenance.** Every artifact sha256-ledgered; snapshot dates and zip byte-counts recorded; API calls carry versionHolder stamps; license ledger with quoted text and access dates; protocol + lock hashes in every delivery.

**Monitoring.** Monthly: re-probe cutoff/validation snapshot availability (patchy availability observed); AACT schema drift check via central-directory diff (47-table list hashed); API taxonomy drift (status enum + fill-rate re-sample); license-page change watch for ChEMBL/UniProt/ChEBI/MONDO. Any drift -> freeze pipeline, alert, do not silently adapt.

**Rollback.** Every round is snapshot-pinned and protocol-locked; a bad R1 can be abandoned by reverting to the R0 verdict with zero data mutation (all inputs read-only remote). Reason-taxonomy versions are immutable; a taxonomy revision creates a new version, never edits history.

**Measured cost (observed this round).** Cutoff snapshot: 1.83GB remote, 0 bytes downloaded for verification (range-request verification pattern; three demo tables totaled 2.4MB). API probing: ~25 calls. Full studies.txt-scale extraction is a one-time ~1.8GB pull per snapshot (bandwidth only); two snapshots (cutoff + validation) budget ~3.7GB. No paid resources anywhere in the design.

## Known limitations (preserved)
- Monthly granularity: intra-month status changes are invisible; cutoff/validation events are bounded to snapshot dates.
- whyStopped is free text: the frozen taxonomy will misclassify some reasons; mitigated by the audit sample + abstain class, reported as label noise.
- 7% of terminated studies lack whyStopped; they stay "reason-missing", never imputed.
- Per-study fine-grained version history (CT.gov history tab) was not programmatically accessible from this environment (403/404 on probed endpoints); monthly snapshots are the versioned source.
- DrugCentral excluded pending license verification; if verified later, it is additive, not required.
