# ADDENDUM P2 - locked 2026-09-24 06:53 IST BEFORE P2 outcomes (invokes locked failure tree P2)
P1 result: AUROC 0.9097, margins +0.028 (phyloP) / -0.007 (phastCons): FAIL. 3-mer composition hurt
(-0.011 vs the f1-f6 composite) - motif composition is noise on this cohort; recorded as a finding.
P2 form (locked): stratum-restricted arms on the SAME f1-f6 composite, margins unchanged
(>= +0.03 vs both baselines, dev CV seed 7). Strata from the ClinVar MC consequence field:
(a) splice stratum: mc contains 'splice'; (b) UTR stratum: mc contains 'UTR'.
A stratum arm passes G1'' iff both margins >= 0.03 within that stratum.
If a stratum passes: G2 evaluates the f1-f6 composite on the same stratum of frozen chr22
(thresholds unchanged: AUROC >= 0.65 and >= max(frozen baseline AUROC)+0.01, single pass, no refit).
If no stratum passes: documented boundary - phastCons-scale conservation saturates non-coding
ClinVar signal in this envelope; the composite's consistent edge over phyloP (+0.04) but not
phastCons is the boundary statement.
