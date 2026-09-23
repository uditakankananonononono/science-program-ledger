# algo50/19 - Finding transmembrane helices: Kyte-Doolittle hydropathy window vs a learned window scanner

Protocol and gates locked before scoring (PROTOCOL.md, results/lock.txt). UniProt reviewed proteins with 3D structure: 719 membrane proteins, 4303 helices whose TM annotations all carry structure/experimental evidence (predictor-only labels excluded), 395 families; 1500 soluble human structures as a false-call control. 5-fold CV grouped by family.

## Results (results/metrics.json)
| method | segment F1 | recall | precision | exact TM count | soluble proteins falsely flagged |
|---|---|---|---|---|---|
| KD published rule (19-aa window >= 1.6) | 0.636 | 0.48 | 0.95 | 19.1% | 1.5% |
| M1 learned 21-aa scanner | 0.911 | 0.93 | 0.89 | 40.3% | 23.3% |
| KD, threshold tuned on training folds (secondary, not gated) | 0.879 | 0.90 | 0.86 | 40.3% | 44.1% |

## Gates
- G1 PASS: segment F1 +0.275 over the published KD rule (95% CI 0.258 to 0.292).
- G2 FAIL: the scanner falsely flags 23.3% of soluble proteins vs 1.5% for KD at 1.6.
- G3 PASS: exact TM-count accuracy +0.213 (CI 0.171 to 0.252).

## What this means (read with the secondary row)
Most of the headline gain comes from the threshold, not the model. The published 1.6 cut-off is very conservative on these structures: it misses half the helices but almost never fires on soluble proteins. Simply re-tuning KD's threshold recovers most of the F1 (0.879) and all of the count gain (40.3%). Against tuned KD, the learned scanner adds a modest +0.03 F1 and halves the soluble false-call rate (23% vs 44%). So the learned scanner is the better trade-off at high recall, while the classic 1.6 rule remains the high-precision choice. Gates G1 and G3 pass as locked, but the size of the "learning" benefit is much smaller than they suggest. That's disclosed here rather than left implied.

## Caveats
- Exact TM count stays low for every method (<= 40%). Adjacent helices merge and long helices split. Counting was not the design target.
- Negatives are human soluble structures while positives span all organisms.
- Segment matching needs >= 5 residues of overlap.

## Reproduce
cd code && python3 parse.py && python3 run.py (~3 min on 2 cores)
