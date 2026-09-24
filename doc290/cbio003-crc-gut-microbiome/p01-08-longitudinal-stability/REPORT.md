# P01-08 Build Report: stabl (Longitudinal Stability of CRC Microbiome Markers)

**Parent:** CBIO003 CRC Gut Microbiome (2025) | **Spec:** doc290/cbio003-crc-gut-microbiome/08-longitudinal-stability.md
**Built:** 2026-09-24 | **Status:** MIXED - G1 FAIL, G2 PASS, G3 FAIL (locked gates evaluated once, no re-fishing)

## What was built
`tool/stabl.py` - per-species temporal ICC in healthy and IBD longitudinal arms, antibiotic response,
a top-50 CRC-marker stability scorecard (results/top50_scorecard.csv), and a stability-weighted vs
unweighted classifier comparison under simulated antibiotic and temporal perturbation, leave-one-
cohort-out (LOCO) over 5 CRC cohorts. Tool and gates were committed (4411743a) before the run.
Run: `python3 tool/stabl.py data results` (~1.5 min).

## Data (frozen in data/)
curatedMetagenomicData 2021-03-31 MetaPhlAn2 species tables fetched from ExperimentHub and parsed
with python `rdata`:
- CRC: ZellerG_2014, FengQ_2015, YachidaS_2019, ThomasAM_2018a, HanniganGD_2017 (same tables as P01-07; CRC vs control).
- Healthy longitudinal: HMP_2019_ibdmdb non-IBD controls, 426 samples / 27 subjects (EH5590).
- Perturbed longitudinal: HMP_2019_ibdmdb IBD arm, 1182 samples / 84 subjects.
- Antibiotic: RaymondF_2016 cephalosporin arm, paired day 7 vs day 0, 18 subjects (EH5770).

## Locked amendments (frozen before results)
- Diet arm dropped: David 2014 is 16S and not in cMD; no shotgun diet time series was frozen.
- Top-50 markers ranked from the cMD CRC cohorts (MetaPhlAn names, to match the longitudinal
  tables) instead of P01-01/P01-03 mOTU lists.
- Stability weighting via feature scaling in L2 logistic regression (Random Forest ignores feature
  scale); a model-matched unweighted logistic is reported as control.
- Primary perturbation = mean cephalosporin day-7 log10 shift per species; temporal noise secondary.

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | healthy ICC for all top-50 markers | 46/50; no ICC for Gemella morbillorum, Peptostreptococcus stomatis, Solobacterium moorei, Dialister pneumosintes (never detected in HMP healthy controls) | **FAIL** |
| G2 | >= 60% of top-50 with ICC >= 0.4 | 72% (median ICC 0.62) | **PASS** |
| G3 | weighted loss < 0.03 AND unweighted RF loss >= 0.05 | RF loss -0.013 (antibiotic shift raised AUC), weighted -0.000 | **FAIL** (weighting non-beneficial) |

Mean LOCO AUC (clean / antibiotic-shifted / temporal noise): parent RF 0.726 / 0.739 / 0.717;
stability-weighted logistic 0.636 / 0.636 / 0.631; unweighted logistic 0.655 / 0.655 / 0.657.

Low-ICC (< 0.4) top markers: Streptococcus salivarius, Anaerostipes hadrus, Parvimonas micra (0.15),
Fusobacterium nucleatum (0.08), Eisenbergiella tayi, Blautia wexlerae, Porphyromonas asaccharolytica,
Streptococcus thermophilus, Anaerotruncus colihominis, Enterorhabdus caecimuris.

## What the result means
1. **Most CRC markers are stable in healthy people (72% ICC >= 0.4), but the oral-pathogen core is
   not measurable this way.** The species that drive transport and the P01-05 panel (P. micra,
   F. nucleatum, G. morbillorum, P. stomatis) are absent or near-absent in healthy guts, so their
   ICC is undefined or low. That fits a tumor-associated signal rather than a stable host trait. It
   also means their within-person stability in people WITH CRC is unknown - the real open question.
2. **Perturbation did not hurt the parent RF**, so weighting had nothing to protect against. The
   weighted model paid ~0.09 AUC vs the RF (0.02 vs the matched logistic) for no robustness gain.
3. **Limits:** 27 healthy subjects; a population-mean antibiotic shift is gentler than a real
   individual course; zero-inflated abundances make ICC partly a presence/absence stability measure.

## What this build needs next
- Repeat-sampled stool from CRC patients (none open in cMD) to measure marker stability where the markers are present.
- Individual-level antibiotic perturbation (apply each Raymond subject's own shift) as a locked sensitivity check.
- A shotgun diet-perturbation time series to restore the diet arm.
