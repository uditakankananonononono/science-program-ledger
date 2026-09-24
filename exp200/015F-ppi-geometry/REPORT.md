# DOC-1-015F: PPI Interfaces + Structure Geometry — REPORT (complete 2026-09-24 12:44 IST)

Follow-up to DOC-1-015 (boundary: linear head on ESM-2-8M+PSSM stalls below frozen bars;
mechanism: feature poverty at interface geometry). Parent-approved sketch 12:27:53; GATES.md
locked pre-scoring (3b46cdc4) + addendum-1 alignment/coverage rule (pre-scoring).
**Outcome: DOCUMENTED BOUNDARY** per the locked failure tree — but with a real positive
mechanism signal: contact-graph geometry is the FIRST feature block to beat the PSSM
baseline in this program's PPI task.

## Structure mapping (locked rule; addendum-1)
RCSB sequence API (identity>=0.95, evalue<=1e-20, first result_set entity): 360/418
survivors mapped (86.0%). 58 zero-hit proteins dropped both-arms (not a short-sequence
artifact: median len 169 vs 164). Coverage guard (>=50% residues aligned to resolved CA)
dropped 40 more both-arms. Final same-set pools: dset72 56/71, dset164 123/164, dset186
141/183 (train). Experimental mmCIF (first model, intra-chain CA only — assembly contacts
would leak the interface label; disclosed design choice).

## Gate results (same-set comparisons per GATES; 015's committed numbers are cross-set anchors)
| Gate | Bar | Result | Verdict |
|---|---|---|---|
| G1 sanity | ARM E train AUROC >= ARM M train | 0.7513 vs 0.7195 | PASS |
| G2 Dset_72 | ARM E >= ARM M + 0.03 | 0.6755 vs 0.6487 (+0.0268) | FAIL by 0.0032 |
| G2 Dset_164 | ARM E >= ARM M + 0.03 | 0.6815 vs 0.6229 (+0.0586) | PASS clause |
| G2 overall | both clauses | one clause miss | FAIL per locked rule |
AUPRC (context): Dset_72 0.227 (M) -> 0.253 (E); Dset_164 0.252 -> 0.310. Direction
positive on every metric and set; magnitude below the locked bar on Dset_72.
Cross-set anchor note: ARM M-control on the reduced same-set pools (0.6487/0.6229) sits
below 015's committed full-set multimodal (0.6697/0.6310) — the dropped 15/41 proteins
were not neutral (disclosed; same-set fairness governs G2).

## G3 mechanism (the useful part)
- Geometry-ONLY arm beats the classical PSSM baseline on both frozen sets:
  Dset_72 0.6023 vs PSSM 0.5853; Dset_164 0.6686 vs 0.5853 (015's committed PSSM number).
  On Dset_164 geometry-only (0.6686) nearly matches the multimodal control (0.6229 same-set,
  0.6310 cross-set anchor) — 4 hand-built geometry numbers carry most of what a 340-dim
  PLM+PSSM stack carries, for interface prediction.
- Contrast with 015's PSSM story (+0.002 over ESM-only): geometry is NOT already inside
  the small PLM the way evolutionary covariation is — it adds real, orthogonal signal.
- ARM E geometry coefficients: packing +2.79 / degree -2.92 (the locked 10A definitions
  are exactly collinear — pack = degree+1 — so the head split weight between them;
  net effect = exposure -1.42: buried/high-contact residues predicted as interface).
  Sign read vs literature: in UNBOUND monomer structures, future interface residues sit
  in unusually packed/concave surface regions — consistent with hot-spot anatomy
  (Bogan & Thorn 1998: interfaces have defined packed cores), not with bulk hydrophobics
  (015's G3 found the same reversal).

## Deliverables
- tools/ppi_interface_geo.py (ESM-2 + flat-PSSM + geometry from user mmCIF; boundary
  disclosed in header)
- results/scores015F.json (all gate numbers, AUPRC, per-set pools), results/models015F.pkl
- GATES.md, GATES-addendum-1.md, PROVENANCE.md

## Prospective nomination (locked)
Dror lab (DIPS benchmark lineage, as 015) or a PPI-benchmark group: evaluate whether
monomer contact-graph geometry transfers as a cheap interface prior to complexes absent
from training (geometry-only is within 0.013 AUROC of the multimodal stack on Dset_164 —
a nearly-free feature worth prospective testing on DIPS-class cases).
