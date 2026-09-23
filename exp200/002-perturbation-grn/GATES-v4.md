# GATES v4 (locked 2026-09-23 ~22:53 IST, before any Adamson-dataset outcome)
# Project steered to a new dataset per the pivot rule after the documented v1-v3 boundary.
Dataset: AdamsonWeissman2016_GSM2406675_10X001.h5ad (scPerturb, Zenodo 13350497).
Design identical to v3 (control-only top-500 variable genes; size-matched 100x
control-split effect-presence null; panel >= 5 required; G1 median Pearson delta >= 0.05
vs mean-DE baseline AND >= 50% permutation-sig; G2 precision@20 beats baseline).
QC note (pre-registered from v1 lesson): report target-mRNA invisibility rate; do NOT
use target-mRNA self-effect as a panel criterion. If this dataset also yields <5 panel
targets or fails G1/G2, DOC-1-002 closes as a two-dataset boundary, documented, and the
topic is reported to the lead lane as needing a large-screen (Replogle-scale) retry
outside the 2GB compute envelope.
