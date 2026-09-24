# P01-05 Build Report: panelpick (Minimal qPCR-Ready CRC Microbial Panel)

**Parent:** CBIO003 CRC Gut Microbiome (2025) | **Spec:** doc290/cbio003-crc-gut-microbiome/05-minimal-qcpr-panel.md
**Built:** 2026-09-24 | **Status:** G1 PASS, G2 PASS, G3 PASS (locked gates evaluated once, no re-fishing) - with the practical caveats below

## What was built
`tool/panelpick.py` - fully nested panel selection inside each leave-one-cohort-out (LOCO) fold:
replication filter (MW BH-FDR<0.05 in >=3 training cohorts), 1000-subsample L1 stability
selection, batch-confound exclusion using P01-02, greedy forward selection (budget 8) on inner
LOCO AUC, linear (L2 logistic) panel scoring, and a qPCR noise simulation on the held-out cohort.
Full-metagenome reference = Random Forest (parent recipe) on all species. Tool and gates were
committed (e4f74dd3) before the run.
Run: `python3 tool/panelpick.py data results ../p01-02-batch-leakage-audit/data/tech_metadata.csv ../p01-02-batch-leakage-audit/results/per_cohort.csv` (~1 min).

## Data (frozen in data/)
species_matrix.csv: 767 samples x 849 mOTU species from Wirbel 2019 Suppl. Data 1
(doi:10.1038/s41591-019-0406-6), same samples/cohorts as P01-01; 10/10 alignment spot-check vs
source xlsx (data/alignment_spotcheck.txt). Cohort names per the P01-01 erratum.

## Locked amendments (frozen before results)
- Species level (qPCR targets are species), >=5% prevalence; panel scored by L2 logistic regression.
- Batch-confound flags: (a) |Spearman rho| >= 0.3 with log10 reads among controls in >=2 of 5
  discovery cohorts; (b) species replicating only through cohorts P01-02 flagged (DE-Wirbel).
- qPCR noise: +N(0, 0.301) log10 (Ct SD 1.0) and 5% limit-of-detection dropout, 20 draws.
- 16S cross-platform penalty and primer drafting not run; cost model not computed (needs sourced prices).

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | panel LOCO >= 0.90 x full AND >= 0.70 | panel 0.786 vs full 0.832 (ratio 0.946) | **PASS** |
| G2 | qPCR-noise degradation < 0.05 | 0.011 (0.786 -> 0.776) | **PASS** |
| G3 | no batch-confounded marker in panel | 0 flagged species selected (5 read-depth-flagged species excluded upstream; none reached the candidate pool) | **PASS** |

| held-out cohort | full RF | panel (clean) | panel (qPCR noise) | panel size |
|---|---|---|---|---|
| AT-Feng | 0.879 | 0.860 | 0.839 | 6 |
| CN-Yu | 0.932 | 0.841 | 0.825 | 5 |
| DE-Wirbel | 0.831 | 0.834 | 0.826 | 5 |
| FR-Zeller | 0.861 | 0.730 | 0.720 | 6 |
| IT1-Thomas | 0.730 | 0.697 | 0.689 | 7 |
| IT2-Thomas | 0.785 | 0.802 | 0.788 | 7 |
| JP-Yachida | 0.856 | 0.821 | 0.821 | 7 |
| US-Vogtmann | 0.779 | 0.705 | 0.697 | 7 |

Panel membership across the 8 outer folds (a stable result): Parvimonas micra 8/8, Gemella
morbillorum 8/8, Fusobacterium nucleatum subsp. animalis 8/8, Peptostreptococcus stomatis 8/8,
unknown Dialister (meta-mOTU 5867) 8/8, Hungatella hathewayi 5/8, Parvimonas sp. (mOTU 4961) 5/8.

Ceiling curve (mean held-out AUC by panel size; sizes 6-7 average over fewer folds):
1: 0.707, 2: 0.739, 3: 0.770, 4: 0.780, 5: 0.782, 6: 0.765, 7: 0.756.

## What the result means
1. **A 4-5 target oral-pathogen panel keeps about 95% of full-metagenome transport accuracy**,
   and simulated qPCR noise costs only about 0.01 AUC. Gains flatten after 4-5 targets.
2. **The replication filter, not the 8-target budget, set panel size**: only 5-7 species replicate
   in >=3 training cohorts, so every fold's greedy search ran out of candidates before 8.
3. **Practical caveats:** (a) one core member is an unnamed meta-mOTU ("unknown Dialister") with no
   reference genome, so no qPCR assay exists yet; a buildable panel is Parvimonas micra, Gemella
   morbillorum, F. nucleatum, P. stomatis (+ H. hathewayi). (b) Per-cohort panel AUC falls just under
   0.70 in IT1 (0.697) and US (0.705) - the gate is on the mean. (c) qPCR noise is simulated; real
   assay cross-reactivity and extraction bias are not modeled. (d) No Indian cohort (parent's setting).

## What this build needs next
- Source published qPCR assays/primers for P. micra, G. morbillorum, F. nucleatum, P. stomatis,
  H. hathewayi; decide on the Dialister meta-mOTU (drop, or design from metagenome-assembled genomes).
- Refit the 4-named-species panel as a locked sensitivity check.
- Cost model with sourced per-sample qPCR, 16S and shotgun prices; 16S cross-platform penalty.
