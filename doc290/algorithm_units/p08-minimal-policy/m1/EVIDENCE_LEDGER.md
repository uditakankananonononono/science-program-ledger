# M1 manual evidence ledger

Source Synthetic-Automated-Systems/RUDER_MBOT_RL, exact
e27a3ca877763cad6f8f3667ab96242a70e49819. All11 fixed sizes/Git blob OIDs
verified before AST/text analysis;113,447 bytes. All strict UTF-8; all four Python
sources parsed without AST error. AST inventory is triage, not policy/budget admission.
Citations below are raw Python str.splitlines(),1-based, blanks retained, VT/FF
boundaries included. All11 sources have zero VT/FF. AST lineno uses parser newline
convention; no silent substitution of AST coordinates for raw citations.

## Eleven-source evidence inspection

README.md L4: source describes helical agar swimmer/external electromagnet and a
Windows10 workstation with dual NVIDIA RTX1080 GPUs. L10-14 identifies host main
program/environment/config and Arduino STEMtera firmware plus motor shields. This
supports descriptive apparatus partition, not an onboard swimmer processor. "Official"
is the README's assertion; live GitHub metadata marks this repository as fork. Neither
proves false attribution or author identity; fork status does not invalidate readable
source bytes. No additional upstream/code/artifacts were fetched to resolve provenance.

LICENSE L1-3 root MIT/copyright2022 mrbehrens48;L5-13 permission and notice conditions;
L15-21 warranty disclaimer. Root source assertion/evidence, not weights/data/hardware/
import/patent clearance or external-author authority.

microrobot_SAC_control.py raw L1-21 imports TensorFlow,camera Vimba,OpenCV,environment,
config and host libraries; not executed. L23-26 chooses convolutional image-history
or state-history shape. L29-37 references local model/log/buffer folders including
absolute Windows model_save_path L32. L47-49 device-ID comments are not runtime
placement proof: environment function explicitly enters CPU context L718; learner
enters GPU context L1366, after GPU-memory configuration L1354-1361. No actual
runtime/hardware capability measured from those declarations.

L268-280 policy calls pi_model TWICE with training=True for both mu/log_std,
clips/exponentiates log_std,samples Gaussian action and squashes. State actor L341-354
contains Dropout0.2 atL348/L350. Even the evaluation branch selecting returned mu
L868-874 still calls this training=True policy. Therefore source's "deterministically"
config comment cannot be silently adopted as proof of deterministic inference.
No correction, execution or claim of observed behavioral error made.

Architecture defined in L294-313 CNN and L341-354 state actor. Architecture is not
trained immutable policy. L768-779 loads local .h5 filenames; learnerL1374-1391 also
loads referenced models. L1453-1467 writes learned/top .h5 files; these are procedural
references, not checkpoint bytes recovered here. L1427-1445 calls learn on minibatches;
L202-259 andL382-426 define update/learn/alpha pathways. Host environmentL804-883
selects random,hand-coded or learned actions and sends them to environment step;
L937 queues experience. L1480-1529 multiprocessing startup is host orchestration,
not swimmer firmware. Named weights/replay/checkpoint NOT RECOVERED WITHIN THIS
FIXED11-TEXT-FILE UNIT, no searched proof absent elsewhere.

microrobot_environment.py L33-76 physical environment: episode_length100,
goal_distance20,theta-margin3,success_reward1000 and STEP_DURATION0.3 L52 are
declared constants, not measured budget or inference timing. L69-76 COM5 serial
connection. ObservationL104-119 gets camera picture,grayscale,threshold,id,resize;
thresholdL329-339 uses threshold200,inversion,13x13 dilation. id_robotL344-396
uses two contours,centroids,angle,goal marking and abort if count differs; not
calibrated localization evidence. Nonconvolutional stateL215-232 includes theta/360,
goal offset/360,remaining-episode fraction and previous4actions; stackingL258-273
uses N_steps. Convolutional observation/255 atL211-214. This is source-specific
preprocessing, not a portable benchmark observation stream.

ActionL157-182 uses four inputs M_x,M_y,phi_x,phi_y,derivesM_z=max(abs(M_x),abs(M_y)),
setsfreq80 and maps phase to0..2pi,then serial command. These are source command
values, not measured magnetic field/force/energy units or safety bounds. L188-203
loops N_steps observations and waits on STEP_DURATION; controller cycle includes
camera/OpenCV/serial work, not measured inference latency. L247-255 reward is
angular increment plus success bonus at angle tolerance; not vascular delivery or
an independent navigation validation. L299-310 formats six serial values/response.
Microrobot_Sim L398-553 is separate source simulation code, not run or evidence for
physical transfer. Config switch does not turn it into a admitted proxy experiment.

myconfig.py L6 SIMULATION0,L12 CONVOLUTIONAL0,L15NUM_ACTIONS4,L23-33 eval/load
flags/model-name references;L40/L43 random/warmup/update thresholds;L45-50 hand
policies disabled;L59STATE_SIZE64,L62N_STEPS3;L71/L74 training time/frame caps;
L77BUFFER_CAPACITY100000,L80BATCH_SIZE256,L101update/frame ratio,L104eval frequency.
All declarations, not serialized policy size/runtime memory/measured cycle budget,
independent seeds or held-out dataset. L110Arduino reset interval60 is also not
inference latency. No runtime config evaluated or model initialized.

Magneturret/Magneturret.ino L2-8 imports motor-shield libraries,coil connections;
L82-98 sets up serial/motor apparatus. L115-143 loop receives host commands then
uses sinusoidal PWM coil drive. L154-212 parses incoming text and six coil parameters,
not camera observations or neural navigation policy. L240-255 temperature handling
is source firmware logic, not a tested hardware-safety guarantee. Coil PWM constants
and millis()/serial rates do not bind onboard swimmer computation,memory,power,
inference latency or measured controller-step rate.

Magneturret/Serial_Commands_to_coil.py L9-16 imports serial and opens COM5;
L25-35 formats six fields,writes/reads serial;L39-43 repeating debug commands and
sleep1. Debug sleep is not a measured navigation/controller budget. Never executed.

requirements.txt L1-173 dependency declarations,including TensorFlow2.1.0L149,
Keras2.3.1L57,OpenCVL78,pyserialL111 and Vimba local file URL L163; multiple other
local build paths (e.g.L20,L42,L172). No installation; list is not portable runtime
proof, dependency license clearance or pinned complete hardware/camera environment.

libraries/readme.txt L1-49 motor-shield installation/pin remapping/apparatus wiring
instructions. Evidence for external coil driver interface only, not permission to
wire hardware or compile source; no instructions followed, no linked-source fetch.

libraries/DualG2HighPowerMotorShield/LICENSE.txt L1-25 and
libraries/DualG2HighPowerMotorShieldTop/LICENSE.txt L1-25: same Pololu2017 license
assertion/permission,notice/warranty clauses. Exact texts retained; these do not
clear third-party imports,camera data,hardware or patents. No dependency adopted.

## Binding decisions

| Item | Evidence | Decision |
|---|---|---|
| Source observations/actions/preprocessing | controlL23-26;envL104-119,L157-182,L211-232,L329-396 | Descriptive source pathways identified, NOT replay calibration |
| Inference vs training | controlL268-280,L718,L868-874,L1366,L1427-1445 | Host source partition identified; actual execution not measured |
| Trained immutable policy/checkpoint | configL26-33;controlL32,L768-779,L1453-1467 | Not recovered within fixed unit; no elsewhere absence claim |
| Onboard swimmer navigation compute | README L4/L10-14;firmwareL115-143 | NOT ESTABLISHED; Arduino apparatus is coil actuator, not swimmer |
| Measured memory/FLOPs/latency/power/device budget | config constants;envL52,L188-203;firmware PWM | NOT ESTABLISHED; no measured budget table/trace in fixed sources |
| Fair replay/task/split/seed comparator | reward/env and training/config references | NOT RECOVERED within unit; no independent replay bytes |
| Deterministic evaluation | configL23-24 vs policyL268-275/state-actor dropout | UNRESOLVED implementation semantics; no deterministic assumption |
| Rights | root +2 component license texts | Evidence/assertions only; no clearance |

## Endpoint and controls

REJECT policy-compression/invention benchmark on this bounded source surface:
immutable trained policy,replay/equal-budget comparator and measured compute budget
not recovered/admitted. Descriptive host/coil partition and source preprocessing
are useful evidence, NOT minimal onboard deployment or invention. Structural machine
output did not determine this finding; manual cited source evidence did. No positive
compression gate,quantization/distillation/simulation/proxy experiment or benchmark.
No new model,checkpoint repair,external weights fetch or dependency install.

40s deadline checked between20s reads,not hard mid-read. CPU/RAM stated,not quotas
or measured peak. Failed partial streams would be error-recorded,not complete
originals; all11 actual reads verified complete. No VT/FF divergence in actual texts.
