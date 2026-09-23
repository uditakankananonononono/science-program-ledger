# DOC-1-004 — Gut microbiome digital twin: genus composition reads 20/30 metabolites; species resolution makes it WORSE

**Status: G1 genus-level FAIL on effect size (7.5% vs 10% gate) with 20/30 permutation-significant; G1-v2 species-level FAIL harder (-6.5%); candidate boundary-map result, adjudication requested.**

## What happened (all gates locked pre-outcome)
- Genus level (220 paired FRANZOSA_IBD_2019 samples, subject-disjoint 5-fold CV,
  subject-level permutation nulls): genus composition significantly predicts 20 of the
  30 highest-variance detectable fecal metabolites (20x null, p<=0.048), median RMSE
  reduction 7.5% (gate was 10%). Named top: urobilin R^2=0.57 (both assays of it:
  0.575/0.561); several unnamed clusters R^2 0.37-0.43. Also a hard floor: 10
  metabolites the community cannot read at all, several with deeply negative R^2.
- Species level (locked v2 pivot): prediction DEGRADES - median -6.5%, only 11/30
  significant, catastrophic overfitting on low-n metabolites (R^2 down to -12).
  Urobilin collapses from 0.57 to negative. Finer taxonomy is not a better twin at
  n=220: genus-level aggregation is where the metabolic signal lives.
- G2 (pre-registered microbial-compound classes): not evaluable - zero panel
  metabolites matched the high-confidence name list; retired honestly.

## Payload (candidate useful result)
1. The predictability ceiling map: which fecal metabolites genus composition can read,
   quantified, with a validated null (results/per_metabolite_metrics.csv + v2_).
2. Methodological boundary: species-level models overfit and underperform genus at
   this cohort size - a concrete design rule for microbiome-twin builders.
3. twin_cli.py: predicts the 20 validated metabolites from a genus profile, with
   cohort-distance abstention (smoke-tested; models only for null-passing metabolites).

## Provenance
results/provenance.md (Borenstein curated FRANZOSA_IBD_2019, SHA-256 all files).
