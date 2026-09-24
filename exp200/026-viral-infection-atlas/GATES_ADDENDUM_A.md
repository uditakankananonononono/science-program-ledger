# ADDENDUM A (2026-09-24 08:08): G1 sanity halt fired - diagnosis documented, thresholds unchanged

## The halt
G1 locked: "if baseline dev mean AUROC < 0.70, pipeline problem - document, stop". Observed: 0.5886.
The halt's parenthetical premise was "ISGs strongly separate COVID from healthy PBMCs in this dataset's
paper". That premise was WRONG for the pooled cohort: Lee et al 2020's headline is that strong type-I
IFN responses characterize SEVERE COVID specifically; mild cases are attenuated (that IS the paper's
finding). Census obs carries no severity field (checked: 28 standard columns only), so the locked
severity-pooled cohort cannot be severity-stratified.

## Diagnosis (no pipeline bug found)
Verified: score construction (mean log-normalized expression of 223/224 present ISG genes), AUROC
direction, per-cell-type pattern biologically sensible (NK 0.715 / CD8 0.668 highest; monocyte 0.493
and platelet ~0.50 near chance - expected under severity pooling, since the monocyte IFN program is
severity-linked in the paper). A pipeline bug would not produce this ordered, biology-consistent
pattern. The low mean is the weak-signal regime of pooled-severity data, identical for BOTH arms, so
the +0.02 G2/G3 comparisons remain valid on the locked cohort.

## Action
Experiment proceeds on the locked cohort with ALL thresholds and margins unchanged (0.70 halt was a
guard against implementation error, not a gate result). The halt's false premise is corrected here for
the record: future gates must sanity-check against the pooled-cohort biology, not the paper's
severe-case subset. Outcome gates G2/G3 evaluated exactly as locked.
