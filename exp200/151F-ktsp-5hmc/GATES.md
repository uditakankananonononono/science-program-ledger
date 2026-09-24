# 151F - follow-up to 151 (DOC-2-051): order-pair rules for cross-lab cfDNA 5hmC
Approved by the parent (11:17) as a fresh attack on 151's failure. Locked 2026-09-24 ~12:22 IST, before any results.
Failure being attacked: multi-gene models (0.61-0.64 external) absorbed lab and normalization batch effects; one gene transferred best (0.73).

## Data (the same as 151; checksums in 151/data/SHA256SUMS)
Train GSE89570 (Li 2017 plasma: 245 cancer vs 96 healthy). Frozen external GSE81314 (Song 2017: 49 cancer vs 15 non-cancer).

## Amendment to the proposed follow-up (disclosed)
The follow-up text proposed "anchors from external non-cancer samples". Using the external controls' labels for alignment would leak the outcome. The anchor arm is therefore label-free: per-gene median centering of within-sample ranks, using each cohort's own full sample median.

## Arms (primary fixed in advance)
- PRIMARY: k-TSP (Tan et al. 2005) on within-sample gene ranks. Pairs come from the 2,000 most variable training genes; k in {1,3,5,7,9} by 5-fold CV on training only. Pair orderings are invariant to per-sample scaling, which is the hypothesized batch source.
- Secondary (reported, not gated): label-free anchor alignment (per-cohort gene-median-centered ranks) + elastic-net, as in 151's B2.

## Baselines (from 151, recomputed identically)
One gene (SNCAIP, 0.73 external); elastic-net (Li 2017 approach, 0.64).

## Gates
- G1: primary external AUROC >= 0.80, AND >= 0.76 (+0.03 over the one-gene 0.73), AND a bootstrap 95% CI of (primary minus one-gene) with a lower bound > -0.05 (i.e., not clearly worse).
- G2: the primary's training-CV AUROC >= 0.75. The external must not be carried by a weak in-lab rule.
- G3 (mechanism): the k-TSP pair genes overlap 158's top-30 shared cancer axis (hepatocyte-dominated) with hypergeometric p < 0.05. The literature link is liver as a variable cfDNA contributor (Moss et al. 2018, Nat Commun, cfDNA methylation atlas).
- G4: scorer tool, plus a nomination (the top pair as a two-gene 5hmC ratio assay).
- PASS = G1-G4. Otherwise a boundary. No change of arms or k grid after results.
