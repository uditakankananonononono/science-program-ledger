# 157F - follow-up to 157 (DOC-2-057): order-flip negative space
Approved by the parent (11:17) as a fresh attack on 157's failure. Locked 2026-09-24 ~12:20 IST, before any results.
Failure being attacked: 157's regression-residual coupling score did not transport (GSE9452 0.46), while the order-based k-TSP was stable. Hypothesis: negative space written as broken orderings (not broken regressions) keeps its signal and transports.

## Task (same as 157)
Quiescent UC mucosa (remission / uninflamed / no macroscopic inflammation) vs control.
- Train: GSE87466 (UC vs normal, as in 157).
- Externals, gated: GSE38713 (remission + non-involved vs controls), GSE9452 (no macroscopic inflammation vs controls), and the NEW cohort GSE59071 (GPL6244): inactive UC (23) vs controls (11).
- Reported, not gated (tiny): GSE16879 UC responders after infliximab (healed) vs colon controls.

## Method (fixed)
- Genes: common to all cohorts, within-sample percentile ranks. Candidate pairs: the top 1,000 most variable training genes.
- Stable pair: gene A > gene B in >= 95% of training normals.
- Selection: the 100 stable pairs with the largest training flip-rate difference (UC minus normal).
- Score = fraction of the selected pairs flipped in the sample.

## Baselines
- k-TSP (Tan et al. 2005, Bioinformatics), with 157's exact implementation and CV-chosen k.
- 157's broken-coupling score, for reference.

## Gates
- G1: AUROC >= 0.75 in each of the 3 gated externals, AND mean over them >= k-TSP mean + 0.03.
- G2 (new frozen cohort): GSE59071 AUROC >= 0.75 and >= k-TSP. This is the frozen external on a new platform.
- G3 (mechanism): genes in the selected pairs are enriched (hypergeometric p < 0.01 vs candidate genes) for Hallmark FATTY_ACID_METABOLISM, OXIDATIVE_PHOSPHORYLATION or INFLAMMATORY_RESPONSE. The literature link is epithelial energy-metabolism loss in UC (Roediger's butyrate hypothesis) and residual inflammation.
- G4: a CLI scorer, plus a prospective nomination (the single most discriminative stable pair, proposed as a two-gene qPCR ratio test for quiescent UC).
- PASS = G1-G4. Otherwise a boundary. No changes after results.
