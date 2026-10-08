# Constant-map terminal support bounds

Established analytic reachability bound, not invention. For positive dt, actuator
j has feasible pointwise extrema min(limit,previous+slew*cumulative_time) and
max(-limit,previous-slew*cumulative_time). These monotone saturated ramps obey each
step's slew constraint. For direction v and fixed B, each control weight is dt[k]
(v^T B)[j], whose sign is constant across time. Thus sign-selecting the upper/lower
ramp independently per actuator attains the terminal projection extrema. Returned
extremizing schedules witness those two supports. No LP used in production function.

41 local dev methods pass (37 prior + 4): hand-computed scalar ramp, negative weight
with nonzero previous control, coordinate bounds insufficient for joint feasibility,
and dense-map comparison against an independently assembled LP plus witness checks.
The rank-one target [1,-1] lies inside both coordinate ranges but fails direction
[1,-1], explicitly showing that finite direction passes do not prove feasibility.

Outside a verified support interval implies unreachable for these abstract constraints,
but no automatic target verdict/tolerance classification implemented here. Floating
arithmetic interval endpoints are not exact rational certificates; use numerical
margin/error policy before an application rejects a near-boundary target. No corridor,
terminal boxes, coupled controls, time-varying maps or continuous safety included.
Scenario intersection has not been solved by this single-map support. No hardware,
anatomy, calibration, score, novelty or scientific gate. Review pending. Prior code
unchanged. Extreme finite arithmetic may raise FloatingPointError; scaling open.
