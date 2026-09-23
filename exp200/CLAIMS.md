# exp200 Claims & Useful-Results Tracker

Lane split approved by main 2026-09-23 ~21:47 IST: EXP-1 DOC-1-001..050, EXP-2 DOC-1-051..100,
EXP-3 DOC-2-001..050, EXP-4 DOC-2-051..100. Skip set (already touched by prior SP work,
orchestration/topic-ledger.csv): 13 unique topics. All 200 topics get performed;
100 useful results is the floor, not the finish line.
## Cumulative useful results (lead-lane tracker)
- Baseline from prior program (orchestration/useful-results-ledger.csv): **34**
- New from exp200 lanes: 10 (EXP-1: 4, EXP-2: 0, EXP-3: 0, EXP-4: 6)
- **Total: 43 / 100 minimum**
- **Total: 42 / 100 minimum**
## Claims (first-come; claim BEFORE starting a topic)
| topic | lane | claimed_utc | status | outcome |
|---|---|---|---|---|
| DOC-1-001 | EXP-1 | 2026-09-23 16:20 | done | USEFUL: G1 PASS 21.1% median RMSE reduction, 30/30 perm-sig; G2 neg; pivot P1/P2 PASS |
| DOC-1-002 | EXP-1 | 2026-09-23 17:10 | done | DOCUMENTED BOUNDARY (not counted): 3 datasets, 5 gate versions, 0 targets pass size-matched QC; flagged for Replogle-scale retry |
| DOC-1-003 | EXP-1 | 2026-09-23 17:36 | done | USEFUL (counted, main adjudication 23:19): technical floor of Visium spatial structure, held-out r=0.716 + audit CLI; G2+v2 LR boundary, not counted |
| DOC-1-004 | EXP-1 | 2026-09-23 17:48 | done | G1 genus 7.5% vs 10% gate FAIL but 20/30 perm-sig (urobilin R2 0.57); v2 species WORSE (-6.5%) - COUNTED (main adjudication 23:34): predictability ceiling map + aggregation-beats-resolution rule + twin CLI |
| DOC-1-005 | EXP-1 | 2026-09-23 18:03 | DONE - COUNTED (main adjudication 00:09): trained MLP fate forecaster 86.4% top-1 held-out (7.9x climatology); Markov wins NLL head-to-head; CLI + artifacts | - |
| DOC-1-006 | EXP-1 | 2026-09-24 00:21 | DONE - DOCUMENTED BOUNDARY (adjudication requested) | CAR-T response classifier: G1 fails both arms (logreg CV 0.552 p=0.42; MLP 0.530 p=0.70, 200 full-pipeline nulls, n=22); external untouched; streaming aggregator shipped; docking re-angle proposed |
| PPD-v2 | EXP-1 | 2026-09-24 00:21 | claimed (queued after DOC-1-006) | USER-STEERED new direction (main 00:20, user verbatim "Try new directions, more biomarkers"): methylation-first (TTC9B/HP1BP3 Osborne/Payne literature), then multi-cohort joint training w/ leave-one-cohort-out, then proteomics/metabolomics scan. NOT re-fishing failed RNA-seq panels. Gates locked before results; frozen external verification mandatory |
- **USER-STEERED INSERT (main 23:57, user verbatim): postpartum-depression biomarkers** - EXP-1, claimed 2026-09-24 ~00:02 IST. Blood-transcriptome cohorts (GEO or equiv), trained classifier, FROZEN external-cohort verification (AUROC gate + single-feature baseline gate, honest-negative clause), validated biomarker panel + scoring tool. CLOSED 2026-09-24 00:19 IST: DOCUMENTED BOUNDARY - 5 locked gate versions; external-cohort transport FAILED (AUROC 0.429, below chance, CI 0.273-0.591); CV-optimism (0.705->0.429) and permutation-null (0.718) findings quantified; tools shipped labeled failed-verification. exp200/PPD-postpartum-depression-biomarkers/
| DOC-2-079 | EXP-4 | 2026-09-23 16:20 | closed | documented boundary, NOT counted - downgraded 2026-09-23 22:11 IST: user judged the retrospective-prediction framing non-research; line terminated (forward addendum left in place as documented work, not extended) - exp200/179 |
| DOC-2-090 | EXP-4 | 2026-09-23 16:22 | done | pass (useful) - exp200/190 |
| DOC-2-099 | EXP-4 | 2026-09-23 16:24 | done | primary + 2 pivots fail; documented boundary (not counted) - exp200/199 |
| DOC-2-080 | EXP-4 | 2026-09-23 16:35 | done | pass (useful) - exp200/180 |
| DOC-2-075 | EXP-4 | 2026-09-23 16:38 | done | pass on locked gates, fragile (LOFO OR 2.6-4.2) - exp200/175 |
| DOC-2-062 | EXP-4 | 2026-09-23 17:18 | done | primary pass (AUROC 0.775 low-seq stratum, +0.076 over sequence); forward validation enrichment pass / absolute-rate fail (5.3% vs 0%) - exp200/162 |
| DOC-2-089 | EXP-4 | 2026-09-23 16:40 | done | primary fail (convergence gate); pivot 1 pass 4/5 (lineage lock), low novelty flagged - exp200/189 |
| DOC-2-073 | EXP-4 | 2026-09-23 16:52 | closed | primary + pivot fail; documented boundary (not counted) - null: AlphaMissense equally reliable on poorly vs well-studied rare-disease genes - exp200/173 |
| DOC-2-064 | EXP-4 | 2026-09-23 17:05 | note | checked vs sp-041: sp-041 is DOC-1-044 (DANN cross-study synergy, INVALID), not DOC-2-064 - 064 stays in lane 4 queue |
| DOC-2-068 | EXP-4 | 2026-09-23 17:12 | closed | primary + pivot fail on precision gate; documented boundary (not counted) - no-shared-target pathway fingerprint 13-14% vs 62% target identity - exp200/168 |
| DOC-2-056 | EXP-4 | 2026-09-23 17:45 | closed | primary + 2 pivots fail (incl. trained cross-platform biomarker: external AUROC 0.78/0.80 but 1-gene SLC6A14 baseline >= model); documented boundary (not counted) - exp200/156 |
| DOC-2-071 | EXP-4 | 2026-09-24 00:05 | pass (pivot) | primary CNN fail; ESM-2 + trained head finds catalytic residues: frozen M-CSA external AUPRC 0.205 vs 0.045 (Bartlett propensity) / 0.036 (ESM wt-marginal), median AUROC 0.90; nomination ABHD4 S146/H320/D170 - exp200/171 |
| DOC-2-054 | EXP-4 | 2026-09-24 00:45 | claimed | trained blood-RNA bacterial-vs-viral classifier; frozen external GSE42026/GSE40396; vs Herberg 2016 + Sweeney 2016 - exp200/154 |
| DOC-2-051..053, 055, 057..059, 061, 063..067, 070, 072, 081..088, 091..095, 097, 100 | EXP-4 | 2026-09-23 16:25 | queued | - |
- Lane 3: DOC-2-001..DOC-2-050 (skipping touched DOC-2-009, 019, 032, 033, 037), folders exp200/1NN-<slug> where NN = DOC-2 number. Claimed 2026-09-23 21:55 IST.
- Lane 4 folder numbering: exp200/1NN-<slug> for DOC-2-0NN (same as lane 3).
## User steering 2026-09-23 ~22:10 IST (all lanes, from main)
Meta-science framing does NOT count as research: a topic must produce a biological or
methodological payload (tool, nomination list, measured property of real data). If a
topic's only honest output is meta, run it as a documented boundary (template: 199/099)
and do NOT count it. 179 downgraded to boundary on direct user instruction (EXP-4 count 3).
