# DOC-1-002F: Replogle-Scale Perturb-seq Retry — REPORT (complete 2026-09-24 12:28 IST)

Follow-up to DOC-1-002 (boundary: TF-KO mRNA effects inseparable from noise at available
scale; named repair = Replogle-scale retry with n-vs-full-reference null). Eligibility
verified 12:22 (parent-reported); sketch approved 12:22:30; GATES.md locked pre-scoring
(commit 1ebc8bc6) with numeric thresholds per parent's two adjustments.

## Headline
- G1 PASS (decisive): 1,088/1,299 targets with >=100 cells pass effect-presence vs the
  repaired null (bar >=650; q95 = 2.7043). 002's 0/10 was power/null, NOT biology — the
  falsifiability boundary is REPAIRED at Replogle-essential scale (10,691 controls,
  n-vs-full-reference null as named in the 002 WRITEUP).
- G2 PASS (decisive): 1,141/1,164 on-target-visible targets repressed (bar >=698; 98.0%).
  CRISPRi assay QC confirmed; 002's KO-invisibility failure mode absent.
- G3 FAIL per locked bar: network-from-controls (control-cell correlation network) median
  r_net 0.317 vs shared-program baseline (mean DE of other panel members) median r_base
  0.621; bar required r_net >= r_base + 0.10. Permutation clause passed (12/20 <= 0.05)
  but is moot given the first clause. Panel = top-20 G1-passers in the top-500
  control-variance set (full 20/20 eligible).

## Interpretation
The 002 question is now ANSWERED at adequate power: perturbation effects are real and
detectable (83.8% of targets), the assay works (98% on-target repression), but the
control-cell correlation network does NOT predict a target's differential-expression
profile better than the average of other perturbations. The shared essential-response
program dominates (median 0.621); control-space regulatory correlations add nothing above
it. Consistent with the co-essentiality literature: functional modules are recoverable
from perturbation-space structure, not from unstimulated control-space covariance.
Per the locked failure tree (G1+G2 pass, G3 fail): falsifiability repaired, the 002
hypothesis answered negatively at adequate power — a real answer, not a boundary.
Parent adjudicates counting.

## Protocol fidelity
All mechanics per locked GATES: rng seed 20260924; N = log1p(CPM*1e4); S = top-500
control-variance genes ∪ target genes (|S| = 1,490; 1,164 targets in-matrix); n=100
per-target draws; 200-draw full-reference null; same thresholds as locked. Streaming
pipeline (tools/grn_perturb_predict.py) ran end-to-end in ~2 min of passes on 1.9GB RAM.
Data: ReplogleWeissman2022_K562_essential.h5ad, Zenodo 7041849, md5
d8cba17576d1a8afc0f7d71b79cad0f7 (verified). results/: g1/g2/g3_results.json (full
per-target tables).

## Prospective nomination (locked)
A Perturb-seq validation lab (e.g., an scPerturb-scale consortium group): test whether
control-space network edges predict perturbation responses in a NON-essential context
(signaling-pathway or TF-perturbation screens with weak shared programs), where the
shared-program baseline is weak enough for control-space signal to matter. The 002F
result predicts control-space networks only lose where a dominant shared program exists.
