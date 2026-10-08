# D3 final synthetic factorial one-shot results

Unchanged published a20b9cfadc306a17aaa30928159dbe69b6318143 then sole full run.
All 32 rows/16 pairs/640 transitions retained. Env/hashes in summary.json. No tuning,
code/rule/sequence changes, discarded cases, novel or physical claims. Chronology
supported by our push/readback log, not independently established by replay alone.

Hold-P:7 misses/1 success. Predict-P:8 misses/0 success. Both sign variants:8 successes.
No boundary exit/invalid action/exception. All complete; all paired counts match.
Prediction-minus-hold terminal error:0 lower/13 ties/3 higher. Effort:4 lower/12 ties.
All-step MAE/MSE:5 lower/9 ties/2 higher. Dropout-only MAE/MSE:8 comparable pairs,
5 lower/1 tie/2 higher;8 noncomparable no-dropout pairs, NOT zero/ties.

Nominal/dropout P repeats D2 success-to-miss tradeoff; alternating drift and reduced
actuation with dropout also worsen P final error while improving estimate MAE/MSE.
Immobilization with dropout makes prediction estimates WORSE for both P and sign:
hold estimate remains exact while nominal model predicts movement that does not occur.
Sign immobilization/dropout MAE increases by 1/10 and P by 206284401/5000000000.
Terminal results remain tied for these immobilization pairs; estimation accuracy and
terminal task success are separate. No robust estimator or physiological winner claim.
No all-controller failure found, no lack-of-failure defect, no tuning to force it.

Closed-loop trajectories differ; pairing shares exogenous sequences/availability.
Fixed dimensionless sequences cover this toy missing-observation x hidden-plant gap,
not calibrated disturbance distributions, physical safety or four controller classes.
Source magnitudes/data rights remain unadmitted, science gates open. Pins trusted-local,
not hostile edit authenticity; check/import TOCTOU not concurrent-files defense.
Trusted direct-child poll only, recv/serialization/OS not independent wall-bound;
no hard deadline or sandbox guarantee. Final synthetic extension complete numerically;
closeout after independent review/publication, no further toy extension proposed.
