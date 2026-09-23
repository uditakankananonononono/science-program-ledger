# DOC-1-001 — Baseline transcriptomics predicts drug response: a 30-drug locked-gate map (EXP-1)

**Status: G1 PASS (useful result), G2 FAIL (honest negative, preserved), pivot P1/P2: PASS/PASS**

## One-line
Across 30 pre-registered high-variance GDSC2 drugs, baseline gene expression (DepMap 24Q2)
predicts ln IC50 with a median 21.1% RMSE reduction over a drug-mean baseline, and all
30 drugs beat a 20x permutation null (p<=0.048) in cell-line-disjoint CV (median CV R^2 ~0.37).

## What was locked and what happened
- G1 (primary): PASS — median relative RMSE reduction 0.211 (gate >=0.05); 30/30 drugs
  permutation-significant (gate >=50%).
- G2 (boundary hypothesis): FAIL — targeted drugs are NOT more predictable than
  cytotoxics (median R^2 0.376 vs 0.369, Mann-Whitney p=0.187). Pathway class does not
  stratify predictability. Negative preserved; no re-fishing.
- Pivot (GATES-v2, locked before pivot computation): is the signal just lineage? BOTH PASS -
  lineage-only models achieve only 9.7% median RMSE reduction vs the expression model's
  21.1% (extra-lineage margin 11.5 points, gate >=5), and the margin is positive for
  30/30 drugs (gate >=50%). The G1 claim survives lineage control.

## Payload
1. Per-drug predictability map for 30 drugs (n=405-705 lines each) — which responses a
   baseline transcriptome can and cannot read (results/per_drug_metrics.csv).
2. Boundary result: predictability is not a targeted-vs-cytotoxic property.
3. Tool: predict.py — (expression vector, drug) -> predicted ln IC50/IC50 uM with
   Mahalanobis-distance abstention (results/tool_model.pkl; acceptance: >50% missing
   model genes -> abstain; out-of-distribution -> abstain flag).

## Caveats
Cell lines, not organoids — the virtual-organoid framing reduces to its testable core on
a 2-CPU/2GB sandbox; transport to patient-derived organoid screens is the named next
experiment. Permutation floor p=0.048 (compute-bounded, declared in gates). Ridge-only:
this is a calibrated baseline map, not a generative model.

## Provenance
results/provenance.md — GDSC2 xlsx SHA-256 + DepMap 24Q2 figshare MD5s, gate-file hashes
locked before outcomes.
