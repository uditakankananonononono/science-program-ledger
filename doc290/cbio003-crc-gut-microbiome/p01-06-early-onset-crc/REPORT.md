# P01-06 Build Report: eo-crc-atlas (Early-Onset CRC: Distinct or Shared Microbiome Signal?)

**Parent:** CBIO003 CRC Gut Microbiome (2025) | **Spec:** doc290/cbio003-crc-gut-microbiome/06-early-onset-crc.md
**Built:** 2026-09-24 | **Status:** G1 FAIL (data condition: 1 cohort with >=30 EOCRC). G2: the locked run says "distinct signal", but that result is **invalidated by duplicate samples across two cohorts**; after removing the duplicate cohort the shared-signal null holds. G3: age confounding NOT the primary finding.

## Lock evidence
Tool, gates and the locked cohort list were committed in c568fd11 (commit time 12:53:30 IST);
the first results file was written at 12:55:49 IST. (The docstring's "12:56" lock time is a
typo - the commit is the evidence.)

## What was built
`tool/eocrc.py` - early-onset (<50) vs late-onset comparison: per-cohort EOCRC counts and power,
within-cohort EOCRC AUC where n >= 30, EO-trained vs size-matched LO-trained models on held-out
EOCRC (leave-one-cohort-out), and age-residualized case-control LOCO.
Run: `python3 tool/eocrc.py data results [excluded studies]` (~2 min).

## Data (frozen in data/) - locked cohort list (resolves the QC FIX item)
All 11 curatedMetagenomicData 2021-03-31 stool CRC studies with per-sample age (ExperimentHub,
parsed with python `rdata`): ZellerG_2014, FengQ_2015, YachidaS_2019, ThomasAM_2018a,
ThomasAM_2018b, ThomasAM_2019_c, HanniganGD_2017, GuptaA_2019 (India), VogtmannE_2016,
WirbelJ_2018, YuJ_2015. 1394 samples, one per subject within each study.

EOCRC cases / controls <50 per cohort: Yachida 32/52, Thomas2019c 10/9, Vogtmann 8/11, Wirbel 7/17,
Hannigan 6/6, Feng 4/3, Gupta 4/15, Thomas2018b 4/4, Yu 4/0, Zeller 3/8, Thomas2018a 0/0.
Hanley-McNeil SE of an AUC of 0.70: 0.061 in Yachida, 0.12-0.21 everywhere else.

## Locked amendments (frozen before results)
- Entropy balancing replaced by age-stratum restriction of controls (BMI mostly missing).
- TCGA tissue layer not used. The "shifted" classifier is not scored separately (AUC ignores thresholds).

## Data-integrity finding (found after the locked run)
ThomasAM_2019_c (Japan, 80 samples) duplicates YachidaS_2019: every Thomas2019c profile has a
Yachida profile with cosine similarity >= 0.9995 (all 80 > 0.99; within-Yachida nearest-neighbour
median is 0.66, and no other cohort pair exceeds 0.82). The same people appear under two study
names, so any fold with one of them held out and the other in training leaks. Thomas2019c's
LOCO AUC of 1.000 was the symptom. **Correction (post-result, clearly labelled, gates unchanged):**
rerun with ThomasAM_2019_c excluded -> results_dedup/. Both result sets are kept.

## Results vs locked gates
| gate | criterion | locked run (results/) | dedup rerun (results_dedup/) | verdict |
|------|-----------|-----------|-----------|---------|
| G1 | >= 2 cohorts with >= 30 EOCRC | 1 (Yachida; within-cohort AUC 0.551) | 1 (0.553) | **FAIL** (data condition; power above) |
| G2 | EO-trained - LO-trained (size-matched) >= 0.05 on held-out EOCRC | 0.817 vs 0.715, diff +0.103 [0.030, 0.173] | 0.695 vs 0.690, diff +0.005 [-0.066, 0.074] | **Locked "distinct" result invalid (leakage); corrected: shared-signal null** |
| G3 | age-residualized LOCO AUC < 0.60 => age confounding primary | 0.819 (unadjusted 0.815) | 0.796 (unadjusted 0.788) | **Not age-confounded** |

What drove the locked G2 result: Yachida's 32 EOCRC cases scored 0.812 with the EO model when
Thomas2019c (its duplicate) was in training, and 0.608 without it. The full-size LO model
(0.739 dedup) does as well on EOCRC as either size-matched model.

Age from microbiome (controls, 5-fold RF R^2): 0.26 (locked) / 0.19 (dedup) - age is partly
encoded, but removing it linearly does not lower case-control AUC.

## What the result means
1. **No evidence for a distinct EOCRC microbiome signal** once duplicate samples are removed: a
   model trained on young patients detects young patients no better than one trained on older
   patients (diff +0.005). A model trained on all older samples does slightly better, which fits a
   shared signal where more data helps.
2. **The data cannot support a strong claim either way:** only 68-78 EOCRC cases across public
   cohorts, and only Yachida has >= 30. The field's EOCRC-distinct claim is not testable at
   power with open shotgun data today.
3. **Age is not what CRC classifiers are detecting** (G3).
4. **Knock-on:** ThomasAM_2019_c must never be combined with YachidaS_2019 in cMD-based builds.
   P01-07 and P01-08 did not use ThomasAM_2019_c. GuptaA_2019 is an open Indian CRC cohort (30/30) -
   this closes the P01-01 "no Indian cohort" gap for a locked transport addendum.

## What this build needs next
- More EOCRC shotgun cases (e.g., new SRA submissions) to reach >= 2 cohorts with >= 30.
- Nonlinear age adjustment (current removal is linear).
