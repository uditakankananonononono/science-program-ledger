# P08-06 initial interface and magnitude screen

Inventory of checked local implementation tree at 3dac113ed67d181c4df2623c147b64afda551a9b.
Initial three-new-primary-source screen plus prior Doppler primary; not a completed
physiological literature survey or absence claim. No measured dataset admitted,
controller simulation built, disturbance battery frozen or atlas scored in this unit.

## Actual interfaces, not names promoted into controllers

| Module/callable | Inputs/outputs | Role and admission boundary |
| --- | --- | --- |
| p08-field-planning/feasibility.solve | initial,target,dt,actuation,limit,slew,previous; status, full controls/trajectory/residuals | Discrete constant-map open-loop terminal LP. No flow, measurement, feedback step or real field calibration. |
| p08-field-planning/corridor.solve_corridor | same plus lower/upper node boxes; schedule/trajectory | Discrete-node open-loop corridor plan, not continuous collision safety. |
| p08-field-planning/scenarios.solve_scenarios | finite constant maps and terminal bounds; common schedule | Open-loop feasibility across specified maps, not adaptive controller. |
| p08-field-planning/minimax.minimax_terminal | finite maps/targets; shared controls, worst coordinate error | Open-loop minimax terminal LP, not independently dual-certified optimum or MPC interface. |
| p08-tracking/kalman.ConstantVelocity.step | dt, optional position measurement/covariance; state [x,y,vx,vy], P, NIS | Causal estimator only. Missing data predicts; no actuation/control output. q/R caller supplied. |
| p08-tracking/smoother.smooth | supplied Gaussian forward records; smoothed records | Offline future-data estimator. Exclude from causal controller comparison. |
| p08-reacquisition/deferred.resolve | first/confirmation observations; provisional/confirmed state | Two-branch delayed measurement handling. Not feedback actuation, calibrated association or dropout statistic source. |
| p08-routing/routing functions | graph, costs/budgets/turns; route witness | Graph planning; no dynamical actuator loop or physical edge calibration. |
| p08-swarm probability units | marginal/joint event distributions; probabilities/certificates | Probability accounting/decision selection, not controllers or disturbance dynamics. |

No P08-02 executable control module in this checked root; source direction is a
specification, not implemented PID/LQR/MPC/RL. Four controller classes cannot be
obtained by renaming these modules. Possible future receding-horizon adapter for
field planners requires explicit observation/state/control timing, failure handling,
actuator units, updated state and plant model. No such adapter admitted here.

## Evidence for magnitudes: candidate facts, not simulator calibration

1. https://pmc.ncbi.nlm.nih.gov/articles/PMC7909881/ (2021 Doppler microswarm).
Primary text: pulsatile pump interval 1 s, input 12 ml/min/mean 37.7 mm/s;
continuous 14 frames in 1 s had 9 frames with detectable red signals in one example.
These are controlled experimental conditions and illustrated detection sequence,
not a distribution of physiological shear impulses or Bernoulli imaging dropouts.
Strongly dependent frame detection/processing and magnetic actuation matter.
CC BY-NC article; raw/supplement rights not admitted. No values used in harness.

2. https://www.nature.com/articles/s42005-024-01724-4 (2024 Communications Physics,
"Drag force on a microrobot propelled through blood"). Numerical framework with
experimental validation examines resistance in RBC suspensions. Describes changing
hematocrit in quiescent suspensions and dependencies on robot/RBC size and geometry;
Fig.1 example phi=20%, Gamma=epsilon=1. These model-specific dimensionless controls
are not additive force/noise magnitudes for our current integrator. Data and code availability both state corresponding-author reasonable request.
No downloadable artifact or reuse grant established; none requested/downloaded here.

3. https://pmc.ncbi.nlm.nih.gov/articles/PMC10162671/ (2023 active retention).
Primary text gives geometry/coating-dependent detachment, claw-mediated retention
and reversibility under rotating magnetic fields. Controls under 30 mT/30 Hz detach
when blood-plasma flow increases to 2.1 cm/s, while clawed particles can adhere and
remain stationary. This is not a random adhesion-duration law or universal wall
collision threshold. Specific robot/surface/fluid/field domain essential. Article
states CC BY-NC 4.0; no force/time distribution or dataset admitted.

4. https://www.mdpi.com/2072-666X/14/2/317 (2023 pulsatile RBC assessment).
Primary experimental apparatus uses blood/dextran microfluidics, tested Hct 30/40/50%,
including a T=240 s pulsatile fit with mean 10.68 mm/s and alternating 4.51 mm/s.
This apparatus waveform period is not physiological heartbeat period. Sedimentation,
dextran and flow system affect readings; not direct microrobot crowding perturbation.
No waveform bytes/rights admitted or universal parameter calibration inferred.

These excerpts support why source anchoring cannot be a unitless number copied into
a stress test. Shear, crowding, adhesion and imaging dropout remain UNANCHORED for
our plant. Exclude all from a physiological atlas until qualified; clearly synthetic
analogs can be used only in a labeled development harness.

## Next-unit contract proposed, not yet frozen

Minimal shared dimensionless position integrator, explicit actuator bound, causal
observation and per-step bounded action. New baseline controllers must be implemented
and named honestly, not called existing validated published controllers. Disturbance
sequences supplied explicitly with units/definitions, not physiological labels.
Typed outcomes separate control exception, invalid action, boundary exit, terminal
miss and timeout; thresholds locked before scoring. No tuning to force failure or
all-controller failure. Lack of failure is valid data, not an evaluation defect.
No controller-count or four-disturbance science gate passed by an interface inventory.
