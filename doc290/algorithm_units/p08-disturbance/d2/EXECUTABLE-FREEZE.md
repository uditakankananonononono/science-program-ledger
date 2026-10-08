# D2 executable candidate before full battery

Implements design 50005ae94baa6210e31d82132b12c456a74cb032. D1 files unchanged.
Manifest binds D1 manifest SHA256 and exact case-array equality, four variants x
five cases. No full battery executed yet. Two action forms x two estimator variants,
not four physiological controller classes. Closed-loop pairing means same exogenous
sequence and observation availability, not same realized observations: controls
change plant trajectories. Actual truth/errors computed parent-only, never in calls.

Return exactly tuple(estimate,action), both int/Fraction excluding bool/float. Valid
estimates contribute diagnostic error even on invalid action; invalid estimates,
exceptions/timeouts get None diagnostic fields. All/valid-dropout counts retained.
Zero valid count yields None MAE/MSE, not zero. Missing-observation count is attempted
steps only; reset failure zero. Pair differences prediction minus hold only when
both completed full horizon with terminal outcome, both values exist and estimate
counts match. Otherwise comparable=false, difference=None, counts retained. Missing
pairs not ties. Error negative/zero/positive means lower/equal/higher error; effort
negative/zero/positive describes less/equal/more effort, not an efficacy winner.
No early exception/invalid/boundary exit can win by a short MAE average.

Exact integrator prediction uses only own action and known nominal dt/gain1/drift0.
Each observed position replaces predicted estimate before action. Hold ignores own
actuation during dropout. No known hidden drift/gain/immobilization policy access.

Eight development methods pass: literal timing, short D1 hold replay fixture, causal
hidden-world variations, misspecification, reset, invalid/None/count rules, no-dropout
nonpair, exception and never-return timeout. Short fixtures only, not full manifest.
Previous D1 boundary/immobilization/domain fixtures are not independently rerun for
D2 instrumented runner; independent executable review required before scoring.

Trusted-policy timeout disclosure: one-second parent poll for reset/action, direct
child kill only, no process group kill. Pipe.poll/recv/serialization edges have no
independent wall bounds, no hard deadline or hostile sandbox. OS/startup not bounded.
No tuning of D1 or full-battery outcomes, measured data, CIs, calibration, novel or
physical robustness claims. Science gates OPEN. Freeze/publish before compare.py.
