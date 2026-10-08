# P08-04 actuator-model grounding - October 8, 2026

The abstract LP cannot yet be promoted to a magnetic microrobot planner. OctoMag
provides a defensible model lead, but its map depends on position and magnetic
moment. Our constant linear actuator-to-position-rate map does not contain those
quantities or hydrodynamic mobility. No hardware profile or scientific gate admitted.

## Recommended path

1. Keep current LPs as abstract software baselines.
2. Qualify device-specific field/gradient calibration bytes and rights before
   importing them. Inspect the official Tesla model code as a lead, not a licensed
   dependency based on repository existence alone.
3. Specify robot magnetic moment, orientation assumptions, fluid mobility, and
   position-dependent maps before constructing a physically labeled schedule.

## Primary model evidence

OctoMag (ICRA 2010) states field B(P) = B(P) I and directional gradient maps from
individual coil contributions. Its equation (7) maps currents to field/force via
A(M,P), and equation (8) gives pseudoinverse control. Knowledge of pose and magnetic
moment is required; alignment with the field is an assumption under slow enough
orientation changes. These do not validate our constant map along a vessel path.
The paper's center-workspace force examples assume 15 A amplifier saturation; this
is not a calibrated per-device operating/slew policy or a microrobot velocity bound.
No numeric hardware limit was imported.

A possible future connection is mobility times a fixed-moment gradient-current
force map. That is a proposed modeling derivation, NOT a sourced/validated drag
or mobility value. In vivo wall/flow effects and orientation changes remain open.

## Code/model leads and limitations

mag_manip's package description explicitly models electrical currents to magnetic
field in an electromagnetic navigation system. mCR_simulator interfaces that model
to SOFA mechanical simulation and a calibration path, but concerns magnetic continuum
robots, not automatically untethered microbots. Tesla_core_public is the official
upstream lead named by adjacent code. Search's GitHub-named mirror was excluded.
Its fetched repository summary says license Other; exact component licenses and
calibration rights were not audited. Modeling_eMNS's fetched summary says Apache
2.0; this is metadata, not admission of all code/calibration files. Adjacent levitation
and inverted-pendulum implementations show calibration dependencies; neither is
microrobot tracking/anatomy validation. No code or calibration dataset downloaded.

## Source ledger

All below pages fetched; titles/dates as visible, no bibliographic precision claim.
- OctoMag ICRA 2010 primary paper, hosted by Missouri university:
  https://vigir.missouri.edu/~gdesouza/Research/Conference_CDs/IEEE_ICRA_2010/data/papers/0469.pdf
  Used for field/gradient/current map and pose/moment assumptions.
- ETH repository primary paper lead, Remote Magnetic Levitation Using Reduced Attitude Control and Parametric Field Models:
  https://www.research-collection.ethz.ch/server/api/core/bitstreams/417d0174-8f1d-4662-aa91-06c7bbb91a15/content
  Adjacent lead, no imported hardware values.
- Package registry description: https://pypi.org/project/mag-manip/
  Used for current-to-field model purpose, not licensing/calibration acceptance.
- Official model repository: https://github.com/ethz-msrl/Tesla_core_public
  Used as upstream lead, component rights unresolved.
- Official modeling repository: https://github.com/ethz-msrl/Modeling_eMNS
  Adjacent lead, no code/calibration admission.
- Official continuum simulation repository: https://github.com/ethz-msrl/mCR_simulator
  Used for distinct robot domain and calibration/mechanics dependency.
- Adjacent levitation repository: https://github.com/NeelakshSingh/oct_levitation
  Lead for calibration workflow, no transfer of device claims.
- Adjacent pendulum repository: https://github.com/slavasg-lab/emns_invpend_swingup
  Lead for calibration/model fitting, no transfer of device claims.

Three source types: primary papers, project repositories and package registry.
No real anatomy, hardware constraint gate, license admission or novelty established.
