# DOC-1-004 — Digital twin of the gut microbiome: composition -> fecal metabolome
# GATES locked 2026-09-23 ~23:27 IST, before any outcome inspection. Lane EXP-1.
# Testable core: how much of the fecal metabolome is predictable from genus-level
# community composition, for which metabolites, and which chemical classes?

## Data (Borenstein-lab curated paired collection, Muller et al. 2022 npj Biofilms;
# github raw URLs + SHA-256 in results/provenance.md)
- FRANZOSA_IBD_2019: genera.tsv (taxonomy), mtb.tsv (metabolites), mtb.map.tsv,
  metadata.tsv (subject IDs, diagnosis). Paired samples, longitudinal per subject.

## Frozen design
- Samples: all with both taxonomy and metabolomics. Longitudinal -> SUBJECT-DISJOINT
  5-fold CV (no subject in two folds; frozen seed).
- Features: log10(relative abundance + 1e-4) of genera with >=10% prevalence, cap 200
  by mean abundance. Metabolites: log10(x + half-min) per metabolite.
- Panel rule (frozen): metabolites detected in >=50% of paired samples; if >30, keep
  the 30 with highest variance. Selection before model evaluation.
- Model: ridge (alpha by inner 3-fold CV, subject-disjoint). Baseline: metabolite
  training-fold mean.

## Success gates
- G1 (primary): median relative RMSE reduction vs baseline >= 10% across panel AND
  >=50% of panel metabolites beat a 20x subject-level label-permutation null (p<=0.05).
- G2 (boundary payload, pre-registered classes): pre-registered microbe-derived
  metabolite names (short-chain fatty acids: acetate, propionate, butyrate, valerate,
  isobutyrate, isovalerate; secondary bile acids: deoxycholate, lithocholate,
  ursodeoxycholate; tryptophan derivatives: indolepropionate, indoleacetate,
  indolelactate, tryptamine; polyamines: putrescine, cadaverine) show higher
  predictability (CV R^2) than the rest of the panel (Mann-Whitney, p<=0.05 one-sided).
- Failure policy (pivot rule): if G1 fails at genus level, pivot to species-level
  features (species.tsv, same gates, GATES-v2 locked first); if that also fails,
  pivot to disease-stratified models (IBD vs control) as the boundary question
  ("predictability collapses under dysbiosis"). Documented negatives preserved.
- Payload: per-metabolite predictability map + CLI predicting a metabolite panel from
  a genus profile with abstention.

## Reviewer questions (pre-registered)
- Longitudinal leakage? Subject-disjoint CV + subject-level permutation.
- Detection-rate bias? Panel rule frozen pre-outcome; missing values handled by the
  frozen log10(x+half-min) rule on detected values; undetected -> excluded per
  metabolite-sample pair, never imputed to zero.
