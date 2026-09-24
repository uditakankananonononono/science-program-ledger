# P02-01 Build Report: ferroatlas (Ferroptosis Signature Atlas in AD Brain)

**Parent:** CBIO006 Ferroptosis AD Antibodies (2025) | **Spec:** doc290/cbio006-ferroptosis-ad-antibodies/01-ferroptosis-signature-atlas.md
**Built:** 2026-09-24 | **Status:** MIXED - G1 FAIL, G2 PASS as locked but not ferroptosis-specific (post-hoc control), G3 not declared

## What was built
`tool/ferroatlas.py` - per-cohort AD-vs-control differential expression (OLS on z-scored expression,
adjusted for age and sex), a competitive gene-set test for the locked FerrDb V2 set, per-core-gene
random-effects meta-analysis with I^2, and a leave-one-cohort-out (LOCO) elastic-net classifier vs an
age/sex baseline. Tool, gene-set source and gates committed at 89f8821b before any result existed.
Run: `python3 tool/ferroatlas.py <geo_out> data results` (~20 s). `tool/extract_geo.py` builds the
gene-level matrices from GEO series matrices (probe -> symbol from the GEO platform annotation, ambiguous
probes dropped, mean over probes).

## Data
- Gene set: FerrDb V2 driver + suppressor + marker downloads (data/ferrdb_*.csv, 728 rows), filtered to
  Validated, protein-coding -> 313 genes. Core (spec): GPX4, ACSL4, SLC7A11, FTH1, FTL, TFRC, SLC40A1.
- Cohorts (GEO; raw file sha256 in data/source_sha256.txt; phenotype tables in data/):

| cohort | platform | region | AD / control (analysed) |
|--------|----------|--------|-------------------------|
| GSE33000 | Rosetta/Merck GPL4372 (two-colour log ratio) | prefrontal cortex | 310 / 157 |
| GSE132903 | Illumina GPL10558 | middle temporal gyrus | 97 / 98 |
| GSE118553 | Illumina | temporal cortex | 52 / 30 |
| GSE122063 | Agilent GPL16699 (tech reps averaged per subject) | temporal cortex | 12 / 11 |
| GSE48350 | Affymetrix GPL570 | superior frontal gyrus | 21 / 26 |

(GSE33000 and GSE132903 counts: see results/results.json `cohorts` for exact analysed n after age filter.)
One sample per subject in every cohort. Cross-cohort duplicates: cohorts come from different brain banks
and platforms (HBTRC, Banner, ARUK/Nottingham, UCSD, multi-ADRC); no sample IDs are shared, so no
expression-similarity duplicate scan was run across platforms (stated limit).
Spot-check before lock: GSE132903 GPX4 gene value = mean of its 2 probes in the raw series matrix
(first 3 samples 10.1629 / 10.4311 / 10.164, exact match; data/SPOTCHECK.txt).

## Locked amendments (frozen before results)
- GEO instead of AMP-AD (Synapse needs an account and data-use terms).
- No APOE in 4 of 5 cohorts -> G2 baseline is age + sex only.
- One cortical region per cohort; regions differ between cohorts (PFC, MTG, TC, SFG).
- Excluded groups: Huntington's (GSE33000), AsymAD (GSE118553), vascular dementia (GSE122063).
- GSE48350 controls restricted to age >= 60 (the series includes controls aged 20-59).
- GSE5281 excluded (laser-captured neurons, not bulk tissue).

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | set FDR < 0.05 in >= 3 cohorts AND >= 5/7 core genes direction-consistent | set FDR < 0.05 in 1/5 (GSE33000 q = 0.023; others q 0.18-0.87). Core consistent 6/7 as coded (4/7 under the stricter reading, see integrity notes) | **FAIL** |
| G2 | ferroptosis LOCO AUC >= 0.65 AND >= +0.03 over age/sex | 0.776 vs 0.692, delta +0.084 | **PASS** (as locked) |
| G3 | "not stable" declared if >= 4/7 core genes have I^2 > 75% and inconsistent direction | max core I^2 = 67% (SLC7A11); 0 genes meet both | **not declared** |

LOCO AUC per held-out cohort (ferroptosis / baseline): GSE33000 0.862 / 0.905; GSE132903 0.646 / 0.507;
GSE118553 0.844 / 0.743; GSE122063 0.795 / 0.625; GSE48350 0.733 / 0.679.

Core genes (AD t by cohort, random-effects effect on z-scale, I^2):
| gene | t (33000 / 132903 / 118553 / 122063 / 48350) | RE effect | I^2 |
|------|------|------|------|
| GPX4 | -5.68 / -1.93 / -1.61 / -1.58 / -1.51 | -0.49 | 25% |
| ACSL4 | -7.72 / -5.35 / -1.41 / -1.21 / +0.53 | -0.54 | 65% |
| SLC7A11 | +5.28 / +1.94 / +1.66 / -1.01 / -0.76 | +0.25 | 67% |
| FTH1 | +0.79 / -2.13 / -2.31 / -2.05 / -1.39 | -0.32 | 64% |
| FTL | n/a / +2.14 / +0.35 / +2.03 / -0.69 | +0.22 | 37% |
| TFRC | n/a / -2.49 / +0.96 / -1.47 / -0.84 | -0.22 | 41% |
| SLC40A1 | +3.74 / +1.69 / +2.22 / +1.06 / -0.21 | +0.36 | 0% |

## Post-hoc exploratory control (NOT a gate; written after results.json existed)
`tool/exploratory_random_sets.py`: same learner and LOCO on 30 random 251-gene sets (non-FerrDb genes
measured in all 5 cohorts, seed 0). Result (results/exploratory_random_sets.json): random sets reach median mean-LOCO AUC 0.744 (range 0.67-0.89); 7/30 (23%) match or beat the FerrDb set's 0.776. The locked G2 pass is therefore not ferroptosis-specific.

## What the result means
1. **The ferroptosis gene set as a whole is not enriched for AD change beyond the rest of the
   transcriptome** in 4 of 5 cohorts. Only the largest cohort (GSE33000) passes, and there the set is
   shifted relative to background.
2. **A few core genes move consistently:** GPX4 is lower in AD in all 5 cohorts (low heterogeneity),
   ACSL4 lower in 4/5, SLC40A1 (ferroportin) higher in 4/5. That is a mixed picture - lower GPX4 fits
   ferroptosis vulnerability, but lower ACSL4 points the other way.
3. **G2 passes on paper but is not evidence for ferroptosis.** The control shows random gene sets of
   the same size reach similar LOCO AUCs, so the gain over age/sex reflects broad AD transcriptome change
   (neuronal loss, glial activation), not a ferroptosis-specific signal.
4. **Limits:** bulk tissue (cell-composition shifts can drive every core gene), mixed regions and
   platforms, no APOE, small GSE122063.

## Integrity notes
- Post-lock parser fix (2a9e1ff0): the first run crashed before producing any output because GSE118553
  has age "NA" for some subjects; age is now parsed as missing and those subjects dropped. No gate or
  analysis change.
- Core-gene consistency rule as coded: with 5 cohorts, >= 4 same sign; with 4 cohorts (FTL, TFRC absent
  from GPL4372 gene mapping), >= 3 same sign. The docstring says ">= 4 of the cohorts where measured";
  under that stricter reading FTL and TFRC fail, giving 4/7 (< 5). G1 fails under both readings.
- The random-set control is post-hoc and labelled as such; it does not change the locked G2 verdict.

## What this build needs next
- Cell-type deconvolution (or adjustment for neuronal/glial proportions) before calling any core-gene change ferroptosis-related; P02-06 (single-cell) is the right follow-up.
- AMP-AD (ROSMAP/MSBB/Mayo RNA-seq) with APOE for the spec's full baseline, via a Synapse account.
- A set-specificity control locked as a gate in any future ferroptosis-score classifier.
