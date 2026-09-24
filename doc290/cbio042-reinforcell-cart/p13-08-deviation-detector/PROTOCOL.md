# P13-08 Deviation Detector (BatchSentinel) - locked protocol

Locked 2026-09-24 11:39 IST, before any detector was trained or scored.
What had been looked at: file structure, batch IDs, and the Fault_ref windows of batches 91-100. No model outputs.

## Data
IndPenSim V3, Mendeley Data doi:10.17632/pdnjz7zz5x (zip sha256 bc434c6c...181f00). 100 batches:
1-30 recipe, 31-60 operator, 61-90 advanced/PAT control, 91-100 recipe with faults (Fault_ref = 1 inside the fault window).
Raman columns dropped. The source header splits one name across commas, so columns are re-named by position (tool/load.py).

## Features (online-measurable only)
Fg RPM Fs Fa Fb Fc Fh Fw pressure Fremoved DO2 V Wt pH T Q CO2outgas Fpaa Foil OUR O2 CER NH3_shots, plus batch time.
Excluded: substrate/penicillin states (S, P), all offline assays, fault/flag columns.

## Split (nominal batches, balanced across the three control modes, seed 0)
Per mode: 15 train, 5 calibrate, 10 test (45 / 15 / 30 overall). Faulted: all 10 (91-100) are test only.

## Detectors
(a) Phase-aligned z-score model: per sensor, nominal mean/sd in 2 h batch-time bins; score = RMS of z-scores.
(b) Isolation Forest on 5-step sliding-window features (mean, slope, sd).
(c) Dense autoencoder (sklearn MLP, bottleneck 8) on the same windows; score = reconstruction error.
    Deviation from spec: the spec says LSTM autoencoder. torch isn't available in the build sandbox.
Ensemble = max of per-detector scores, each rank-normalized against calibration-nominal score distributions.
Alarm = score above threshold for 3 consecutive samples. The threshold is set once, on calibration nominals only,
as the smallest value giving <= 0.5 alarm events per batch.

## Gates
- G1: on held-out faulted batches, detection rate >= 90% (alarm inside [first Fault_ref, last Fault_ref]) at <= 1 false alarm
  per batch (alarm events on the 30 test nominals, plus pre-onset alarms on faulted batches).
- G2: median lead time >= 20% of batch duration before fault manifestation. Manifestation = first time penicillin P leaves
  the phase-aligned nominal +/-3 sd band for 3 consecutive samples after fault onset (batch end if never).
  Lead = (manifestation - first in-window alarm) / batch duration.
- G3: transfer to mammalian data keeps >= 70% detection with <= 2x false-alarm inflation, or the domain gap is quantified.
  Pre-declared data boundary: a bounded search (web; NIST CHO / csbg DGTX repo; Kamen Lab Borealis) found no public
  mammalian culture dataset with online sensor streams across multiple runs and labeled deviations. The NIST CHO
  feeding-strategy data is daily offline assays only. G3 is recorded as a data boundary. The spec's pivot (synthetic
  cell-therapy benchmark) is logged as follow-on work, not run in this build.
- G4: honest-negative clause per spec.
Evaluated once. Any repair is disclosed.
