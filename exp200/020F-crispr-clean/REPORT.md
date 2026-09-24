# DOC-1-020F: CRISPR Outcome Modeling on Clean Data — REPORT (2026-09-24)

Follow-up to DOC-1-020 (boundary: transport across cell types yes, across library designs
no; label-corruption confounds flagged). 020F re-tests on two clean, independent public
datasets with gates locked pre-scoring (GATES.md, commit 1dd0c417; parent lock instructions
12:43:56). Verdict: BOUNDARY — G1 and G2 both FAIL on clean data; 020's dev result is
incoherent with clean-data behavior. Per the locked failure tree (G1 fail -> halt to
parent), reported to parent for adjudication.

## Data & provenance
- DEV: Leenay et al. 2019 Nat Biotechnol (doi 10.1038/s41587-019-0203-2), figshare 6957125
  LeenayIndelCounts.tar.gz (7,842,905 bytes, 1,985 per-site count files parsed) +
  Leenay_bam_df.rds (guide->reference map). Primary human T cells, SpCas9, 2,472 guides.
- FROZEN: Allen et al. 2019 (FORECasT), figshare 7312067, K562_800x LV7A+LV7B DPI7
  (replicate batches summed per the locked "replicate columns" floor rule); wild-type
  contexts reconstructed per oligo from profile rows (insertion-row anchoring + deletion-row
  verification); label parse per felicityallen/SelfTarget indel.py semantics.
- Label: outcome complexity = # unique observed indel classes per guide (020's label family).

## G0 label audit (locked pre-modeling) — PASS, no halt
- Parse audit: 1,985/1,985 Leenay files parsed; 0 multi-guide files; 0 unmapped columns;
  487/2,472 guides lack count files (paper's amplicon filter) — dropped and counted.
- Orientation: 1,685/1,685 floor-passing references carry a single + strand NGG PAM at
  position 33 (cut boundary 30); zero inconsistencies.
- Depth floor (>=10,000 reads summed over replicates): DEV 1,685/1,985 pass (84.9%).
  FROZEN 56/16,052 reconstructed oligos pass (0.35%) — disclosed: the Allen K562 per-guide
  depth (median ~600 summed over both batches) almost never reaches the locked 10k floor;
  G2 is therefore a 56-guide estimate.
- Spearman(complexity, log10 depth) after floor: 0.387 (< 0.8 halt; < 0.5 G3 check).

## Gates (all scoring post-lock)
- G1 (dev, Leenay T-cell): ridge 5-fold guide-disjoint CV (seed 7) Spearman = 0.1956.
  Bar: >= 0.50 AND >= |Bae rho| + 0.20. Bae MH-score rho = -0.0814 -> margin bar 0.2814.
  FAIL on both clauses (0.196 < 0.50; 0.196 < 0.281). Contrast: 020 dev on inDelphi mESC
  was 0.783.
- G2 (frozen, Allen K562, single-pass, n=56): ridge Spearman = 0.3367 vs bar 0.45;
  Bae rho = -0.2118. Clause 1 FAIL (0.337 < 0.45); clause 2 (ridge >= Bae) passes.
  Both clauses required -> FAIL.
- G3 (mechanism audit): Bae MH score is NOT the #1 |coefficient| feature on clean data —
  the top 10 are all dinucleotide-composition terms (max |coef| 0.60); MH features absent
  from the top 10. 020's G3 finding (Bae MH #1, coef -0.19) does NOT replicate on clean
  T-cell data. Complexity-depth rho 0.387 survives the floor (< 0.5), so the weak
  predictability is not a depth artifact.
- G4: code/predict_precision.py CLI + model020F.pkl (ridge, n=1,685 Leenay guides) — this
  REPORT. Prospective nomination: Leenay-style primary-T-cell screen on a small NEW guide
  panel chosen to span the model's predicted-complexity range would directly test whether
  the T-cell signal ceiling (G1 rho ~0.2) is biological or assay noise.

## Interpretation vs literature
On clean data, 020's exact feature family predicts outcome complexity far worse in primary
T cells (0.196) than on inDelphi mESC (0.783), and the frozen K562 transport number
(0.337) sits BELOW 020's same-library U2OS transport (0.657) though above its T3
cross-library fail (0.279). The clean-data picture: sequence-determined outcome
complexity is largely a cell-type/assay-regime property, not a library-design property —
the opposite emphasis from 020's confounded read. Bae (2014) MH dominance does not survive
on clean T-cell data; Shen (2018) inDelphi-scale predictability does not transfer to
Leenay's T-cell assay; Allen (2019) K562 remains an easier regime than T cells.

## Failure-tree routing
G1 fail -> "incoherent vs 020's dev result on corrupted-data history; halt to parent."
Halted to parent with full numbers; no patching, no retries.
