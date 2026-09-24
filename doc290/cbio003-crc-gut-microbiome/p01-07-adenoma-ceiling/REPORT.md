# P01-07 Build Report: adenoma-ceiling (Detecting Pre-Cancerous Adenomas from the Gut Microbiome)

**Parent:** CBIO003 CRC Gut Microbiome (2025) | **Spec:** doc290/cbio003-crc-gut-microbiome/07-adenoma-detection.md
**Built:** 2026-09-24 | **Status:** NEGATIVE - G1 FAIL, G2 FAIL, G3 FAIL (locked gates evaluated once, no re-fishing). Spec's failure rule applies: the detection-ceiling result is published as the outcome.

## What was built
`tool/adenoma_ceiling.py` - leave-one-cohort-out (LOCO) adenoma-vs-control classifier scored on
advanced adenomas, a carcinoma-trained continuum test, and a per-cohort stage-consistency marker
scan. Model everywhere = parent recipe Random Forest (500 trees, balanced, seed 7) on log10
species abundance. Tool and gates were committed (88743925) before the run.
Run: `python3 tool/adenoma_ceiling.py data results` (~1 min).

## Data (frozen in data/)
curatedMetagenomicData 2021-03-31 release (MetaPhlAn2 species relative abundance), fetched without
R from Bioconductor ExperimentHub (EH5938 ZellerG_2014, EH5530 FengQ_2015, EH5902 YachidaS_2019,
EH5842 ThomasAM_2018a, EH5566 HanniganGD_2017) plus cMD sampleMetadata.rda (waldronlab GitHub),
parsed with python `rdata`. 1047 stool samples, one per subject: 482 CRC / 209 adenoma / 425
control. Advanced labels: Feng advancedadenoma (47), Zeller largeadenoma (15, treated as advanced).
Yachida "carcinoma_surgery_history" excluded.

## Locked amendments (frozen before results)
- Three-group ordinal classifier replaced by two binary models (adenoma-vs-control; carcinoma-trained continuum score).
- Adenoma model trained on all adenoma labels (advanced labels too scarce to train on), evaluated on advanced only.
- Continuum "paired test" -> two one-sided Mann-Whitney tests (groups are different people; no pairing exists).
- Pathway-restricted (genotoxin/inflammation) model not run: species-level build only.
- Yachida adenomas are not advanced-labelled in cMD: used in training, G2 and G3, not G1 evaluation.

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | advanced-adenoma LOCO AUC >= 0.65, CI low > 0.55 | 0.518, boot95 [0.410, 0.625] (Feng 0.543, Zeller 0.492) | **FAIL** |
| G2 | continuum (adenoma > control and CRC > adenoma, both p<0.05) in >= 3 cohorts | 0 of 5 | **FAIL** |
| G3 | >= 3 stage-consistent species replicating in >= 2 cohorts | 0 (12 hits, all Yachida-only) | **FAIL** |

Secondary (no gate) any-adenoma LOCO AUC: Feng 0.543, Hannigan 0.558, Thomas 0.579, Yachida
0.506, Zeller 0.555; mean 0.548.

Continuum detail (median carcinoma-trained score control / adenoma / CRC; one-sided p adenoma>control; CRC>adenoma):
| cohort | control | adenoma | CRC | p(A>C) | p(CRC>A) |
|---|---|---|---|---|---|
| FengQ_2015 | 0.400 | 0.430 | 0.524 | 0.060 | <0.001 |
| HanniganGD_2017 | 0.290 | 0.277 | 0.296 | 0.486 | 0.197 |
| ThomasAM_2018a | 0.515 | 0.528 | 0.562 | 0.101 | 0.038 |
| YachidaS_2019 | 0.498 | 0.518 | 0.558 | 0.065 | <0.001 |
| ZellerG_2014 | 0.432 | 0.449 | 0.594 | 0.323 | <0.001 |

## What the result means
1. **Stool species profiles do not detect advanced adenomas across cohorts.** Held-out AUC is at
   chance (0.52; CI includes 0.5). This is the detection ceiling for this data and model class.
2. **Adenomas look like controls, not like early cancer.** The carcinoma score separates CRC from
   adenoma in 4 of 5 cohorts, but adenoma vs control never reaches p<0.05. Adenoma medians sit
   slightly above controls in 4 of 5 cohorts (p 0.06-0.32) - a hint of ordering too weak to confirm
   at these sample sizes.
3. **No adenoma marker replicates**: all 12 FDR<0.1 adenoma species are from Yachida alone
   (largest cohort, 67 adenomas); none repeat in a second cohort.
4. **For the parent project:** the CRC signal it models is mostly a carcinoma-stage signal (the
   oral-pathogen core, see P01-01/P01-05). Claims about pre-cancer screening from this signal are
   not supported by public data.
5. **Limits:** only 62 advanced adenomas across 2 cohorts, so the G1 CI is wide (upper 0.63); a
   modest real signal (AUC ~0.6) cannot be excluded. Species level only; pathways untested.

## What this build needs next
- Sample-size calculation: advanced adenomas needed to confirm or exclude AUC 0.60 (locked before use).
- Pathway-level rerun (cMD HUMAnN pathway tables are fetchable the same way) with gates unchanged.
- Yachida stage-resolved (MP / stage 0) labels from the original supplement for the stage trajectory.
