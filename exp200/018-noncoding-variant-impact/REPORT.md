# DOC-1-018 REPORT - Predicting the Impact of Non-Coding Variants
EXP-1, 2026-09-24. GATES.md locked 06:41 BEFORE outcomes; ADDENDUM_P1 locked 06:52 before P1 outcomes; ADDENDUM_P2 locked 06:53 before P2 outcomes. Thresholds never changed after outcomes.

## What the topic named vs what ran
The topic names AlphaGenome. Access check (pre-gates): DeepMind's API is free for non-commercial use but needs a user-held key from a Google sign-in + ToS flow - a user-side action; no key in the vault. The public-data substitute arm ran instead: ClinVar non-coding SNVs on chr21 (dev) / chr22 (frozen), benchmarking against the two named published conservation baselines phyloP (Pollard 2010) and phastCons (Siepel 2005). Addendum A1 names the AlphaGenome head-to-head on the identical frozen cohort if the user obtains a key.

## Gate trail (locked failure tree followed exactly)
- G1 (dev chr21, 6-feature LR composite vs baselines, 5-fold CV seed 7): composite 0.9210 vs phyloP 0.8815 (+0.0395 PASS) vs phastCons 0.9163 (+0.0048 FAIL the +0.03 bar): G1 FAIL. Documented loss vs phastCons at genome-wide-non-coding scale.
- P1 (locked: + 64-dim 3-mer composition): 0.9097 - WORSE than the 6-feature composite (-0.011). Motif composition is noise here. FAIL, recorded as finding.
- P2 stratum (a) splice: degenerate - ClinVar chr21 splice variants are 514P/2B (99.6% pathogenic). Not a prediction problem; a classification-policy fact worth stating.
- P2 stratum (b) UTR: composite 0.7651 vs phyloP 0.6382 (+0.1269) and phastCons 0.7203 (+0.0447): BOTH locked margins PASS (G1'').
- G2 (frozen chr22 UTR stratum, model fit on chr21 UTR only, single pass, no refit): composite AUROC 0.9015 vs phyloP 0.7876, phastCons 0.8491: +0.052 over the best frozen baseline and >= 0.65 absolute: PASS. Cross-chromosome transport held (and improved with the frozen P-fraction).
- G3 (mechanism): LOFO drops on dev UTR are all <= 0.007 - no single feature indispensable; the signal is redundant across correlated conservation features. The interpretable fact is enrichment: pathogenic UTR variants sit at phastCons 0.63 vs benign 0.24 (2.6x) and window phyloP 2.32 vs 0.62 (3.7x); cCRE overlap adds nothing in UTRs (0.19 vs 0.18) - consistent with the literature that UTR pathogenicity acts through deeply conserved regulatory elements (uORFs, structure motifs), not promoter/enhancer-style cCREs.
- G4: score_variant.py CLI (chrom pos -> features + pathogenic probability from the frozen exported model) smoke-tested on 3 locked variants: chr22:17207277 (P) p=0.719, chr22:17207279 (P) p=0.889, chr22:17592497 (B) p=0.158. Prospective lab nomination: Gad Getz lab (Broad) - regulatory variant effect group.

## Verdict
Useful result on the UTR stratum: a 6-feature conservation+context LR beats both named conservation baselines by locked margins on a fully frozen cross-chromosome cohort (0.9015, +0.052 over phastCons). Equally valuable boundaries, documented under the locked tree: at whole-non-coding scale phastCons alone nearly saturates ClinVar signal (composite edge +0.005); 3-mer composition hurts; splice-region pathogenicity in ClinVar is a policy fact (99.6% P), not a learnable signal.

## Honest limits
ClinVar labels carry ascertainment/circularity (conservation-informed classifications can inflate conservation-based AUROCs - flagged, not correctable with this data); UTR stratum is small on dev (37P); research use only, not clinical; AlphaGenome comparison pending user key (A1).
