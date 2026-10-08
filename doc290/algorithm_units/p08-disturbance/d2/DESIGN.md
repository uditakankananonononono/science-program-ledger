# D2 paired estimator/control design, before executable freeze

D1 is untouched: its plant, policies, manifest and results remain frozen at reviewed
f938957be88db7a2378c5cf55b8b6461c5d14cbd. D2 will copy the D1 five sequence
arrays verbatim with hash verification and implement a separate instrumented runner.
Dimensionless synthetic development only, no physiological/atlas/novelty claim.
No full D2 battery execution before executable+manifest review and publication.

## Pairing and timing

Four established-form variants: hold-proportional, predict-proportional, hold-sign,
predict-sign. Hold retains latest observed position, initialized to zero. Prediction
retains nominal position estimate, initialized to zero. At step k:
1. Receive exactly D1 observation x_k or None, target, dt and action bound.
2. When observed, set estimate to observation. Otherwise hold uses its retained last
observation; prediction uses estimate propagated after previous action.
3. Return estimate_used and action computed from that estimate, with D1 gain-1
saturated proportional or saturated sign rule. Observation correction occurs before
both action and estimation-error measurement.
4. Prediction stores estimate_used+dt*action for the next call under known nominal
integrator gain=1/drift=0/no immobilization. Hold stores estimate_used unchanged.
Policies never receive actual gain/drift/immobilization, future observations, true
state during dropout, or target error derived from hidden state. Honest trusted
policies only, not hostile-code isolation. Four variants are not four distinct
physiologically anchored published controller classes.

## Identical comparison conditions

D1 x0=0, target=1, dt=1/10, 20 steps, bound=1, boundary [-1/2,3/2] and terminal
absolute-error tolerance 1/10. Same reference, alternating drift, reduced actuation,
immobilization block and observation block arrays. No tuning of sequence/policy/gain
or outcome threshold. Terminal/failure precedence and effort remain D1 rules. No
seeds/CIs: 20 deterministic constructed rows (five cases x four variants). Baseline
hold variants must replay D1 action/state/outcome/effort traces exactly before a D2
scoring run is admitted, using fixtures/reviewer checks without rerunning full D1
battery as hidden development tuning.

## Pinned additions for the executable freeze

Return contract is exactly (estimate_used, action), both Fraction/int only, excluding
bool/float/nonfinite values. estimate_used is unrestricted in magnitude but finite by
exact-domain construction; action bound enforced as D1. Invalid estimate or action
is invalid_action with separate identifier, no plant transition/effort contribution.
Controller exception/timeout similarly halts and retains observation/pre-step state.
One-second reset/action parent poll timeout mechanism as D1: direct child killed;
no process-group kill, hard per-call deadline or independent recv/serialization wall
bound. Parent startup/OS scheduling not a total runtime guarantee.

Record signed estimation_error=estimate_used-x_k, absolute error, and square at each
valid return before plant transition, including a valid returned estimate on an
out-of-bound action (annotated failed action). Invalid estimates/exceptions have None
errors, not zero; record valid_estimate_count separately. Report mean absolute error
and mean squared error over valid estimates, None if count zero. No square-root RMSE
needed, keep exact rationals. Separate missing_observation_count and dropout-only
MAE/MSE/count, None if no valid dropout estimate. Thus observed-step zeros cannot hide
dropout-only behavior. No unavailable truth in this fully synthetic plant.

Maximum boundary overshoot over visited states including initial; final error from
last completed state; effort over completed transitions including immobilized steps.
Retain all attempted steps, flags, raw exact estimates/actions and typed outcomes.
All 20 rows reported plus within-case prediction-minus-hold terminal error, effort,
and all-step/dropout MAE/MSE for each action rule. Loss/tie/win signs defined explicitly
in executable manifest: lower error preferred; effort is descriptive, not equal budget
or safety. No preselected winner. No altering hypotheses when prediction misses under
unmodeled drift/gain/immobilization. Observation-block success need not be improvement
in estimator accuracy, and predicted position need not equal physical truth.

## Admission tests before scoring

Literal observed/dropout estimate-action timing; independent trace formula fixtures;
hold/P and hold/sign equivalence to published D1 fixtures; nominal exact prediction;
misspecified drift/gain/immobilization divergence fixtures; identical observed prefixes
with varying hidden future -> same estimate/action; policy reset; return-domain/bounds;
valid-estimate counts/None and dropout metrics; exception/timeout early metrics.
Development fixtures kept distinct from full manifest. Design admission alone is not
scoring admission. Any changed contract disclosed before executable refreeze.
