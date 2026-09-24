# DOC-1-002F: Replogle-Scale Perturb-seq Retry — GATES (locked 2026-09-24 12:26 IST, before any scoring)

Follow-up to DOC-1-002 (DOCUMENTED BOUNDARY: across 3 Perturb-seq/CROP-seq datasets and 5
locked gate versions, per-target mRNA pseudobulk effects of TF knockouts are not separable
from size-matched sampling noise at available cell counts; CRISPR-KO target mRNA invisible
in 26/27 cases; WRITEUP flagged the named repair: Replogle-scale retry with an
n-vs-full-reference null replacing the conservative n=100 null). Parent queue 10:59
(eligibility-conditional); eligibility verified and reported 12:22; sketch approved 12:22:30
with two adjustments (G1/G2 thresholds locked numerically). 008->METENG pattern: fresh
experiment, fresh gates — this REPAIRS the falsifiability boundary at adequate scale, it is
not a retry of any 002 gate.

## Eligibility findings (locked as facts, verified from the file 12:19-12:23)
- DATASET: ReplogleWeissman2022_K562_essential.h5ad, scPerturb Zenodo record 7041849,
  1,546,729,675 bytes, md5 d8cba17576d1a8afc0f7d71b79cad0f7 (verified against the record).
  K562 CRISPRi essential-scale Perturb-seq, day 6/7 post-transduction (20Q1 DepMap common
  essential targets).
- 310,385 cells x 8,563 genes. X dense float32, chunked (1213x67) + gzip: streams at
  ~10,000 rows / 1.5s (~342MB/block); 5,000-row blocks used for RAM margin (envelope 1.9GB).
- Controls: exactly 10,691 cells (obs.perturbation == 'control').
- Targets: 2,057 non-control perturbations. G1 pool: exactly 1,299 targets with >=100 cells.
  G2 pool: exactly 1,164 targets with >=100 cells AND own mRNA in the 8,563-gene matrix.
- On-target visibility: 1,866/2,058 targets (90.7%) have own mRNA in-matrix — CRISPRi
  represses at the TSS, so 002's KO invisibility failure mode does not apply.
- gwps genome-scale file (8.8GB) not needed; essential scale tests the repair within envelope.

## Protocol (all mechanics locked here; rng seed 20260924 throughout)
- Normalization (identical to 002-v5): N = log1p(counts * 1e4 / library_size).
- Selected gene set S: top-500 genes by control-cell variance UNION all G1-pool target genes
  present in the matrix (identical selection rule to v5).
- Target DE: for each target t, draw n=100 of its cells without replacement (seeded);
  DE_t = mean(N[cells_t]) - mean(N[ALL 10,691 control cells]);
  statistic ss_t = sum over g in S of DE_t[g]^2.
- NULL (the named repair, locked): 200 draws; draw k = 100 random control cells vs ALL
  remaining controls; ss_k = sum over g in S of (mean(N[draw_k]) - mean(N[controls\draw_k]))^2.
  q95 = 95th percentile of {ss_k}. v5's null was 100v100 disjoint splits (both arms n=100,
  double sampling variance = conservative); the full-reference null removes the reference-arm
  variance — this IS the repair, locked pre-scoring.
- PASS_t iff ss_t > q95.

## Gates
- G1 (falsifiability repair): >= 650 of the 1,299 G1-pool targets (>=50.0%) PASS. v5 scored
  0/10 under the conservative null at TF scale; the bar is locked numerically.
- G2 (assay QC): for each of the 1,164 G2-pool targets: d_t = mean(N[cells_t, own gene]) -
  mean(N[all controls, own gene]); null d_k from the same 200 control draws on the own-gene
  column; REPRESSED iff d_t < 5th percentile of {d_k}. Bar: >= 698 of 1,164 (>=60.0%)
  repressed (CRISPRi expectation; v5's effective rate was ~4%).
- G3 (the original 002 question, run only if G1 passes with >=5 eligible panel members):
  panel = up to 20 G1-passing targets ranked by ss_t that are themselves in S's top-500
  control-variance set (network nodes). Control-cell correlation network C over S-top500.
  Per panel target t: predictor pred = C[t,.] * DE_t[own gene]; observed = DE_t over
  S-top500; baselines: (i) mean DE of other panel members; (ii) permutation null p over
  other panel members' predictors (as v5). Metrics: Pearson r_net vs r_base; top-20 |DE|
  overlap. Bar: median r_net >= median r_base + 0.10 AND >= half of panel targets with
  permutation p <= 0.05.
- G4 (deliverables): tools/grn_perturb_predict.py + REPORT.md + prospective nomination.
- Failure tree: G1 fail -> boundary STANDS at Replogle-essential scale (power/null no longer
  the explanation; that negative at adequate power is itself the report). G1 pass + G2 fail
  -> assay/label incoherence, halt to parent. G1+G2 pass + G3 fail -> falsifiability repaired,
  network-from-controls still unpredictive: the 002 question answered negatively at adequate
  power (a real answer; parent adjudicates counting).
