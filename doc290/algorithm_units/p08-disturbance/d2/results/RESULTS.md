# D2 one-shot synthetic causal estimator/control results

Published executable freeze 0422d8dd0e0da931291869c8fee1740859412cc5 then ran
sole full 20-row battery. No post-freeze code/sequence/threshold changes or tuning.
All 20 rows/10 pairs/400 transitions retained; env/hashes in summary.json.
D1 remains unchanged. Tool push/readback log supplies publication-before-run evidence.
Independent result review cannot establish that chronology solely by replaying data.

Hold-P: 4 misses/1 success; predict-P: 5 misses/0 success. Both sign variants 5 successes.
No boundary/invalid/exception. Prediction-minus-hold final error: 0 lower,9 ties,1 higher.
Effort:1 lower,9 ties,0 higher (descriptive, not efficacy/energy equality).
All-step MAE/MSE:2 lower,8 ties,0 higher. Dropout-only MAE/MSE:2 comparable pairs,
both lower;8 noncomparable because no dropout estimates, NOT zero/ties.
All rows complete 20 transitions; compared valid counts match.

Only observation-block case differs. Predict-P estimates exactly under the nominal
plant there, giving zero dropout error rather than hold-P MAE 0.19683. But predict-P
final error is higher by ~0.0300695, with equally lower action effort; it misses while
hold-P succeeds. This is the retained prediction-control tradeoff under gain-1 P and
fixed finite horizon, not a tracking-safety verdict or proof prediction is worse.
Predict-sign dropout error also zero vs hold-sign MAE 0.3, with same terminal/effort.
The drift/gain/immobilization cases have observations every step, so prediction resets
before action and this battery cannot assess unobserved misspecification robustness.
No claimed combination-disturbance benefit. Short misspecification development
fixtures are not scored held-out evidence.

Closed-loop paired sequences allow different trajectories/observed positions.
Exact estimates do not guarantee terminal success; stale errors can sustain actuation.
No physiological/atlas/novelty/CI/four-controller-class claim, source calibration open.
One-second poll kills trusted direct policy child only; no hostile sandbox/hard deadline,
process-group kill or independent recv/serialization wall bound. Attempted missing
counts and None handling retained. Manifest hash/case gate does not enforce every
plant constant at runtime; frozen supplied constants match reviewed design.
