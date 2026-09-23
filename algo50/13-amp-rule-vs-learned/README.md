# algo50/13 - Spotting antimicrobial peptides: physicochemical rule vs learned composition model vs homology transfer

Protocol and gates locked before scoring (PROTOCOL.md, results/lock.txt). Data: UniProt 2026_03, 3376 short (10-60 aa) reviewed peptides: 1216 antimicrobial vs 2160 other secreted peptides (hormones, neuropeptides; toxins excluded). Homology-aware 5-fold CV over 830 groups (shared family or 3-mer Jaccard >= 0.3).

## Results (results/metrics.json)
| method | AUROC | AUPRC | AUROC, Cys-rich subset (n=602) |
|---|---|---|---|
| R rule: net charge x hydrophobic moment (no training) | 0.778 | 0.700 | 0.823 |
| L learned: 424 composition features | 0.701 | 0.566 | 0.614 |
| NN homology transfer (3-mer) | 0.730 | 0.612 | 0.714 |

## Gates
- G1 FAIL: L is 0.077 BELOW the rule (CI -0.127 to -0.019).
- G2 FAIL: L vs NN -0.029 (CI -0.101 to 0.041).
- G3 FAIL: L on Cys-rich peptides 0.614 (needed 0.80).

## Post-hoc pivot (Amendment 1, locked before scoring; results/pivot_metrics.json)
LP: the same logistic model on 8 physicochemical features (charge, moment, length, hydrophobic/aromatic/Gly+Pro fractions, Cys count, rule score).
- AUROC 0.817 vs rule 0.778: +0.039, CI -0.007 to 0.076. P1 FAIL (needed +0.03 with CI above 0).
- Cys-rich subset 0.634 (rule 0.823). P2 FAIL.

## What this means
Once close homologs are kept out of the test folds, the textbook cationic-amphipathic rule is hard to beat. A 424-feature composition model does worse than the rule, apparently because it learns family make-up that does not transfer. A small physicochemical model may add a few points, but not beyond noise here. The surprise: the plain rule scores best on cysteine-rich peptides (defensin-like), where amphipathic-helix reasoning was expected to fail. That is worth a follow-up but was not tested here. 13 closes as a documented negative.

## Caveats
Negatives are UniProt secreted peptides lacking the antimicrobial keyword; some may have untested antimicrobial activity. Grouping heuristic (3-mer Jaccard) is coarser than alignment clustering; the largest group has 272 peptides.

## Reproduce
python3 code/run.py && python3 code/pivot.py (a few minutes on 2 cores)
