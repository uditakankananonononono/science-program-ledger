# GATES v2 (locked 2026-09-23 ~23:30 IST, before any species-level outcome)
G1 FAILED at genus level (median rel. RMSE reduction 7.5% < 10% gate; 20/30 panel
metabolites permutation-significant). Locked failure policy fires: pivot to
SPECIES-level features (species.tsv), all other gates identical (same panel of 30
metabolites, same CV scheme, same permutation protocol).
- G1-v2: median relative RMSE reduction >= 10% AND >= 50% permutation-sig.
- G2 note: the pre-registered microbial-metabolite class list matched ZERO panel
  members at genus run (checked against high-confidence annotations) - G2 is
  NOT EVALUABLE on this panel and is retired, documented honestly. The v2 payload
  keeps the per-metabolite predictability map (named compounds incl. urobilin
  R^2~0.57) plus a species-vs-genus predictability comparison per metabolite.
- If G1-v2 also fails: the documented result is the genus/species predictability
  ceiling map (which metabolites composition can read at all) - a boundary with a
  real payload, adjudicated by lead lane.
