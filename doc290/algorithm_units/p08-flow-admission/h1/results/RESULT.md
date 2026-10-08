# H1 result: reject pulsatile-controller waveform admission on fixed surface

Outcome B. After the mandatory manual evidence ledger, time-indexed pulsatile
waveform admission is NOT ESTABLISHED WITHIN THREE CSVs + PINNED RECORD METADATA.
All original source identities verified; this is an evidence-binding rejection,
not a transport-unavailable result. No source, executable, cap or rule changed.

Useful positives: V and F each have four data rows with nine response columns;
V labels dwell time in seconds and volume in μL; F labels time in minutes and flow
rate in μL/min. W has 264 data rows labeled channel length and WSS (Pa). Original
BOMs, repeated headers and duplicate W coordinates retained. No syntax errors or
blank/ragged records in this source run. These are literal table observations,
not schema/physical validation. See MANUAL_LEDGER.md for exact raw citations.

Critical losses: identical V/F numeric time labels with different unit labels are
not resolved; time origin/sampling/aggregation, measured-vs-simulated provenance,
geometry/fluid/forcing regime, pulsatility definition, trial identity/independence,
uncertainty, and commanded-forcing/response mapping are not established. W's
channel-length axis has no supplied unit and cannot be relabeled as time.
Do not repair the minute/second labels or divide/integrate tables to invent data.

No waveform fit, frequency estimate, plot, model/controller experiment, simulated
substitute, RL/proxy score, physiology readiness, heldout performance, novelty or
invention credit. CC-BY4.0 metadata is not rights clearance. No absence-elsewhere
claim. This closes only the H1 bounded admission, not all Flow-Adaptive Control.

Execution: published frozen f235213ad94edd4b0a637b581e217384c8d143ef;
Python 3.10.12 pin checked by executable. 4,631 source bytes verified before
analysis; socket/read limits, not hard wall-clock/memory quotas. Retained-source
replay inputs/inventory/manifest byte-identical. Text-only artifacts, no spatial
or visual claim. Results await exact-commit review before publication.
