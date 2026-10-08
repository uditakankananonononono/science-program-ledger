# D1 synthetic battery one-shot results

Published executable/manifest freeze 63c10afc2d997aeb6ad453de81bc70f485bd2455,
then one full battery run. No rule/code/sequence changes or tuning after freeze.
All ten rows and step records retained in raw.json; env/hashes in summary.json.

Outcomes: 6 success, 4 terminal_miss, no boundary exit/invalid action/exception.
Proportional: one success (observation block), four terminal misses INCLUDING the
reference. Sign: all five successes. All max visited-state overshoots zero.
The proportional reference final error is ~0.12158, above the locked 0.1 terminal
threshold after 20 steps. This is finite-horizon/gain behavior of an untuned baseline,
not a failure caused by physiological disturbances. Observation block actually
improves its terminal result via stale-error hold sustaining control. That negative
interpretation remains: success does not show better tracking or biological benefit.
No policy failed every scenario and no disturbance makes all policies fail. Do not
increase magnitudes/horizon/gain/threshold to force desired atlas conclusions.

Effort differs by policy/case; action bounds and observations are shared, not equal
energy or information bits. Sign consumes greater absolute action effort in several
stress cases. Both are simple fixed baseline forms, not optimized classes or novel
algorithms. No ranking of physiological robustness or four-controller atlas claim.

Trusted-policy disclosure: timeout kills the direct policy child only, not a process
group. Trusted frozen baselines spawn no child processes. No hostile-sandbox or hard
per-call deadline claim; Pipe.poll/recv/serialization edges lack independent wall
bounds. Parent startup/OS scheduling not covered by total runtime guarantee.

This is constructed deterministic development sensitivity, not held-out validation,
CIs, physiological calibration or independent experimental evidence. Source magnitudes
remain unadmitted. Original P08-06 scientific gates OPEN, including physiological
four-disturbance/four-controller comparisons. No lack-of-failure defect inferred.
