# algo50/11 - Finding nuclear localization signals: classical regex vs a learned window scanner

Protocol and gates locked before scoring: PROTOCOL.md, results/lock.txt (2026-09-23T21:11:20Z; Amendment 1 was a memory fix made before any output). Data: UniProt 2026_03, 289 proteins with 344 experimentally mapped NLSs (ECO:0000269 only), 256 families; 1126 experimentally secreted human proteins as a control. 5-fold CV grouped by protein family.

## Results (results/metrics.json)
| method | residue AUPRC | segment recall | segment precision | segment F1 | secreted proteins flagged |
|---|---|---|---|---|---|
| M0 classical regex (pat4/pat7/bipartite) | point: P 0.33, R 0.51 | 0.71 | 0.44 | 0.546 | 40.1% |
| M1 learned 15-aa scanner | 0.282 | 0.46 | 0.45 | 0.454 | 17.4% |
| M2 K+R density | 0.207 | 0.37 | 0.34 | 0.356 | 13.9% |
Residue base rate 1.9%.

## Gates
- G1 PASS: M1 AUPRC beats basic-residue density by +0.074 (95% CI 0.058 to 0.092).
- G2 FAIL: M1 segment F1 is 0.092 BELOW the regex rules (95% CI -0.142 to -0.044). The classic patterns find far more of the real NLSs (71% vs 46%) at the same precision.
- G3 PASS: M1 flags 17% of secreted proteins vs 40% for the regex.

## What this means
The old regex rules are still the better finder of experimentally mapped NLSs: a small learned scanner does not beat them on recall at equal precision. The regex's cost is specificity: it fires on 40% of secreted proteins that should never enter the nucleus, versus 17% for the scanner. So the scanner is a better filter and the regex is a better net; neither wins outright, and the locked headline gate (G2) is an honest negative.

## Caveats
- Unannotated real NLSs inside positive proteins count as false positives for every method, so precisions are lower bounds.
- 344 segments is small; the scanner may be data-limited. M1's threshold was tuned on training folds for F1; the regex has no threshold.
- Secreted-protein flag rate is a proxy for false alarms, not a measured false-positive rate.

## Reproduce
python3 code/parse.py && python3 code/run.py  (about 10 min on 2 cores)

## Post-hoc pivot (Amendment 2, locked before scoring; results/pivot_metrics.json)
Cascade M3: keep a regex hit only if the scanner also scores it highly (threshold tuned on training folds).
- Segment F1 0.566 vs regex 0.546: +0.020, 95% CI -0.0003 to 0.040. Precision rises 0.44 -> 0.51, recall drops 0.71 -> 0.63.
- Secreted proteins flagged: 31.2% vs 40.1% for regex.
- P1 FAIL (needed +0.03 with CI above 0). P2 FAIL (needed <= 20.1%).
The cascade is a small, borderline improvement, not a clear win. Project 11 closes as a documented negative: on experimentally mapped NLSs, a small learned scanner does not beat the classical regex rules, and gating the regex with it only trims a little noise.
