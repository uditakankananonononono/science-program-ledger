# DOC-1-020F: CRISPR Outcome Modeling on Clean Data — GATES (locked 2026-09-24 12:46 IST, before any scoring)

Follow-up to DOC-1-020 (boundary: outcome-complexity models transport across cell types on
the same library (0.657) but NOT across library designs (0.279 < Bae 0.336); confounds
flagged: mirror-data label history, readcount-vs-complexity, single-publication frozen sets).
Parent-approved sketch 12:43:56 (fresh gates, 008->METENG pattern; re-tests the transport
question on clean independent data, NOT a retry of 020's failed T3 gate). Parent's numeric
locks: depth floor, G1 margin, G2 bar, split rule — all numeric below. If G0 halts: report,
do not patch (parent rule 12:43:56).

## Data (eligibility verified 12:43, grounded)
- DEV: Leenay et al. 2019 Nat Biotechnol primary-human-T-cell repair outcomes, figshare
  6957125, LeenayIndelCounts.tar.gz (7,842,905 bytes; 1,986 per-site count files;
  variant-class rows x guide columns; published CrispRVariants pipeline). Downloaded +
  inspected 12:43.
- FROZEN: Allen et al. 2019 Nat Biotechnol (FORECasT) K562 collated pre-processed indel
  profiles, figshare 7312067 (third independent source; cross-cell-type = the regime 020
  showed transports).
- Label: outcome complexity = count of unique observed indel classes per guide (020's exact
  label family); precision (dominant-outcome fraction) as secondary descriptor.

## Locked mechanics (all numeric per parent 12:43:56)
- DEPTH FLOOR: a guide enters analysis iff total reads summed over its replicate columns
  >= 10,000 (both datasets). Pass rates disclosed in REPORT before gate verdicts.
- LABEL AUDIT (G0, pre-lock execution, reported before any modeling): (i) parse audit -
  strand/orientation/no-variant handling consistent across all files, zero unparsed variant
  classes; (ii) depth-floor pass rate reported; (iii) Spearman(complexity, log10 depth)
  computed and disclosed; if labels show corruption (parse failures, orientation
  inconsistencies, or complexity-depth rho > 0.8 after the floor) -> HALT, report to parent,
  no patching.
- SPLIT: guide-disjoint 5-fold CV on dev, seed 7 (mirrors 020's dev protocol); folds
  contain disjoint guide sets; no guide appears in two folds.
- FEATURES: 020's exact executed arm — 55nt local context (cut at 27|28), ridge features as
  020 (dinucleotide composition, GC, MH-derived: Bae MH score, MH pattern count, MH max
  length, etc. per 020's code) + Bae 2014 MH score as the NAMED PUBLISHED BASELINE.
  Guide context sequences recovered from the datasets' own references (Leenay contig/plate
  maps; Allen target table); any guide whose 55nt context is unrecoverable is dropped and
  counted in REPORT before gate verdicts.
- MODEL: ridge regression (020's exact model class), fit on dev folds only; frozen pass is
  single-shot, fit on all dev.

## Gates
- G0 (label audit): as above; halt condition locked.
- G1 (dev): ridge 5-fold guide-disjoint CV Spearman >= 0.50 AND >= |Bae rho| + 0.20 on the
  same folds (mirrors 020's G1 form: 0.783 vs -0.328).
- G2 (frozen, Allen K562): single-pass Spearman >= 0.45 (020's U2OS bar, mirrored) AND
  >= Bae-score Spearman on the same frozen set. Both clauses required.
- G3 (mechanism): feature audit on clean data — does Bae MH score stay the #1 |coefficient|
  feature (020's G3 finding)? Does complexity-depth rho survive the floor (< 0.5)?
  Report vs literature (Bae 2014; Shen 2018; Allen 2019; Leenay 2019).
- G4: predict_precision.py (clean-data model) CLI + REPORT.md + prospective nomination.
- Failure tree: G0 halt -> report to parent (no patch). G1 fail -> incoherent vs 020's dev
  result on corrupted-data history; halt to parent. G2 fail -> the 020 library/cohort-design
  transport boundary stands on clean data (a STRENGTHENED boundary: not explainable by label
  corruption or depth confounds). G2 pass + G3 divergent -> report both; parent adjudicates.
