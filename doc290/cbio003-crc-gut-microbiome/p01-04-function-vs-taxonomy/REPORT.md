# P01-04 Build Report: funtransport (Does Microbial Function Out-Transport Taxonomy for CRC?)

**Parent:** CBIO003 CRC Gut Microbiome (2025) | **Spec:** doc290/cbio003-crc-gut-microbiome/04-function-vs-taxonomy.md
**Built:** 2026-09-24 | **Status:** NEGATIVE ON THE MAIN HYPOTHESIS - G1 FAIL, G2 FAIL, G3 PASS (locked gates evaluated once, no re-fishing)

## What was built
`tool/funtransport.py` - rerunnable pipeline comparing three feature views under one
identical model (HistGradientBoostingClassifier, max_iter=150, early stopping, seed 7) and
leave-one-cohort-out (LOCO) evaluation over the same 8 frozen cohorts as P01-01:
taxonomy (164 genera), function (COG relative abundance), and combined. Paired
cohort-bootstrap CI on the function-minus-taxonomy LOCO difference, plus a per-cohort
Mann-Whitney + BH-FDR replication scan over every extracted COG.
Run: `gunzip -k data/cog_matrix.csv.gz && python3 tool/funtransport.py data results` (~2 min, ~1GB RAM).

## Data (frozen in data/, provenance)
- samples.csv, genus_matrix.csv: identical to P01-01 (767 samples, 385 CRC / 382 CTR, 8 cohorts).
- cog_matrix.csv.gz: 767 samples x 30,310 COG/eggNOG groups (5% prevalence filter over 31,185)
  from Supplementary Data 2 of Wirbel et al. 2019 (Nat Med, doi:10.1038/s41591-019-0406-6),
  the same publication and pipeline as the taxonomy table. sha256 of the uncompressed CSV
  is in data/cog_matrix.csv.sha256.
- Extraction check: the first extraction had an off-by-one column shift (xlsx header corner
  cell). It was caught before any model was fit, deleted, re-extracted, and spot-verified:
  10/10 values (5 COGs x 2 samples from different cohorts, zero and non-zero) match the source
  xlsx exactly - see results/alignment_spotcheck.txt.

## Locked amendments (frozen before results)
1. Function = COG relative abundance from the same frozen supplement, not a HUMAnN3/MetaCyc
   rerun on raw reads (infeasible here; a rerun would also mix pipelines across cohorts).
2. Model view uses COGs at >=20% prevalence (25,684 features); G3 scans all 30,310.
3. G3 uses the normal-approximation Mann-Whitney (no tie correction) for the 30k-feature scan.
4. Memory amendment (locked 11:48 IST, after two OOM-killed runs that produced no output):
   the function view uses the top K=2000 COGs by mean relative abundance computed on the
   TRAINING fold only (label-blind, recomputed per LOCO fold). Combined = genus + the same
   2000 COGs. K was fixed before any result and not tuned.

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | function - taxonomy mean LOCO AUC >= 0.03, boot95 CI excludes 0 | -0.127, CI [-0.196, -0.059] | **FAIL** (significantly worse) |
| G2 | combined - best single >= 0.02 | -0.037 (combined 0.793 vs taxonomy 0.830) | **FAIL** |
| G3 | >=10 COGs FDR<0.05 in >=3 cohorts | 293 COGs | **PASS** |

Mean LOCO AUC: taxonomy 0.830, function 0.703, combined 0.793.

| held-out cohort | taxonomy | function | combined |
|---|---|---|---|
| AT-Wirbel | 0.813 | 0.740 | 0.782 |
| CN-Feng | 0.931 | 0.684 | 0.784 |
| CN-Yu | 0.861 | 0.651 | 0.827 |
| DE-Wirbel | 0.841 | 0.775 | 0.824 |
| IT1-Thomas | 0.728 | 0.593 | 0.714 |
| IT2-Thomas | 0.857 | 0.586 | 0.809 |
| JP-Yachida | 0.862 | 0.831 | 0.869 |
| US-Vogtmann | 0.746 | 0.764 | 0.738 |

The taxonomy LOCO mean (0.830, gradient boosting) reproduces P01-01's Random Forest figure
(0.832), which is a useful cross-check on the frozen benchmark.

## What the result means
1. **Function does not out-transport taxonomy here.** Function-only models lose in 7 of 8
   held-out cohorts (only US-Vogtmann is slightly better), and adding function to genera
   dilutes rather than helps. For the parent project, genus-level features remain the better
   portable signal.
2. **Function signal is real and replicable, just not as predictive.** 293 COGs are
   CRC-associated at FDR<0.05 in 3+ cohorts, so the null on G1 is not "function carries no
   CRC signal" - it is "a 2000-COG boosted model transports worse than 164 genera."
3. **Caveats that limit the claim.** (a) COGs are a gene-family proxy, not the pathway-level
   (MetaCyc) function the spec named; pathway aggregation could behave differently. (b) The
   K=2000 cap (memory) means the function model never saw 92% of the prevalent COGs; the top
   2000 by abundance are mostly housekeeping families, which may carry less disease signal than
   rarer ones. (c) The high-dimensional function view gives the booster many more noisy features
   (~2000 vs 164) at n=767. These are reasons to test further, not reasons to reinterpret this
   locked result.

## What this build needs next
- Pathway-level rerun (HUMAnN3 on raw reads, or cMD pathway tables via R) with gates unchanged.
- A pre-registered supervised-free feature reduction (e.g., COG -> KEGG module aggregation) on
  a machine with more memory, so function can use all COGs without an abundance cap.
- Use the 293 replicated COGs as a candidate list for P01-05 (minimal qPCR panel), noting they
  failed as a whole-model feature set.
