# P01-01 Build Report: crc-transport-audit (CRC Microbiome Cross-Cohort Transport Stress Test)

**Parent:** CBIO003 CRC Gut Microbiome (2025) | **Spec:** doc290/cbio003-crc-gut-microbiome/01-cross-cohort-transport.md
**Built:** 2026-09-24 | **Status:** MIXED RESULT - G1 PASS, G2 FAIL, G3 PASS (locked gates evaluated once, no re-fishing)

## What was built
`tool/crc_transport_audit.py` - a complete, rerunnable pipeline: frozen harmonized
8-cohort genus-level benchmark (data/), Random Forest recipe locked to the parent's
(500 trees, balanced class weights), within-cohort 5-fold CV, full LOCO evaluation,
geography-only confound baseline, per-cohort mean|SHAP| importance ranks, pairwise
Spearman transport scores with 1000-permutation nulls, and locked-gate evaluation.
Run: `python3 tool/crc_transport_audit.py data results` (~1 min, sklearn+shap).

## Data (frozen in data/, provenance)
767 fecal shotgun samples (385 CRC / 382 CTR), 164 genera aggregated from the
849-species mOTU table published as Supplementary Data 1 of Wirbel et al. 2019
(Nat Med, doi:10.1038/s41591-019-0406-6). One locked pipeline (mOTUv2) for all
cohorts - removes harmonization confound. Sample metadata from Supplementary
Data panels of the same paper (MOESM8 Panel_b, MOESM9 Panel_c). Cohort identity
bound by exact case/control count match to Suppl. Table S2 and ENA lookups:
CN-Yu (PRJEB10878, 127), CN-Feng (PRJEB7774, 109), AT-Wirbel (114), DE-Wirbel
(120), US-Vogtmann (104), IT1-Thomas (53), IT2-Thomas (60), JP-Yachida (80).
One matrix sample (ERR1018294) lacked published metadata and was excluded.
Amendment vs spec data section: curatedMetagenomicData needs R/Bioconductor; the
identical underlying cohorts were taken from the publisher's supplementary tables
instead. Indian cohort (spec, optional): none found open on GMrepo/SRA during QC;
the build tests transport across 8 non-Indian cohorts (QC.md P01-01 note).

## Locked amendments (frozen before results)
- G2 wording ("taxa replicate") operationalized as: >=5 cohort pairs (of 28) with
  Spearman rho >= 0.6 over the union of each pair's top-20 mean|SHAP| ranks,
  1000-permutation p < 0.05.
- Age/BMI baseline dropped: per-sample age/BMI is not in the public supplement.
  Geography-only baseline retained for G3.
- SHAP used as spec'd (shap 0.49.1 TreeExplainer); permutation fallback not needed.

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | mean LOCO AUC >= 0.75, >=6 cohorts | 0.832 over 8 cohorts, boot95 CI [0.793, 0.869] | **PASS** |
| G2 | >=5 pairs rho >= 0.6 (perm p<0.05) | 0 of 28 pairs (max rho 0.116; mean rho -0.308) | **FAIL** |
| G3 | geography-only AUC < 0.70 | 0.511 | **PASS** |

Within-cohort 5-fold CV AUCs: CN-Feng 0.941, DE 0.897, CN-Yu 0.880, AT 0.824,
JP 0.827, IT2 0.749, US 0.633, IT1 0.596.
LOCO AUCs: CN-Yu 0.908, CN-Feng 0.884, DE 0.842, AT 0.825, JP 0.881,
IT2 0.820, IT1 0.763, US 0.736.

## What the mixed result means
1. **Predictions transport; feature identity does not.** A model trained on any
   7 cohorts scores 0.74-0.91 AUC on the 8th - far above the geography baseline
   (0.511) and above the locked 0.75 bar. Yet the *ranking* of which genera carry
   the signal is cohort-specific to the point of anti-correlation (mean rho -0.31).
   Single-cohort feature-importance reports (like the parent's biomarker list)
   should be read as cohort-local, even when the classifier itself is portable.
2. **A small oral-pathogen core does recur.** Parvimonas and Peptostreptococcus
   are top-5 in 5 of 8 cohorts, Fusobacterium and Gemella in 4 of 8 - the known
   CRC oral-pathogen axis. But below the top handful, importance is cohort-local,
   and no pair reaches the locked rho >= 0.6 bar.
3. **Confounding is ruled out as the driver** (G3): cohort membership alone
   predicts CRC at chance (0.511 AUC) under 5-fold CV.
4. **The parent's 0.992 single-cohort AUC is consistent with within-cohort CV**
   (CN-Feng 0.941 here) and says nothing about transport; the transport number
   for an Indian-cohort model remains unmeasured - the open question the parent
   project most needs answered.

## What this build needs next
- A public Indian CRC shotgun cohort (none found open during QC) to run the
  actual parent-relevant transport direction.
- Effect-direction (fold-change sign) consistency as a locked complement to
  magnitude-rank correlation in any G2 successor - post-hoc here, must be
  pre-locked there.

## Honesty notes
- G2 failed as locked; no alternative metric was substituted to rescue it.
- Genus aggregation sums mOTU "unknown <genus>" clades into their named genus
  where possible; 164 genera, 1% prevalence filter (locked).
- All randomness seeded (7); full results in results/results.json.

## Erratum (2026-09-24, cohort names only - no numbers change)
Two cohort labels in data/samples.csv and in this report are misnamed. Checked against the
`block` column of Wirbel 2019 MOESM8 Panel_b (all 574 discovery samples join, 0 label mismatches):
| label used here | correct cohort | evidence |
|---|---|---|
| AT-Wirbel (CCIS ids, 114) | **FR-Zeller** (Zeller et al. 2014, France) | block = FR-CRC for all 114 |
| CN-Feng (SAMEA ids, 109) | **AT-Feng** (Feng et al. 2015, Austria, PRJEB7774) | block = AT-CRC for all 109 |
The sample groupings are correct, so every LOCO fold, AUC, and gate verdict is unchanged; the
geography-only baseline uses cohort one-hot, not country, so it is also unaffected. Read
"AT-Wirbel" as FR-Zeller and "CN-Feng" as AT-Feng wherever they appear. Frozen data files are
left byte-identical so results stay reproducible. Also noted: CN-Yu is two sequencing batches in
the source (CN-CRC_BEFORE 51 / CN-CRC_AFTER 76), relevant to P01-02.
