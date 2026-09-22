# SP-006 (DOC-2-069) R2 - Mapping/Reliability Refinement: Gate Evaluation

**Verdict: STOP (route_fail arm of the R2 lock).** Predictive mechanism work halts; bounded cohort retained. No clusters built, validation snapshot unopened, no model run, no ranking claims. R2 protocol sha256 02b1432db5a87ea1fc4f6cfbcec2a7b2811633254738e492643b45bba979d789 (locked before recomputation).

## Gate outcomes
| Gate | Result | Key facts |
|---|---|---|
| G1 cutoff safety | PASS (Route B) | Route A: ftp.ebi.ac.uk TLS-blocked on all clients/transports; no official ChEMBL_34 mirror exists (verified). Route B: 5,676 mechanism-ref PMIDs resolved; 4,815/7,561 mechanism records retained (>=1 PubMed ref pubdate <= 2024-05); + first_approval <= 2023 -> 6,287 cutoff-evidenced molecules |
| G2 drug-map coverage (frozen metrics) | **FAIL** | as locked (all names in >=2 trials, n=17,781): names 49.51% (<60), trial-weighted 66.64% (<80). Full ChEMBL_37 diagnostic (never cutoff facts): 59.02% / 70.51% - also fails |
| G3 conditions | PASS | normalizer + 31,246-term vocab frozen (sha256 309e2a702c27dd6b); MeSH-only 84.33% reported separately |
| G4-G7 | not reached | no clusters, no freeze, no validation, no model |

## Why G2 fails (gap decomposition, all preserved in results/g2_gap_diagnostic.json)
- 1,691 pool names lost purely to the cutoff-evidence restriction (laquinimod, anlotinib, ALT-803, etc. - ChEMBL mechanism records carry only post-cutoff or undated refs).
- 7,286 pool names absent from even the full ChEMBL_37 clinical-molecule dictionary: formulations, dose-regimen spellings, combo strings, non-drug entries mislabeled Drug, trial-local codes.
- Sensitivity (nondrug-excluded pool, n=17,274): cutoff-safe 50.97% / 78.82%; still fails both legs.
- Per-phase floors pass (72-83% names, 97-98% trial-weighted per Phase 1-4): coverage is strong where trial mass concentrates; the gate fails on the long tail and on trial-weighted coverage under the locked pool.

## What is preserved for any future round
R1 frozen cohort (123,697 NCTs) + reliability-filtered labels; cutoff-safe mechanism reconstruction (4,815 records / 6,287 molecules, rule + evidence logged); frozen condition vocabulary + disease strata; G2 diagnostics. Validation snapshot 2026-06-01 was never opened.

## Honest paths the orchestrator could consider for R3 (new lock required)
1. Expand cutoff-safe evidence: resolve DailyMed/FDA-label refs in mechanism records to label dates (NLM public), likely recovering a large share of the 1,691 evidence-lost molecules.
2. Add PubChem (NIH, public domain) synonym expansion with cutoff-era literature dating - heavy, uncertain.
3. Revise the coverage metric itself (e.g., trial-mass-weighted primary at >=75%, or names-in->=5-trials) with the R1/R2 diagnostics as justification.
