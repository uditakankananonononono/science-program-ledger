# P13-08 Deviation Detector (BatchSentinel) - Build Report

**Built:** 2026-09-24 | **Status:** 1 of 3 evaluable gates pass. G1 FAIL: the locked ensemble detects 8/10 faulted batches (needs 9). G2 PASS: median lead 0.35 of batch duration, with a weak manifestation proxy disclosed. G3 is a pre-declared data boundary.

Parent: CBIO042 ReinforCell (manufacturing module). Real public data: IndPenSim V3 (Mendeley doi:10.17632/pdnjz7zz5x), 100 simulated 100,000 L penicillin batches, 10 with labeled faults.
Protocol locked and pushed before any model was trained (commit cd734d3a, `PROTOCOL.md`).

## Gates (locked before evaluation, evaluated once)

| gate | criterion | observed (primary ensemble) | verdict |
|------|-----------|----------|---------|
| G1 | >= 90% detection at <= 1 false alarm/batch | 80% detection (8/10), 0.125 false alarms/batch | FAIL |
| G2 | median lead >= 20% of batch before manifestation | 0.346 | PASS (proxy caveat below) |
| G3 | mammalian transfer >= 70% detection, <= 2x FA inflation, or gap quantified | no public mammalian online-sensor dataset with labeled deviations | DATA BOUNDARY (pre-declared) |
| G4 | honest-negative clause | the G1 miss is a characterised boundary (below) | recorded |

## Results
| detector | threshold | FA/batch (cal) | FA/batch (30 test nominals) | FA/batch (all, incl. pre-onset) | detection (10 faulted) | median lead (frac of batch) |
|---|---|---|---|---|---|---|
| ensemble (PRIMARY, locked) | 0.9986 | 0.40 | 0.17 | 0.125 | 80% | 0.346 |
| phase-aligned z (secondary) | 3.699 | 0.47 | 0.33 | 0.250 | 100% | 0.390 |
| isolation forest (secondary) | 0.5777 | 0.47 | 0.27 | 0.250 | 60% | 0.176 |
| dense autoencoder (secondary) | 8.592 | 0.47 | 0.33 | 0.250 | 100% | 0.390 |

| batch | fault window (h) | detected | first alarm (h) | delay (h) | P manifestation (h) | observed? | lead frac |
|---|---|---|---|---|---|---|---|
| 91 | 20-214 | yes | 20.6 | 0.6 | 20 | yes | -0.002 |
| 92 | 80-160 | yes | 150.4 | 70.4 | 230 | no (batch end) | 0.346 |
| 93 | 70-90 | NO | - | - | 210 | no (batch end) | - |
| 94 | 20-110 | yes | 20.6 | 0.6 | 112 | yes | 0.398 |
| 95 | 20-211 | yes | 20.6 | 0.6 | 20 | yes | -0.003 |
| 96 | 70-90 | NO | - | - | 230 | no (batch end) | - |
| 97 | 20-214 | yes | 20.6 | 0.6 | 20 | yes | -0.003 |
| 98 | 80-160 | yes | 150.4 | 70.4 | 230 | no (batch end) | 0.346 |
| 99 | 20-110 | yes | 20.6 | 0.6 | 116 | yes | 0.380 |
| 100 | 20-110 | yes | 20.6 | 0.6 | 106 | yes | 0.372 |

## Findings

1. **The two short faults are the blind spot.** The ensemble catches every long-window fault within 0.6 h of onset (91, 94, 95, 97, 99, 100). It misses both 20-hour faults (93 and 96, window 70-90 h). It catches the 80-160 h faults (92 and 98) only 70 h late. Short, mid-batch faults that stay inside the process's own control action are where detection fails.
2. **Ensembling hurt.** Rank-normalising three detectors and taking the max raises the calibrated threshold. That cost exactly the two short faults. Secondary result, not a re-fished gate: the phase-aligned z model and the dense autoencoder *alone* detect 10/10 at 0.25 false alarms/batch, which would clear G1 as written. The simplest detector matches the best. The locked verdict stays FAIL.
3. **False alarms are low.** 0.17 alarms per clean test batch, and no pre-onset alarms on any faulted batch. The alarm rule is 3 consecutive samples above threshold, calibrated on 15 separate nominal batches.

## Honest limits
- **G2 proxy is weak.** "Manifestation" was locked as penicillin leaving its nominal +/-3 sd band. For batches 91, 95 and 97 this fires at onset, because early-batch P variance is tiny, so their lead is ~0. For 92, 93, 96 and 98, P never leaves the band, so batch end is used, which inflates lead. The 0.35 median is real under the locked rule, but the rule is a coarse stand-in for "failed batch".
- Dense autoencoder instead of the spec's LSTM autoencoder (no torch in the sandbox). Disclosed in the protocol before results.
- Only 10 faulted batches exist, so detection-rate CIs are wide: 8/10 is compatible with anything from ~50% to ~97%.
- IndPenSim is a microbial simulation. Nothing here tests mammalian or cell-therapy physics. That is exactly the question G3 was meant to answer, and there's no open data for it.

## G3 data boundary (what facilities would need to publish)
The bounded search covered the web, the NIST CHO feeding-strategy repo (csbg/DGTX_feeding_strategies_nistcho: daily offline assays only) and the Kamen Lab Borealis repository. It found no mammalian or cell-therapy dataset with multi-run online sensor streams (DO, pH, temperature, gas flows, feeds at sub-hour resolution) plus labeled deviations. The spec's pivot is follow-on work: an IndPenSim-style synthetic cell-therapy benchmark with realism tests against published summary statistics.

## Artifacts
- `PROTOCOL.md`
- `tool/load.py`: position-safe IndPenSim loader.
- `tool/sentinel.py`: all three detectors, the ensemble, calibration and gate evaluation. Re-run it against any historical batch table with the same columns.
- `results/results.json`: split, thresholds, and per-batch alarms, delays and leads for every detector.
- `SHA256SUMS`

## What a reviewer asks next
Fault-type-specific detectors for short excursions (CUSUM on control-action residuals). A better manifestation definition, such as final-yield loss. A torch LSTM autoencoder for comparison. And the synthetic cell-therapy benchmark, so G3 can be tested at all.
