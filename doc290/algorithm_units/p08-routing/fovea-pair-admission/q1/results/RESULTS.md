# Q1 frozen FOVEA shared-skeleton query diagnostic

Published freeze7b40a6d335d724d6cb5ee888d7f9ba55fd1f89d2 then sole full80-pair
measurement in fresh Python -I process, explicit entrypoint, exact pinned pipeline.
No code/endpoint/threshold rule changes. Raw80 rows/all9600 query records, protocol
version/pins, environment and hashes retained. No insufficient endpoint pairs.
All pairs have16 endpoints/120 queries. Original masks and old QC unchanged.
Publication-before-run supported by push/readback log, not review replay alone.

| Phase | Queries | Both reachable | A1 only | A2 only | Neither | Images with disagreement |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Preoperative |4800|4756|0|15|29|1/40|
| Intraoperative |4800|4800|0|0|0|0/40|

Only FOVEA019_p has A2-only queries:15/120,105 both,0 neither; original components
A1=3,A2=1. Component counts alone differ in8 pre/3 intra pairs in old QC, but these
restricted query endpoints reveal disagreement in only one image. Equal restricted
query outcomes do NOT mean equal components/branches or annotation correctness.

Shared pixel coverage ratios (aggregate pixel-weighted, not mean image/patient rate):
Pre A1:198647/1286714; A2:198647/1289762. Intra A1:74628/310773; A2:74628/312780.
Shared pixels per image range2382..8977 pre,722..3717 intra. Each raw row retains its
exact numerator/denominator and endpoint/query/component identities. Exact shared
skeleton overlap selects a small minority of skeleton pixels, then samples16 points;
workload is biased toward overlap and may miss thin/disconnected branches. Zero
intra disagreement is NOT proof no ambiguity or a negative anatomical finding.

80 patient-phase pairs over40 patients, not80 independent patients;9600 correlated
deterministic queries, not independent observations/CIs. Both phase images differ in
scale/rotation/FOV and are not pixel-registered. No nearest projection, repair, union/
consensus anatomical truth, artery-vein/flow costs, robust-routing score or novelty.
All masks previously exposed development. This is supplied-representation diagnosis
only; endpoint coverage/missingness limits retained. No hypothesis rephrased into
invention in this measurement commit. Full original3.1GB MD5 not recomputed today;
mask ZIP/160-byte hashes have independent recheck as previously reported by parent.
