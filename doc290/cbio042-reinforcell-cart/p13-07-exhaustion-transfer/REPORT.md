# P13-07 Exhaustion Transfer Stress Test - Build Report

**Built:** 2026-09-24 | **Status:** BOUNDARY RESULT - single-cohort exhaustion models do NOT transport (G2 fail by a hair: worst 0.643 < 0.65), and the failure is NOT explained by platform, tissue, disease or label definition (G3 fail, R^2 = 0.015). Pre-specified step 5 (pooled core signature) DOES clear the G2 bar under leave-one-cohort-out (median 0.863, worst 0.726).

Parent: CBIO042 ReinforCell. Real data: CELLxGENE Census 2025-11-08, CD8 alpha-beta T cells, primary cells only, 2,000 cells per cohort (seed 0), raw counts pulled from the source h5ad files.
Protocol and gates were locked and pushed before any result (commit f610643e, `PROTOCOL.md`).

## Gates (locked before evaluation, evaluated once)

| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | matrix over >= 8 cohorts with CIs | 9 cohorts, 612 train/test AUCs, each with 200-resample bootstrap CI | PASS |
| G2 | portable iff median cross AUC >= 0.75 AND worst >= 0.65 (logistic, L1) | median 0.768, worst 0.643 | FAIL -> certified non-transport for single-cohort models |
| G3 | named factors explain >= 60% of transport deficit | R^2 = 0.015 (logistic), 0.025 (boosting) | FAIL |
| G4 | non-transport with a named dominant factor | non-transport certified, but no named factor dominates | NOT MET as written - see finding |

## Cohorts actually analysed (disclosed deviation)
C01 RCC kidney 10x5', C02 LUAD lung 10x3'v2, C03 LUAD lung BD Rhapsody, C04 LUAD lung Smart-seq2, C05 LUSC lung 10x3'v2, C06 colon adenocarcinoma 10x3'v2, C08 breast IDC 10x5'v1, C09 oropharynx SCC 10x3'v3, C10 B-NHL lymph node 10x multiome.
Dropped before analysis (fetch, not results): C07 (independent LUAD study, 21.9 GB file - metadata read never finished inside the 2 GB sandbox) and C11 (COVID blood, 14 GB file - rows only partly fetched). Consequence: no infection arm; disease-class contrast is carcinoma vs lymphoma only. Cell cap was lowered 4000 -> 2000 before any expression data was read (sandbox memory).

## Results
| cohort | L1-vs-L2 kappa | pooled LOCO AUC (L1) |
|---|---|---|
| C01 | 0.71 | 0.900 |
| C02 | 0.24 | 0.771 |
| C03 | 0.54 | 0.796 |
| C04 | 0.57 | 0.859 |
| C05 | 0.48 | 0.726 |
| C06 | 0.59 | 0.866 |
| C08 | 0.80 | 0.958 |
| C09 | 0.80 | 0.929 |
| C10 | 0.47 | 0.863 |

| model / label | median in-cohort | median cross | worst cross | best cross |
|---|---|---|---|---|
| lr_L1 | 0.818 | 0.768 | 0.643 | 0.947 |
| lr_L2 | 0.976 | 0.773 | 0.497 | 0.940 |
| hgb_L1 | 0.862 | 0.776 | 0.617 | 0.945 |
| hgb_L2 | 0.975 | 0.748 | 0.465 | 0.926 |

Shapley shares of R^2 (logistic): platform 0.0004, tissue 0.0061, disease class 0.0079, label definition 0.0004

Core genes (selected in all 9 LOCO folds, 68): ACP5, ADGRG1, AKAP5, ALOX5AP, ANXA1, APOBEC3C, ARID5B, C1orf162, CARS1, CBLB, CCL3, CD200R1, CD27, CD38, CD7, CD74, CD82, CD84, CHN1, CSF1, CXCR6, DTHD1, DUSP4, ETV1, FABP5, FAM3C, FASLG, GALNT2, GAPDH, GFOD1, GOLIM4, GZMA, GZMB, HLA-DRB1, HNRNPLL, ICOS, IFI6, IL7R, ITM2A, JAML, LYST, MAF, MX1, MYO7A, NDFIP2, PAG1, PHLDA1, PKM, PLAC8, PRF1, PTMS, RBPJ, RGS1, RGS2, RPL41, RPS27, SAMSN1, SIRPG, SLA, SMC4, SNX9, TBC1D4, TNFRSF9, TNFSF4, TOX2, TTN, TYMP, VCAM1

## Findings

1. **Label instability comes first.** The two exhaustion definitions (gene-set score tertiles vs Leiden-cluster tertiles) agree only moderately: kappa 0.24 (C02) to 0.80 (C08). "Exhausted" is not one stable call even inside a single cohort.
2. **Single-cohort models don't transport.** A model trained on one cohort loses 0.13 AUC on average on another cohort across all label pairings (0.15 for boosting). Same-label pairs alone lose about 0.06. The median cross-cohort AUC is fine (~0.77), but the worst pairs fall to 0.64 (L1) and 0.50 (L2).
3. **The headline, and the reason G3 fails:** the loss is idiosyncratic to the cohort pair. Platform (10x 3'/5', BD, Smart-seq2, multiome), tissue, disease class and label definition *together* explain 1.5% of its variance. Same-dataset LUAD pairs across three platforms (C02/C03/C04) lose 0.051 AUC on average, versus 0.062 for all other pairs (logistic, L1 to L1). Cutting platform, tissue and study differences together barely helps. The drivers are unmeasured cohort-level factors: donor mix, dissociation, and each study's annotation of "CD8 T cell". The practical implication for ReinforCell-style engines is that you can't fix transport by matching platform or tissue. You have to train across cohorts.
4. **Pooling fixes it (spec step 5).** An L1-sparse logistic model trained on 8 pooled cohorts and tested on the held-out 9th reaches median AUC 0.863 and worst 0.726 (C05 LUSC). That clears the locked G2 thresholds. 68 genes are selected in all 9 folds, including GZMB, PRF1, TNFRSF9, CXCR6, RGS1, DUSP4, CD38, ICOS, TOX2, IL7R (negative) and VCAM1.

## Honest limits
- The label is defined from 9 canonical exhaustion genes. Those genes are excluded from the features, so "portable" means the co-expression program around exhaustion transports. It doesn't mean a functional readout transports.
- `results/core_signature_check.txt` scores the 68-gene intersection on all cohorts (median 0.862, worst 0.709). That is optimistic because the genes were chosen using every fold. The LOCO numbers above are the honest ones.
- There is no CAR-T infusion-product cohort in Census at usable size, and no chronic-infection arm. The spec's product/infection transport questions remain open.
- 2,000 cells per cohort; one seed.

## Artifacts
- `PROTOCOL.md`: locked gates.
- `tool/`: `select_cells.py` (Census selection), `remote_fetch.py` (resumable S3 row fetch), `offsets.py`, `prep.py` (labels and kappa), `transport.py` (N x N matrix), `evaluate.py` (gates, decomposition, core signature) and `transport_check.py`. The last one is the auditor: it scores any gene signature against all cohorts under the G2 rule.
- `results/`: `results.json` (gates, decomposition, LOCO), `transport_matrix.json` (all 612 AUCs with CIs), `tr_*.json`, `prep_info.json` (panel, kappa), `core_signature_check.txt`.
- `data/`: per-cohort cell manifests (Census soma_joinid, observation_joinid, donor), enough to re-pull the exact cells.

## What a reviewer asks next
Add a CAR-T product cohort (GEO) and a chronic HIV/HCV cohort. Check whether donor-level (not cell-level) resampling changes the worst-pair verdict. Test whether the 68-gene core predicts clinical response in a CAR-T product dataset.
