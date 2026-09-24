# DOC-1-033F — Cold-Host Hybrid Exact-Signal Predictor — REPORT

## Verdict
Core claim PROVEN on the locked cold subset (G2 PASS); unified single-predictor extension
is a DOCUMENTED BOUNDARY (G3 fail, then HYBRID-2 G2' fail under Addendum A; locked failure
tree exhausted — no further rescue pre-registered). Useful result: two-output predictor.

## Cold subset (locked pre-scoring, recomputable)
72 of 615 evaluated test pairs whose host_species is absent from all 1,260 train labels
(32 species). Lineage: 033 GATES' "36 species" was computed on raw TEST671; the evaluated
615-pair set yields 32/72 (disclosed in GATES).

## Outcomes (all thresholds locked before the outcomes they govern)
| Gate | Bar | Result | Verdict |
|---|---|---|---|
| G1 premise | ARM A' cold <= 5% | **0.00%** (structural blindness verified) | PASS |
| G2 claim | HYBRID cold >= ARM A'+5pp = 5.00% | **36.11%** (26/72) | PASS |
| G3 no-free-lunch | HYBRID warm >= ARM A'-2pp = 65.03% | 48.80% vs ARM A' 67.03% | FAIL |
| G2' (Addendum A) | HYBRID-2 cold >= 5.00% | 0.00% (0/72 routed to CRISPR) | FAIL -> boundary |
| G3' (Addendum A) | HYBRID-2 warm >= 65.03% | 67.03% (= ARM A'; never routed) | n/a (degenerate) |

Harness: rebuilt KNN-d2 reproduces 033 ARM A 0.5919 vs 0.5935 reported (1 pair, tie-break).

## What is proven
1. **Exact signals name the unnameable.** CRISPR-spacer panel votes recover 26/72 (36.11%)
   cold hosts that KNN-d2 cannot name BY CONSTRUCTION (its output space is train labels).
   Among the 41/72 spacer-covered cold viruses, precision is **63.41% (26/41)**; even
   single-spacer hits are sometimes right (correct-call spacer counts: 1..230).
2. **Universal override is wrong.** The same spacer vote is strictly worse than a warm KNN
   vote (48.8% vs 67.0%) — documented failed direction (user pivot rule applied).
3. **The cold regime is undetectable from sequence.** Train panel has no cold-regime
   analogs (1239/1260 leave-one-out max cosine >= 0.95; 0 below 0.8), so train-CV tau
   selection is flat (0.7492 at every tau in [0.50, 0.95]) and selects tau=0.50, which
   routes 0/72 cold viruses. Cold test viruses are compositionally indistinguishable from
   warm (median maxsim 0.984 vs 0.997). k-mer similarity to train does not flag host-label
   novelty — HYBRID-2's regime gate cannot exist with these features. G2' fail, boundary.
4. Wrong-call taxonomy: 46 wrong cold calls under the locked hybrid; of the 15 wrong
   CRISPR votes, 8 are genus-correct (spacer hits a relative of the true host —
   strain-level mismatch dominates CRISPR error).

## Tool (G5)
`tools/cold_host_predict.py` + coldhost_assets.npz (1.2MB) + X_kmer.npy + virus_ids.json:
two-output predictor — KNN-d2 host vote (59.19% frozen) plus CRISPR ALERT channel
(63.4% precision among covered cold-regime viruses). Smoke-tested both channels.
Nomination (locked): phage-therapy group screening a patient isolate panel — CRISPR ALERT
is the high-precision hypothesis for spot assays when KNN-d2's vote is suspect.

## Boundary statement
Failed directions documented: (a) universal CRISPR-override destroys the warm regime;
(b) similarity-gated regime detection cannot work — no sequence-computable signal in this
feature space separates cold from warm. The useful result stands: the two-regime reality
(KNN-d2 where warm, CRISPR-alert where blind) with quantified precision on both sides.

## Reproduce
scores033F.json (locked-design), scores033F_h2.json (HYBRID-2), g4_033F.json (mechanism);
script in-repo tools/; all inputs inherited from 033's committed manifest (hash-pinned).
