# H1 mandatory manual waveform-binding evidence ledger

Reviewed complete three retained CSVs and the pinned official record metadata before
classification. Frozen executable f235213ad94edd4b0a637b581e217384c8d143ef, no edits.
All three pinned size+MD5 identities verified before any text/CSV parsing. 4,631
original bytes retained. inputs.json carries exact endpoints and SHA256/MD5.
Replay from retained originals produced byte-identical inputs/inventory/manifest.

## Coordinates and literal observations

Citations below are raw Python splitlines 1-based ordinals, blank-inclusive. CSV
record ordinal and physical start/end line are separately stored in inventory.json.
For these actual files, each record occupies one physical line, there are no blank
records or VT/FF, and all three numbering systems happen to coincide. This is a
checked property of these files, not a general conversion rule. UTF8 BOM remains
in each first header field as U+FEFF; it was not stripped or treated as a data unit.

- V = Volume passing.csv, raw lines 1-5, five CSV records, ten fields each.
  L1: `U+FEFFDwell time (sec),μL,μL,μL,μL,μL,μL,μL,μL,μL`.
  L2-5 first fields: `60`, `120`, `180`, `240`. Nine repeated unit-labeled
  columns, no individual column IDs. L2 is `60,31,33,30,41,30,30,39,40,42`;
  L3 is `120,49,56,57,50,40,42,45,51,47`. Remaining rows retained unchanged.
- F = Flow rate_update_07122024.csv, raw lines 1-5, five CSV records, ten
  fields each. L1 first field `U+FEFFTime (min)`, followed by nine identical
  `Flow rate (μL/min)` header strings. L2-5 first fields are also `60`, `120`,
  `180`, `240`. L2 equals V L2 literally. F L3 is
  `120,18,23,27,9,10,12,6,11,5`; for example its first response `18` equals
  V L3 `49` minus V L2 `31`. This arithmetic observation does not establish a
  derivation procedure, matched trials, elapsed interval or corrected time unit.
- W = WSS.csv, raw lines 1-265, 265 CSV records, two fields each.
  L1: `U+FEFFChannel length,WSS (Pa)`. L2: `0,0.040659`,
  L265: `18,0.036398`. L114-115 repeat `7.7253,1.362`; duplicate coordinates
  retained, not dropped. The named independent column is channel length,
  not time. Its unit is not stated in the header or elsewhere in this file.
- M = record-metadata.json, metadata.title refers to a microfluidic vessel-on-chip
  platform, cellular defects in venous malformations, and shear/flow conditions.
  metadata.description is ABSENT, not an empty string. metadata.resource_type is
  dataset, metadata.license.id is cc-by-4.0; files list the exact three identities.
  Title/resource-type labels do not bind the numerical tables to a physical trial.

## Binding decisions within V+F+W+M only

| Required binding | Source-specific evidence | Decision |
|---|---|---|
| Time/index semantics and units | V L1 says dwell time in seconds; F L1 says time in minutes, with identical 60/120/180/240 labels in both tables; W L1 says channel length | Some literal units present, but cross-table time binding/conflict resolution NOT ESTABLISHED. Do not silently turn F minutes into seconds. |
| Time origin, acquisition order, sample interval, drop/aggregation rules | V/F each four ordered printed labels; complete V/F L1-5 and W L1-265 contain no procedure or sampling rule; M lacks description | NOT ESTABLISHED. Printed order/differences do not establish acquisition cadence. |
| Response units | V L1 has μL, F L1 μL/min, W L1 Pa | Literal response-unit labels established; calibration, dimensional consistency and physical interpretation NOT ESTABLISHED. |
| Experiment versus simulation provenance | M title suggests an apparatus topic; V/F/W do not identify measured/simulated values, software, instrument, or trial | NOT ESTABLISHED. No inference from title or shape. |
| Geometry/fluid/forcing regime | W names channel length but omits length unit; no geometry/fluid viscosity, pressure/pump program or regime in complete files or M | NOT ESTABLISHED. |
| Pulsatility definition/period and time-indexed waveform | V/F have four labels and nine indistinguishable response-column names; W is length-labeled, not time-labeled; no command waveform or pulsatility definition | NOT ESTABLISHED. No frequency estimate, interpolation or temporal reinterpretation. |
| Independent trials/repeats and error semantics | V/F have nine unit-labeled columns, no IDs, protocol, independence statement, uncertainties or exclusions | NOT ESTABLISHED. Nine columns are not nine authenticated independent trials. |
| Commanded forcing to observed response | No commanded forcing column or map between V/F/W, no controller/output measurement pairing | NOT ESTABLISHED. Arithmetic coincidences and same labels do not supply the mapping. |
| Rights | M asserts CC-BY4.0 | Dataset-license assertion retained, not blanket hardware/clinical/patent or downstream rights clearance. |

The unsupported statements above are bounded to the complete frozen three CSVs
and the retained official metadata snapshot. They do not claim evidence is absent
from a paper, supplement, other version or anywhere else. No source rescue was
attempted. Strict CSV parsing is syntax only, not validation of any header claim.
