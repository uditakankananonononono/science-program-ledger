# P01-01 Addendum: Transport To and From the Open Indian CRC Cohort (GuptaA_2019)

**Approved by the lane parent 2026-09-24.** Tools and gates locked in commit 27875788 before any
result existed. Main P01-01 gates were rerun with an identical copy of tool/crc_transport_audit.py.

## Data
curatedMetagenomicData 2021-03-31 (ExperimentHub, python `rdata`), 10 stool CRC cohorts, 1314
samples: GuptaA_2019 (India, 30 CRC / 30 control), FengQ_2015, HanniganGD_2017, ThomasAM_2018a,
ThomasAM_2018b, VogtmannE_2016, WirbelJ_2018, YachidaS_2019, YuJ_2015, ZellerG_2014.
ThomasAM_2019_c excluded (duplicate of Yachida, project QC rule). Genus = MetaPhlAn2 species summed
by first name token. Different profiler from the main P01-01 benchmark (mOTU), so numbers are not
pooled with the main report. WirbelJ_2018 is instrument-confounded (P01-02) - kept for comparability.

## Results
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 (main, unchanged) | mean LOCO AUC >= 0.75 over >= 6 cohorts | 0.782 [0.716, 0.834], 10 cohorts | **PASS** |
| G2 (main, unchanged) | >= 5 pairs rho >= 0.6 (perm p<0.05) | 0 of 45 (max rho 0.03; India vs each: -0.38 to -0.65) | **FAIL** |
| G3 (main, unchanged) | geography-only AUC < 0.70 | 0.507 | **PASS** |
| A1 | others -> India held-out AUC >= 0.75 | 0.856 | **PASS** |
| A2 | India-trained -> mean AUC on other 9 >= 0.75 | 0.681 (range 0.385 Hannigan - 0.804 Wirbel) | **FAIL** |

India within-cohort 5-fold CV AUC: 0.953 (the parent reports 0.992 on its own Indian cohort).

## What it means for the parent project
1. **A model trained on other populations works on Indian patients** (0.856) - the global CRC signal
   reaches this Indian cohort.
2. **A model trained only on an Indian cohort does not travel well** (0.681 mean; 5 of 9 cohorts
   below 0.75), even though it scores 0.95 inside its own cohort. This is the parent's exact setup:
   a near-perfect single-cohort AUC says little about use elsewhere, and 60 samples is a small base.
3. **The Indian model leans on different genera**: its top features are Flavonifractor, Prevotella,
   Odoribacter, Veillonella, Ruthenibacterium; the other cohorts lean on the oral-pathogen core
   (Peptostreptococcus, Parvimonas, Fusobacterium). Importance ranks anti-correlate (rho -0.38 to
   -0.65). Whether that reflects Indian gut biology (e.g., Prevotella-rich diets) or a 60-sample
   model fitting noise cannot be separated with one small cohort.
4. **Limits:** one Indian cohort, 60 samples; different profiler from the main benchmark.

## Needs next
- A second Indian shotgun cohort (or the parent's own data) to tell population biology from small-cohort overfitting.
