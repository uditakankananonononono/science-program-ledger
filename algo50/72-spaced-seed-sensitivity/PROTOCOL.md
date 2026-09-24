# algo50/72 - Spaced vs contiguous seeds: sensitivity under substitution noise

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55).

## Question
A spaced seed (care positions only) tolerates mismatches at don't-care positions. Quantify the sensitivity gain of spaced vs contiguous seeds of equal WEIGHT (same number of care positions) under iid substitution noise - and the cost: spaced seeds also match more background (same weight => same random hit rate? test empirically).

## Data (simulated, seed 53)
Homology: 1000 pairs of 200bp windows at identity q in {0.70, 0.80, 0.90, 0.95}. Background: 1000 unrelated pairs.
Seeds (weight 8): contiguous 11111111; spaced 1101001101101011 (PatternHunter-style 8 of 12); long contiguous 111111111111 (weight 12, common default).

## Methods
Hit = at least one position in the 200bp window where the seed matches exactly on all care positions. Sensitivity = hit fraction on homologous pairs; background rate = hit fraction on unrelated pairs.
Theory for random pairs: P(hit at one position) = (1/4)^w for weight w.

## Gates
- G1: at q=0.80, spaced-8 sensitivity >= contiguous-8 sensitivity + 0.10.
- G2: at q=0.70, spaced-8 sensitivity >= 0.90 AND contiguous-12 sensitivity <= 0.60 (the classic PatternHunter selling point).
- G3: background hit rates within 2x of theory (1/4)^w per position for all three seeds (spaced doesn't inflate random hits beyond weight).
- G4: sensitivity strictly decreasing as q drops, all seeds (sanity).
PASS if all.

## Failure policy
Negatives preserved; pivots via locked amendments.
