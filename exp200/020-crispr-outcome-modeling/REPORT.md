# DOC-1-020 REPORT - Fine-Tuning Evo 2 for Gene Editing Guide Design (feasible arm)
EXP-1, 2026-09-24. GATES.md locked 07:09 BEFORE label parsing; ADDENDUM A (07:09, label redefinition for mirror data) and ADDENDUM B (07:10, source switch to inDelphi supplement, supersedes A) both locked before the outcomes they govern. VERDICT: G1 PASS, G2 SPLIT (U2OS transport PASS / designed-library FAIL), G3 PASS - documented boundary on library-design transport, submitted for adjudication.

## What the topic named vs what ran
Topic: fine-tune Evo 2 for guide design. Evo 2's smallest checkpoint (evo2_1b_base, 1B) cannot be fine-tuned on 2 CPU/1.9GB (parent-approved pivot 07:07, with the constraint to stay distinct from algo50/43's Doench efficiency scorer). Executed arm: Cas9 repair-OUTCOME COMPLEXITY modeling (unique indel count per guide) from 55nt local context - different label family, data (inDelphi LibA, Shen 2018), and baseline (Bae 2014 MH score) from 43. A precise/complexity predictor is the design-relevant property (choose guides with clean outcomes for templated editing).

## Gate results
- G1 (dev LibA mESC, 5-fold CV seed 7): ridge Spearman 0.783 vs Bae MH score -0.328: PASS by a wide locked margin. The Bae score anti-correlates with complexity - mechanistically correct (strong microhomology channels repair into one dominant deletion, i.e. PRECISE outcomes) - so the baseline carries real inverse signal; the model roughly doubles its |rho|.
- G2 (frozen, fit on dev only, single pass): U2OS cross-cell-type transport 0.657 (bar 0.45, Bae -0.240): PASS. Designed-library transport (Table 3, MMEJ-repeat constructs) 0.279 vs Bae +0.336: FAIL - the model LOSES to the raw MH score on the designed library. G2 FAIL as locked (both sets must pass).
- G3 (mechanism): corrected feature audit (context is 55nt, cut at 27|28): the Bae MH score is the #1 feature (-0.19, suppresses complexity), MH pattern count #2 (+0.07, competing paths raise complexity), MH max length #11. Dinucleotide composition and GC secondary. Literature-consistent (Bae 2014; Shen 2018; Allen 2019).
- G4: predict_precision.py CLI (55nt context -> predicted log1p complexity + class + Bae score) smoke-tested on 3 locked dev contexts (ordering consistent: MH 79 -> 4.57 low; MH 33 -> 5.44 medium); Parts lab (Sanger) nomination.

## The boundary finding
Outcome-complexity models transport across CELL TYPES on the same library (mESC -> U2OS, 0.657) but NOT across library DESIGNS (random-library model -> designed MMEJ-repeat library, 0.279 < Bae 0.336). On MH-engineered sequences the MH score itself flips sign (+0.336): the semantics of microhomology depend on the sequence regime. Third generalization boundary in the program (010 transported, 019 and now 020-arm did not) - library/cohort design is the confound that keeps deciding what transports.

## Honest limits
Complexity = count of unique observed indels (presence-level), not read-frequency-weighted entropy; readcount confounds complexity (deeper sequencing sees more classes - median 433k reads LibA vs 13.7k T3, which is part of why T3 transport fails, flagged not corrected); ridge is linear - interactions (MH x position) unmodeled; U2OS and T3 frozen sets come from the same publication.
