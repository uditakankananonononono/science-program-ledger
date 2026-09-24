# DOC-1-014F: Score-Guided AMP Design — REPORT (2026-09-24)

Follow-up to DOC-1-014 (boundary: unconditional 8M sampling never finds AMP order;
"needs conditioning or a search/guidance loop"). 014F tests the guidance loop with a
guide/judge separation to break circularity: Macrel guides, two independent published
predictors judge. Gates locked pre-scoring (b7f76994) + Addendum A (AMPlify published
cutoff 3.01 correction) + Addendum B (G1 re-locked to both-judges >= 0.80 after the G0
audit showed the original 3x bars mathematically impossible; parent ruling 13:27:25,
re-locked before the loop ran). VERDICT: G1 FAIL - guidance overfits the guide and
DEGRADES independent-judge AMP-likeness. A clean Goodhart result.

## Locked protocol (executed unchanged)
Seeds: 200 (rng seed 7) from 014's committed shuffled-AMP-composition pool. Loop: 30
iterations of uniform-random 15% re-masking + 014's exact ESM-2 t6_8M masked resampling
(top-p 0.95, temp 1.0, 3 progressive unmask rounds - disclosed refinement of "014's exact
decoding" for partial masks), greedy accept iff Macrel probability non-decreasing, rng
seed 7. Judges: amPEPpy 1.1.0 (p >= 0.5) and AMPlify balanced (published score > 3.01).

## Results (single locked run; results/*.json)
- G0 (judge calibration): amPEPpy 94.2%, AMPlify 97.4% recovery of 500 held-out APD AMPs.
  PASS (bars 30%). Seed rates: amPEPpy 0.825 / AMPlify 0.655 / both 0.575 - the shuffle
  composition baseline fools independent judges MORE than it fooled Macrel (10.2%).
  This is FINDINGS 15 (approved 13:27:25).
- G1 (headline, re-locked): final both-judges AMP+ rate 0.450 vs bar 0.80 (seed baseline
  0.575). FAIL - and directionally NEGATIVE: amPEPpy 0.825 -> 0.690, AMPlify 0.655 ->
  0.470, both 0.575 -> 0.450.
- G2 (novelty + envelope, 90 both-judge winners): 100% novel vs APD (zero MMseqs2 -s 7.5
  hits); median net charge +4.0 (bar >= +2), median hydrophobic ratio 0.423 (bar
  [0.30, 0.60]). PASS.
- G3 (mechanism): median Macrel gain +0.208 over 30 iterations; 179/200 trajectories
  improved; median last-improvement at iteration 15 (saturation). Judge deltas over the
  same trajectories: amPEPpy median -0.015, AMPlify -0.069. The loop climbed the guide
  hard while BOTH independent judges moved DOWN - guide overfitting in a closed loop,
  quantified per sequence.
- G4: code/amp_guided_design.py CLI (+ refine.py) with the Goodhart warning in its
  docstring; REPORT; nomination: judge-ensemble-guided design as a follow-up candidate
  (guide = judge intersection, not one model) for the queue.

## Interpretation vs literature
014 showed the 8M PLM cannot SAMPLE AMP order; 014F shows steering it with one published
scorer actively destroys independent-judge AMP-likeness while satisfying the guide, the
envelope (cationic-amphipathic medians in range), and novelty (100%). Three different
"success" readings - guide score, biophysical envelope, independent judges - diverge
completely. This is the Goodhart/closed-loop overfitting phenomenon (cf. surrogate-model
degradation in protein design, e.g. the Freschlin/Fahlberg discussion of oracle
overfitting) measured end-to-end with per-sequence trajectories. Design pipelines need
the guide to BE the judge ensemble, or held-out-judge early stopping.

## Failure-tree routing
G1 fail -> "guidance loop does not fix 014's boundary at 8M scale; document, parent
adjudicates (with judge-vs-guide divergence analysis from G3)." Documented; reported to
parent with full numbers.

## Honest limits
One seed set (n=200, seed 7); greedy accept is the simplest guidance (no beam/population);
judges are peptide-class predictors, not activity assays; AMPlify needed a tf-keras import
shim to run its published weights under current TF (architecture/weights untouched).
