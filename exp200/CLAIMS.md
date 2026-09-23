# exp200 Claims & Useful-Results Tracker

Lane split approved by main 2026-09-23 ~21:47 IST: EXP-1 DOC-1-001..050, EXP-2 DOC-1-051..100,
EXP-3 DOC-2-001..050, EXP-4 DOC-2-051..100. Skip set (already touched by prior SP work,
orchestration/topic-ledger.csv): 13 unique topics. All 200 topics get performed;
100 useful results is the floor, not the finish line.
## Cumulative useful results (lead-lane tracker)
- Baseline from prior program (orchestration/useful-results-ledger.csv): **34**
- New from exp200 lanes: 5 (EXP-1: 1, EXP-2: 0, EXP-3: 0, EXP-4: 4)
- **Total: 39 / 100 minimum**
## Claims (first-come; claim BEFORE starting a topic)
| topic | lane | claimed_utc | status | outcome |
|---|---|---|---|---|
| DOC-1-001 | EXP-1 | 2026-09-23 16:20 | done | USEFUL: G1 PASS 21.1% median RMSE reduction, 30/30 perm-sig; G2 neg; pivot P1/P2 PASS |
| DOC-1-002 | EXP-1 | 2026-09-23 17:10 | running | v1-v3 boundary documented (CROP-seq under-powered, NOT counted); v4 Adamson2016 direction locked, running |
| DOC-2-079 | EXP-4 | 2026-09-23 16:20 | closed | documented boundary, NOT counted - downgraded 2026-09-23 22:11 IST: user judged the retrospective-prediction framing non-research; line terminated (forward addendum left in place as documented work, not extended) - exp200/179 |
| DOC-2-090 | EXP-4 | 2026-09-23 16:22 | done | pass (useful) - exp200/190 |
| DOC-2-099 | EXP-4 | 2026-09-23 16:24 | done | primary + 2 pivots fail; documented boundary (not counted) - exp200/199 |
| DOC-2-080 | EXP-4 | 2026-09-23 16:35 | done | pass (useful) - exp200/180 |
| DOC-2-075 | EXP-4 | 2026-09-23 16:38 | done | pass on locked gates, fragile (LOFO OR 2.6-4.2) - exp200/175 |
| DOC-2-062 | EXP-4 | 2026-09-23 17:18 | done | primary pass (AUROC 0.775 low-seq stratum, +0.076 over sequence); forward validation enrichment pass / absolute-rate fail (5.3% vs 0%) - exp200/162 |
| DOC-2-051..059, 061..068, 070..073, 081..089, 091..095, 097, 100 | EXP-4 | 2026-09-23 16:25 | queued | - |
| DOC-2-089 | EXP-4 | 2026-09-23 16:40 | done | primary fail (convergence gate); pivot 1 pass 4/5 (lineage lock), low novelty flagged - exp200/189 |
| DOC-2-073 | EXP-4 | 2026-09-23 16:52 | closed | primary + pivot fail; documented boundary (not counted) - null: AlphaMissense equally reliable on poorly vs well-studied rare-disease genes - exp200/173 |
| DOC-2-064 | EXP-4 | 2026-09-23 17:05 | note | checked vs sp-041: sp-041 is DOC-1-044 (DANN cross-study synergy, INVALID), not DOC-2-064 - 064 stays in lane 4 queue |
| DOC-2-068 | EXP-4 | 2026-09-23 17:12 | closed | primary + pivot fail on precision gate; documented boundary (not counted) - no-shared-target pathway fingerprint 13-14% vs 62% target identity - exp200/168 |
| DOC-2-051..059, 061..068, 070..072, 081..088, 091..095, 097, 100 | EXP-4 | 2026-09-23 16:25 | queued | - |
- Lane 3: DOC-2-001..DOC-2-050 (skipping touched DOC-2-009, 019, 032, 033, 037), folders exp200/1NN-<slug> where NN = DOC-2 number. Claimed 2026-09-23 21:55 IST.
- Lane 4 folder numbering: exp200/1NN-<slug> for DOC-2-0NN (same as lane 3).
## User steering 2026-09-23 ~22:10 IST (all lanes, from main)
Meta-science framing does NOT count as research: a topic must produce a biological or
methodological payload (tool, nomination list, measured property of real data). If a
topic's only honest output is meta, run it as a documented boundary (template: 199/099)
and do NOT count it. 179 downgraded to boundary on direct user instruction (EXP-4 count 3).
