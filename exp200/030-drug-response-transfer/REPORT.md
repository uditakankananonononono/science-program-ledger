# DOC-1-030: Predicting Drug Response from Single-Cell Data with Transfer Learning - DOCUMENTED BOUNDARY

## Outcome
Bulk-to-single-cell transfer learning does NOT beat the published cognate-target biomarker on
the 32-line breast cancer single-cell atlas. Dev gate G2 fails; pre-registered rescue P1
(per-cell DREEP-style scoring) fails the same gates; frozen afatinib results concur.
Failure tree exhausted per locked GATES.md (2026-09-24 08:31 IST, pre-outcome).

## Data (all public, provenance-verified pre-lock)
- sc atlas: Gambardella 2022 Nat Commun 13:2394 (figshare 15022698), 35,276 cells, 32 breast lines.
- Bulk: CSA benchmark (Zenodo 15258883) cancer_gene_expression.tsv, 468 GDSCv2-labeled CCLE lines x 30,805 genes.
- Labels: CSA response.tsv GDSCv2 AUC; lapatinib Drug_435, afatinib Drug_520; 25/32 atlas lines each
  (GDSCv1 contingency not triggered). Manifest + hashes committed pre-training (results/data_manifest.json).

## Results (Spearman rho, sign-aligned so higher = more sensitive; n=25 paired lines)
| arm | lapatinib (dev) | afatinib (frozen) |
|---|---|---|
| BASELINE ERBB2+EGFR biomarker | **+0.415** (|.|>=0.30, G1 PASS; published PCC -0.423 GDSC / -0.395 CTRPv2) | **+0.478** (published -0.716 GDSC / -0.530 CTRPv2) |
| ARM A no-adapt ridge transfer | +0.163 | +0.214 |
| ARM B quantile-aligned transfer | +0.214 | +0.213 |
| P1 per-cell sensitive-fraction | +0.216 | -0.324 (anti-predictive) |

## Gate adjudication (against locked thresholds)
- G1 PASS: baseline |rho|=0.415 >= 0.30; recomputed GDSC PCC -0.415 vs published -0.423 (labels coherent).
- G2 FAIL: ARM B 0.214 < baseline 0.415 + 0.10 (margin -0.301); ARM B >= ARM A + 0.05 marginal (0.214 vs 0.213).
- P1 FAIL: 0.216 < 0.515 threshold; afatinib P1 inverts sign.
- G3 (frozen) FAIL under the same reading; tree exhausted -> DOCUMENTED BOUNDARY.

## Mechanism (G4, runs regardless)
- MDAMB361 per-cell afatinib predictions do NOT separate HER2+ vs HER2- subpopulations
  (ERBB2>median split: pred AUC 0.807 vs 0.808, MWU p=0.071) - the transfer model carries no
  HER2-specific signal, while the biomarker (ERBB2 level itself) is what the wet-lab-validated
  biology tracks.
- Ridge coefficients are tiny and diffuse (max |w| ~ 0.002 across 2000 HVGs); top-weighted genes
  include GRB7 (ENSG00000141738, 17q12 HER2 amplicon) but with negligible weight - no dominant
  driver-gene signal survives bulk->sc transfer.

## Payload (candidate for the program task-type map)
Cross-platform transfer fails where the signal is a small set of dosage/cis-driven loci:
bulk-trained genome-wide regression dilutes the HER2-amplicon signal that a 2-gene biomarker
preserves, and per-gene quantile alignment cannot recover it (alignment +0.05 over naive).
Per-cell aggregation (DREEP-style) inherits the same dilution. At 25-line evaluation scale with
a strong published biomarker, transfer learning is strictly dominated by the mechanistic baseline -
consistent with the 026/027 out-of-domain rule: mechanistic baselines win out-of-domain.

## Prospective lab nomination (locked, G5)
A breast-cancer functional-genomics unit running scRNA + drug screens (HER2-heterogeneity studies):
the tool (tools/drep_predict.py) is delivered with the negative-result caveat; recommend the
biomarker arm, not the transfer arm, for any prospective use.

## Tool (G5)
tools/drep_predict.py - CLI per-line + per-cell prediction; smoke-tested on the atlas (32 lines).
Local artifacts (bulk_expr.npz, xcell_sparse.npz, line_of.npy, atlas_pseudobulk.npz) in results/local/ (gitignored).
