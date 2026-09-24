# DOC-1-031F: Family-Aware AMP Model — REPORT (complete 2026-09-24 12:05 IST)

Follow-up to DOC-1-031 (boundary: homology-leakage-dominated AMP benchmarks; 3-mer logistic
dev MCC 0.954 but frozen DRAMP MCC 0.380). Parent-approved mechanism-targeted follow-up
(2026-09-24 10:59): explicit Cys/cationic motif features + per-family calibration, frozen on
the family-disjoint split. Fresh gates locked pre-scoring (GATES.md, commit 9e97207e).
**Outcome: DOCUMENTED BOUNDARY.** Neither mechanism-targeted fix repairs family-disjoint
generalization; 031's leakage finding stands and is now mechanism-explained at stratum level.

## Data (hash-verified vs 031 manifest)
- TRAIN: AmPEP 3,268 AMP + 166,182 non-AMP (Macrel build-AMP-table.py rule: AMPs written
  first, non-AMPs skipped if sequence already seen = AMP dupes + internal dupes removed;
  verified against the Macrel source 2026-09-24). 031's REPORT printed 166,170; the exact-rule
  rebuild gives 166,182 (delta 12 rows = 0.007%; same-draw ARM B control anchors all claims).
- DEV: iAMP-2L Supp-S2, 920 AMP + 920 NAMP (hash-identical to 031).
- FROZEN: 031's pinned 2,068 DRAMP positives (reused exactly) + 2,068 rebuilt negatives
  (locked redraw: UniProt reviewed proteins len 8-200, seed-42 pick of 8,000, segment
  length-matched 1:1 per positive, iterative redraw until decontaminated at pident>=80 &
  qcovs>=80 BLASTP-short vs all 2,068 positives + 3,268 train AMPs + 920 dev AMPs).
- Families: 2,464 single-linkage clusters over train AMPs (BLASTP-short pident>=80 &
  qcovs>=80); 2,232 singletons, largest 96.

## Protocol note
Optimizer: minibatch Adam (L2 logistic), weight-decay first set 1e-4 which underfit vs
031's liblinear C=1.0 anchor (dev 0.864 at epoch 25); matched to the documented protocol
scale (wd 3e-6 ~= liblinear C=1.0 per-sample) BEFORE any frozen scoring; both arms then
trained under the identical optimizer. ARM B-control final dev MCC 0.938 vs 031's 0.954
(residual optimizer delta, disclosed; frozen comparisons are same-draw). ARM C warm-started
from ARM B's weights (shared 8,000-feature block, motif block zero-init) — same objective.

## Gate results (frozen = 2,068 pos + 2,068 neg)
| Gate | Bar | Result | Verdict |
|---|---|---|---|
| G1 sanity | ARM C dev MCC >= 0.904 | 0.946 (B-control dev 0.938) | PASS |
| G2 claim | ARM C frozen >= 0.47 AND >= B-control + 0.05 | 0.391 vs B-control 0.380 (+0.011) | FAIL both clauses |
| G3 mechanism | ARM D >= ARM C + 0.02 | 0.3914 vs 0.3910 (+0.0004) | FAIL |

Per locked failure tree: G2 fail -> DOCUMENTED BOUNDARY, no further rescue pre-registered.

## G4 mechanism (the useful part)
Coverage-aware strata of the 2,068 frozen positives (max-pident-unfiltered strata are
meaningless: evalue-1000 BLASTP-short returns ~4-aa exact-match HSPs at pident 100 for
2,065/2,068 sequences):
- Homolog stratum (pident>=80 & qcovs>=80 to a train AMP; n=225, 10.9%): TPR 0.653 (B)
  -> 0.720 (C) -> 0.724 (D). BOTH fixes act here.
- No-homolog stratum (n=1,843): TPR 0.269 (B) -> 0.294 (C) -> 0.294 (D).
  Family calibration cannot act (no family to calibrate against); motif features add 2.5pts.
Findings: (1) even 031's "family-disjoint" frozen set retains 10.9% train homologs
detectable by BLASTP-short — stricter short-peptide homology detection than 031's prune;
(2) the generalization gap lives in the no-homolog stratum and neither canonical motif
features nor family calibration repair it; (3) ARM C motif coefficients match the canonical
expectation (largest positives: net charge/len +1.30, Cys-rich-3mer density +0.59,
Cys fraction +0.59, cationic-3mer density +0.33; largest negatives: Gly fraction -0.84,
disulfide CXXC -0.48) — the model learned the right biology; the biology just does not
transfer across families.
- Negative-set redraw sensitivity: all frozen claims are same-draw (B-control re-trained and
  re-scored on the rebuilt negatives); cross-draw anchor 031 ARM B 0.3798 vs this draw 0.3800.

## Deliverables
- tools/amp_predict_family.py (ARM C inference; boundary disclosed in header)
- results/amp_model_family.npz (8,014-dim ARM C weights)
- results/scores031F.json (all gate numbers, strata, coefficients)
- GATES.md (locked pre-scoring), PROVENANCE.md

## Prospective lab nomination (locked)
An AMP wet-lab screening unit (MIC assays vs ESKAPE panels) running a FAMILY-BALANCED
prospective panel: deliberately include no-homolog-stratum candidates (families absent from
public training corpora), where every sequence model is weakest (TPR 0.29), alongside
homolog-stratum controls (TPR 0.72). A prospective MIC panel on that split directly tests
whether current AMP classifiers have any real predictive value beyond homology retrieval.
