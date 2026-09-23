# Amendment 1 - past the codon ceiling: which sequence features carry abundance information beyond codon bias (locked before these results were computed)

## Outcome of the original protocol (not re-scored)
G1 PASS: label-free SC-CAI matched or slightly beat ribosomal-reference CAI on all three datasets (+0.005 rho each, paired CIs excluding 0). G2 PASS: converged in 4 iterations, and its 101-gene reference is 68% ribosomal proteins, with glycolytic genes (TDH1-3, PDC1, ENO1/2, FBA1, TPI1) and TEF1/2 filling most of the rest. G3 FAIL: a supervised 59-codon ridge model beat CAI-RP by only +0.016 (Kulak) and +0.032 (Mueller), under the +0.05 gate. On genes absent from the training dataset it did not beat CAI-RP on Kulak (0.524 vs 0.542).
Reading: synonymous codon usage looks saturated. Once a single adaptation axis is captured, extra codon-level flexibility adds almost nothing.

## New direction
Test whether non-codon sequence features carry abundance information that codon bias does not. Same 5-fold gene-level CV, trained on Ghaemmaghami labels, ridge, evaluated on Kulak and Mueller.
Feature blocks: R = 59 relative codon frequencies (the G3 model); L = log10 CDS length; A = 20 amino-acid composition fractions; H = SC-CAI of codons 2-50 minus whole-gene SC-CAI (5' ramp).
Models: S2 = R+L+A+H; ablations S2-minus-each-block and single blocks.

## Gates
- A1: S2 rho >= CAI-RP rho + 0.05 on both Kulak and Mueller, paired bootstrap 95% CI excluding 0.
- A2: on the genes absent from Ghaemmaghami (clean holdout), S2 (fit on all Ghaemmaghami genes) beats CAI-RP on both Kulak and Mueller.
- A3 (mechanism, descriptive with a threshold): at least one non-codon block (L, A or H), when removed from S2, lowers Kulak rho by >= 0.02.
