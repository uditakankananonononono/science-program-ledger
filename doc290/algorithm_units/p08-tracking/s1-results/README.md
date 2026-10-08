# S1 frozen synthetic comparison results

Scoring followed published p08-s1-freeze tip 04cc131a3a75a2c65f588528da686f44cc49098c,
with frozen protocol/harness 619ad01d408c09b2c81db5d88cd3fdf483b78bda ancestor.
Live git ls-remote confirmed branch tip before execution. No post-freeze code changes.
60 rows: seeds 1000-1019, 80 times each, three regimes. Raw metrics, secondary
NEES/velocity RMSE and observation counts retained in raw.json. No failed seeds.

Mean trajectory position RMSE (arbitrary simulation units):

| Regime | Position hold | Causal Kalman | Offline RTS |
| --- | ---: | ---: | ---: |
| low | 0.135186 | 0.096135 | 0.055842 |
| noisy | 1.351857 | 0.594143 | 0.315743 |
| occluded | 1.432627 | 0.814467 | 0.447875 |

For each regime, all 20 Kalman-minus-hold and 20 offline-RTS-minus-Kalman
per-trajectory position RMSE differences were negative; none were zero or positive.
This is descriptive for this locked simulation, not a winner rule or inference.

The model/prior/process are matched, q/R are known, and hold has no velocity model.
These choices favor the Gaussian baselines. RTS has future data, so it is not a
causal controller comparator. No imaging calibration, scientific gate, innovation,
physiology claim or stable superiority established. Independent result review pending.

First launch failed before scoring due to absent /usr/bin/time. Harness subsequently
executed unchanged once via runpy; Python stdlib timer/resource measured 1.463 seconds
and process peak RSS 37316 KiB (Linux). Single-thread BLAS; no training/GPU/download.
Full run hashes/environment in run-receipt.json and raw.json, not rounded table values.
