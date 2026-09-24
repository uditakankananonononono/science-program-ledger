# P01-02 Build Report: batchtruth (Adversarial Batch and Leakage Audit of Single-Cohort CRC Models)

**Parent:** CBIO003 CRC Gut Microbiome (2025) | **Spec:** doc290/cbio003-crc-gut-microbiome/02-batch-leakage-audit.md
**Built:** 2026-09-24 | **Status:** 4 of 5 cohorts PASS; DE-Wirbel FLAGGED CONFOUNDED and FAILS G2 (locked gates evaluated once, no re-fishing)

## What was built
`tool/batchtruth.py` - per-cohort audit: metadata-only classifier on per-sample sequencing
metadata, unprotected Random Forest (parent recipe: 500 trees, balanced), a ComBat-style arm for
multi-batch cohorts, and a leakage-protected pipeline (technical covariates regressed out of
genus CLR features inside each training fold) scored against 100 label permutations stratified
within batch. Tool and gates were committed (cea20104) before the first run.
Run: `python3 tool/batchtruth.py data results` (~35 min CPU, 2 cores).

## Data (frozen in data/)
- genus_matrix.csv, samples.csv: same frozen benchmark as P01-01 (cohort names per P01-01 erratum).
- ena/*.tsv: ENA filereport run tables for PRJEB10878 (CN-Yu), PRJEB7774 (AT-Feng), PRJEB6070
  (FR-Zeller), PRJEB27928 (DE-Wirbel), PRJEB12449 (US-Vogtmann).
- tech_metadata.csv: per-sample reads, bases, run count, instrument, layout - 574/574 discovery
  samples matched. cnyu_blocks.csv: CN-Yu sequencing blocks from Wirbel 2019 MOESM8 Panel_b.

## Locked amendments (frozen before results)
1. No torch in the environment: the gradient-reversal MLP is replaced by fold-wise OLS
   residualization of every feature on the technical covariates (same aim: remove technical
   signal the classifier could exploit).
2. ComBat without empirical-Bayes shrinkage (numpy), run only where a cohort has >1 batch.
3. SRA technical metadata taken from ENA filereport (same runs as the SRA Run Selector).
4. IT1/IT2/JP external cohorts excluded from all gates: no technical metadata fetched.
5. 100 permutations, so the smallest reachable p is 1/101 = 0.0099 (< 0.01 needs 0/100 exceed).
6. adjusted AUC = observed - (null mean - 0.5).

## Results vs locked gates
| cohort | n (CRC) | meta-only AUC (G1) | unprotected RF | ComBat RF | residualized RF | null mean | adjusted AUC | perm p | G2 |
|---|---|---|---|---|---|---|---|---|---|
| AT-Feng | 109 (46) | 0.666 | 0.882 | - | 0.892 | 0.489 | 0.903 | 0.0099 | **PASS** |
| CN-Yu | 127 (73) | 0.671 | 0.824 | 0.857 | 0.837 | 0.558 | 0.779 | 0.0099 | **PASS** |
| DE-Wirbel | 120 (60) | **0.959 CONFOUNDED** | 0.837 | 0.961 | 0.976 | 0.945 | 0.530 | 0.0099 | **FAIL** |
| FR-Zeller | 114 (53) | 0.596 | 0.771 | - | 0.805 | 0.492 | 0.813 | 0.0099 | **PASS** |
| US-Vogtmann | 104 (52) | 0.504 | 0.703 | - | 0.719 | 0.480 | 0.739 | 0.0099 | **PASS** |

G3: verdicts are per cohort only; no pooled model was fit in this build.

## What the result means
1. **DE-Wirbel is confounded by sequencing instrument.** In ENA, all 54 HiSeq 2000 samples are CRC
   and 60 of 66 HiSeq 4000 samples are controls; CRC samples also have about twice the reads
   (median 37.2M vs 18.7M). Sequencing metadata alone predicts CRC at 0.959 AUC. Any
   within-cohort accuracy for DE cannot be separated from instrument: the batch-stratified null
   sits at 0.945, leaving an adjusted AUC of 0.530. ComBat does not fix this; it raises AUC to
   0.961 because batch and label are nearly the same variable.
2. **The other four cohorts hold up.** Metadata-only AUC is 0.50-0.67, and protected AUCs stay
   0.72-0.89 with adjusted AUC 0.74-0.90, all beyond every permutation. CN-Yu's two blocks are
   unbalanced (52/24 vs 21/30 CRC/CTR) but removing block effects does not remove the signal.
3. **For the parent's AUC 0.992:** a single-cohort figure that high is exactly the pattern DE
   shows here. Without per-sample sequencing metadata from the parent's cohort, it cannot be
   audited; the parent should report instrument/run/depth by class.
4. **Downstream:** P01-01/P01-04 LOCO folds that include DE in training carry this confound. The
   DE held-out LOCO scores (0.84) remain meaningful as transport tests (model trained elsewhere),
   but DE should not be used for marker discovery. P01-05 excludes DE-only markers by its locked rule.

## What this build needs next
- Tech metadata for IT1/IT2 (Thomas 2019, PRJNA447983) and JP (Yachida, DRA) to extend the audit.
- A true gradient-reversal arm when torch is available (same gates).
- Nonlinear residualization check (current removal is linear only).
