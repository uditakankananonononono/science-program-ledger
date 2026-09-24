# DOC-1-035 — "Dark Matter" Protein Function Predictor with Genomic Context

## Verdict
**DOCUMENTED BOUNDARY** (locked failure tree exhausted: G2 fail → P1 fail → boundary).
The full 3-channel context model (ARM B) and label propagation (P1) both fail to beat
the 2000-era neighborhood-vote mechanistic baseline (ARM A) by the locked +5pp margin on
held-out long-lit dev — and on temporally frozen newly-lit proteins the ordering inverts:
ARM A 24.34% > ARM B 20.45%. Sixth instance of the program's dev→frozen inversion /
mechanistic-baseline-wins-out-of-domain pattern (026/027/030/032/033/035).

## Design (GATES.md locked pre-outcome; Addendum A locked before scoring)
- Temporal split on annotation provenance: long-lit = COG letter in both COG-2014 and
  COG-2020 (train/dev); frozen = newly-lit, no 2014 letter but a 2020 letter (independent
  cohort); dark = unlabeled in both.
- Label (Addendum A): PRIMARY (first) letter of COG functional code; dual-code COGs
  collapse to primary. Composite-label ARM A variant (24.66% dev) was discarded as
  label-inconsistent before any other arm was scored; all reported arms share one label.
- ARM A = executed Huynen 2000 Type-II transfer: weighted vote over STRING-v12
  neighborhood-channel (≥400 combined score) neighbors' 2014 primary letters.
- ARM B = multinomial logistic regression over 3 context channels (neighborhood, fusion,
  co-occurrence aggregate letter distributions) + AA composition; torch float32 batched,
  30 epochs, 100k subsample.
- P1 = 2-step label propagation (F' = 0.9·A_norm@F + 0.1·Y), held-out seeds masked.
- Bars: G1 ARM A dev within [popularity+5pp, 80%]; G2 ARM B ≥ ARM A + 5pp; P1 one
  pre-registered rescue ≥ ARM A + 5pp; frozen documentation-only.

## Cohorts
- Panel: 149/150 prokaryote genomes (taxid 1110502 dropped: 52.2% COG mapping < locked
  60% eligibility bar; documented in manifest035.json, committed pre-scoring).
- 511,522 proteins; 2,200,949 context edges (channels ≥400); cohorts: 324,998 long-lit /
  3,502 newly-lit (3,497 after the genome drop) / 186,586 dark.
- Bridge: exact-sequence md5 join STRING v12 ↔ COG-2020 (median 89.4% panel coverage);
  locus-tag joins across eras verified dead (eligibility finding, per program learning 10).

## Results (all 26-class accuracy, primary-letter labels)
| Gate | Result | Bar | Verdict |
|---|---|---|---|
| G1 ARM A dev | **27.76%** | [13.55% (=8.55%+5pp), 80%] | PASS |
| G2 ARM B dev | **32.22%** (10/10 fold wins) | ≥32.76% (ARM A+5pp) | FAIL (-0.54pp) |
| P1 label propagation dev | **28.32%** (10/10 folds ≥ ARM A) | ≥32.76% | FAIL (mean short) |
| Frozen newly-lit (doc) | ARM A **24.34%** > ARM B 20.45% > popularity 8.55% | — | 6th dev→frozen inversion |

## G4 interpretation
- Channel ablation (dev means): neighborhood-only LR 26.69% > fusion-only 23.35% >
  co-occurrence-only 19.04% — matches the Huynen 2000 hierarchy (gene order dominant).
- Provenance on newly-lit (ARM A): proteins WITH a fusion-channel link to a lit protein
  (7.7% coverage) score 33.58% vs 23.57% without (n=268) — fusion is highest-precision
  per Huynen. With a neighborhood link (79.7% coverage): 30.55%; with NO labeled
  neighborhood (n=711, 20% of newly-lit): 0.00% — context-isolated proteins are
  unreachable by vote; that is the honest coverage ceiling of the method.
- The +5pp gate asks a learned 3-channel model to beat the specific mechanism the data
  actually obeys; it cannot, and out-of-distribution it falls behind it. The boundary IS
  the finding: for sparse evolutionary-context prediction, the published mechanistic
  baseline is the right model class, and its coverage ceiling (context-isolation) is the
  real bottleneck, not model capacity.

## Tool (G5)
`tools/darkfunc_predict.py` + `darkfunc_assets.npz` (edges + 2014 letters, 10.8MB) +
`darkfunc_md5.npz` (8.2MB): ARM A voter as CLI. Input: protein FASTA from any of the 149
panel genomes; sequences matched by exact md5; output letter + neighborhood vote share,
NO_CALL when no labeled neighbor (by design — 24.3% frozen accuracy is
hypothesis-generating, not validated annotation). Smoke-tested: 38/40 calls.

## Limitations
Frozen accuracy 24.3% across 26 classes; popularity floor 8.55%. 20% of newly-lit
proteins are context-isolated (no ARM A call possible). Dual-code COGs force a primary-
letter collapse (Addendum A) that discards real multifunctionality. No sequence-only
fallback for genomes outside the panel.
