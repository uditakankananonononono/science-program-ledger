# SP-006 (DOC-2-069) R1 - Hard Cohort Checkpoint Report

**Verdict: STOP before modeling.** G3 mapping-coverage gate fails as locked; G7 preconditions unmet. A clean cohort stop beats a leaky model. Bounded product delivered; no ranking claims made. R1 protocol sha256 10f39df946c45c23e713f33702c05141cf4871e1d71cf797fb6c9147a91392c6 (locked before extraction).

## Gate outcomes
| Gate | Result | Key numbers |
|---|---|---|
| G1 extraction integrity | PASS | 14/14 tables, CRC32 + double-sha256, 0 failures |
| G2 cohort | PASS | 123,697 NCTs (band 50k-250k), 0 duplicate NCTs, 94 quarantined rows documented |
| G3 mapping coverage | **FAIL** | MeSH browse 84.33% (<85%); drug names 35.58% (<60%) |
| G4 reason audit | PARTIAL | kappa 0.655 PASS overall; safety 0.33 / regulatory 0.30 -> abstained (locked rule) |
| G5 freeze | PASS | 14-entry sha256 manifest frozen before validation access |
| G6/G7 | not reached | model not run |

## Cohort (frozen, 2024-06-01 snapshot)
123,697 interventional drug studies: Completed 100,812 (32,769 with results posted as of cutoff; 68,043 completed-no-results - never read as efficacy failure), Terminated 15,880, Withdrawn 6,399, Suspended 606. Competing-risk labels (reliability-filtered): terminated-enrollment 5,398; terminated-unclear 2,755; terminated-missing 2,193; terminated-business 2,154; terminated-abstained 1,949 (safety+regulatory classes failed audit); terminated-efficacy-or-futility 1,387; terminated-operational 650.

## Why G3 failed - and the recalibration evidence
**MeSH leg (84.33% vs 85%):** investigator free-text conditions cover 100% of cohort; combined MeSH-or-freetext = 100%. The 15.7% MeSH-browse gap is NLM curation lag on newer studies, not missing conditions.

**Drug-name leg (35.58% vs 60%):** the registry's 92,779 distinct intervention "names" are dominated by ~73k single-trial spellings (dose-regimen variants, manufacturer qualifiers, procedures mislabeled as Drug, trial-specific codes absent from ChEMBL). Exact+normalized mapping (case/salt/dose/route/combo-component aware; no fuzzy matching, per lock) against 16,784 clinical-phase ChEMBL_37 molecules covers:
- names in >=2 trials: 60.8% mapped (83.4% trial-weighted)
- >=5 trials: 82.0% (91.8% weighted)
- >=10 trials: 89.4% (94.6% weighted)
- >=100 trials: 98.8% (98.9% weighted)
Mechanism coverage of the evidence mass is strong; the all-distinct-names threshold is unreachable without fuzzy matching (locked out).

**Cutoff-safety note (documented deviation):** ChEMBL_34 (pre-cutoff release) was unreachable - ftp.ebi.ac.uk TLS failures on all protocols/retries from this environment. ChEMBL_37 (API, release 2026-05-01) was used for name mapping and mechanism joins; mechanism-reference records carry PubMed PMIDs for as-of-cutoff reconstruction. This deviation is why clusters were NOT finalized this round.

## G4 audit detail
n=240 stratified double-coded (two independently written deterministic coders; seed 20260601 recorded). Overall kappa 0.655. safety: 10/30 agree, 18 v2-abstentions, 2 cross to efficacy. regulatory-hold: 9/30 agree, 19 v2-abstentions. Disagreement is coder-strictness driven, not class inversion. Per locked rule both classes abstained; five classes (+missing/unclear) carry labels.

## Bounded product
frozen cohort + 11-class competing-risk labels + audit + as-of-cutoff NCT histories (39,877 with results posted; 84 retraction-linked; 2,181 with pending events) + ChEMBL name mapping (33,012 names) + per-phase base rates + freeze manifest. Validation snapshot (2026-06-01) remains unopened.

## Options for the orchestrator (R2 amendment, requires new locked protocol before recomputation)
1. MeSH threshold: combined MeSH-browse-OR-freetext coverage (100%) or MeSH-only ~84%.
2. Drug-name threshold: frequency-weighted (>=60% of names in >=2 trials - achieved 60.8%) or trial-weighted >=55% (achieved 57.7%).
3. Safety/regulatory classes: add a third adjudicating coder or stronger anchors before un-abstaining.
4. ChEMBL cutoff-safety: pre-cutoff release via an alternate mirror, or keep the PMID-dated mechanism-ref reconstruction rule.
