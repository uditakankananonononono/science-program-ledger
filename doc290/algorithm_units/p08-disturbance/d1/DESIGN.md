# D1 synthetic harness freeze design

Design only: no harness implementation, scoring or disturbance/controller tuning yet.
Dimensionless state/control/time; no physiological units, microrobot geometry, magnetic
map, observation noise or admitted parameter data. Not four-controller science atlas.
Existing open-loop planners/estimators are not counted as controller classes.

## Shared plant, observations and causal policies

Scalar x starts at 0, target 1, dt=1/10, 20 control steps. Actuator bound [-1,1].
At step k, observation is exact x_k if observed[k], else None. Policies see only
that observation, known target/dt/action bound and their own retained past state;
never true x during dropout, future schedule, drift, gain or immobilization flag.
Each policy resets per run. All policies receive identical observation schedules.
Latest-observation hold initialized to x=0 is shared estimation convention.

Two new established-form baseline policies proposed:
- Saturated proportional: clip(target-latest_observation,-1,1), gain fixed 1.
- Saturated sign: +1 for positive target error, -1 negative, 0 zero.
No training/tuning; not validated PID/LQR/MPC/RL implementations or novel controllers.
After valid action u_k, x_{k+1}=x_k+dt*(gain[k]*u_k+drift[k]) unless
immobilized[k], when x_{k+1}=x_k. Immobilization suppresses both drift and actuation.
Exact rational arithmetic avoids floating boundary/tolerance ambiguities.
No hidden control clipping in harness: out-of-bound action is invalid action.
Controller exception and invalid action halt run but keep prior records and failure.

## Frozen supplied sequence candidates (all length 20)

Control reference: gain=1, drift=0, observed=True, immobilized=False throughout.
Each stress differs from reference only by its named sequence, applied identically:
- Alternating drift: drift +1/2 at even k, -1/2 at odd k. Not pulsatile shear.
- Reduced actuation: gain=1/2 throughout. Not RBC drag calibration.
- Immobilization block: immobilized=True at k=5..9 inclusive. Not adhesion law.
- Observation block: observed=False at k=5..9 inclusive. Not imaging-dropout law.
No random seeds or CIs: five fixed deterministic constructed cases per policy.
No >=4 disturbances physiological admission or >=4 controller gate passed.

## Fixed typed outcomes and retention rules

After each plant step, boundary exit iff x outside [-1/2,3/2] (strict inequalities).
It halts before terminal assessment. Terminal assessed only after 20 steps, not at
first target visit: success iff abs(x-1)<=1/10, else terminal_miss. No stall definition
added without another freeze. Failure precedence: controller_exception, invalid_action,
boundary_exit, then success/terminal_miss. Nonfinite or unsupported action types are
invalid action, no silent repair. Malformed protocol is a harness error, not policy
failure. Exact records retain all observations, actions and states up to halt plus
outcome/error identifier. Error message storage must avoid leaking private context.

Report all 10 policy/case rows, final error, maximum boundary overshoot and bounded
control effort sum(dt*abs(u)). Do not collapse exception to success/miss. No comparison
winner preselected; none or all may fail. Lack of failure is not a defect and no
sequence will be tuned to force a required failure after scoring. Successful outcomes
prove only this supplied toy model. Equal observation/action bounds, not equal energy
or information bits in a physical system. Observational hold and two policies are
not the previously reviewed tracker; no estimator integration claim.

## Before any scoring

Implement harness and tests against literal traces, action validation/exception,
reset/causality, missing observations, endpoint inclusivity and typed precedence.
Freeze executable code and JSON sequence manifest alongside this design for independent
review and publication BEFORE full 10-row run. This design alone does not clear scoring.
If implementation changes a rule, disclose and refreeze design. No development run of
the full battery before the executable freeze. Protocol admission, development testing
and synthetic sensitivity results must remain distinct from physiological validation.
