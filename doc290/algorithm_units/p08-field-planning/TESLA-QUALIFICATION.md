# Tesla upstream qualification, not physical admission

Official upstream read via HTTPS git from observed source URL:
https://github.com/ethz-msrl/Tesla_core_public
Pinned HEAD 5ef021b0f4c0b91d1d8f3aedf353fe24bf793e84 (October 8, 2026).
Read-only shallow partial clone outside our published repository; no upstream code
or calibration coefficients copied into this unit, no upstream executable run.

## Exact-byte findings

Root LICENSE is a custom BSD-style license with four conditions, including an
advertising acknowledgement to MSRL/ETH Zurich and a no-endorsement condition.
MPEM C++ source header also contains advertising acknowledgement. package.xml's
BSD tag and the repository summary's Other label do not supersede these bytes.
OctoMag calibration YAML has its own Apache-2.0 header, a narrower file-level
licensing statement. Mixed declarations require component-specific handling;
this note is not blanket rights admission or legal advice. Any eventual import
must retain notices and examine dependencies/calibration provenance separately.

| Upstream path | SHA256 |
| --- | --- |
| LICENSE | 6d73dca2e0fbc7b023939eb82b30c79c388e28e0ca522f2f5d450de8086234c7 |
| mag_control/mpem/cal/OctoMag_Calibration.yaml | d0d92541ea3669bb1c4d4daf4acd36b9d3100f728e6270e2aebac53906cc0ad0 |
| mag_control/mpem/include/mpem/electromagnet_calibration.h | 39a37f81e6bf1785fd1e0f1920bd3bd2401f1a6d51e1ec6167fe3d55f3b2a548 |
| mag_control/mpem/src/electromagnet_calibration.cpp | 9ab4c6af405beb866a61916ed0d8aa0597dc9e377987ed176c0822135372cdf8 |
| mag_control/mpem/package.xml | 8a2fdedf91af1cf8fd3dd558df59707c54e6c62f7fa4f36cdd3e698ab6c9a0df |

MPEM README says calibration uses position/current/field CSV, positions in meters,
current in amps, field in tesla, and nonlinear least squares fitting. It requests
verification CSV but permits reusing fitting data as verification data; that option
cannot establish independent held-out error for our benchmark. Its model is described
as analytical with gradients obeying quasistatic Maxwell equations, which is an
upstream description, not independently tested model behavior in this lane.
mag_manip README distinguishes linear-current regimes from saturation and recommends
nonlinear models for strong saturation. Hence a static gradient/current map cannot
be silently treated as globally valid for every input current.

## Remaining admission gaps

The YAML includes eight coil labels and model coefficients, but those bytes alone
do not establish device identity/version, independently held-out field/gradient
error, supported current/position domain, or current/slew/thermal limits. No raw
held-out OctoMag fitting/verification dataset was identified by the bounded path
inspection; that is not proof none exists elsewhere. Robot magnetic moment,
orientation model and fluid/wall/flow mobility are still unadmitted. No calibration
values executed, no physical actuator map or hardware schedule approved.

Recommendation: retain current P08-04 outputs as abstract/synthetic baselines.
Qualify file-level rights and exact calibration validity domain before importing
one profile; require independently verified errors and robot mobility evidence
before assigning physical units/performance claims. No invention/scientific gate.
