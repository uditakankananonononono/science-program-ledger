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

---

# AMENDMENT 1 (locked before pivot run on FRESH seed 59)
Original design saturated: 200 bp windows give weight-8 seeds ~99-100% hit rates even at q=0.70 (no headroom for the spaced-seed advantage), and 400 background pairs cannot measure a 0.3%/0.001% rate (expected counts ~1). Also one gate-check bug (G4 comparison direction reversed; data was monotone as expected) - fixed, documented.
Pivot P (fresh seed 59): window 60 bp; q in {0.60,0.65,0.70,0.75}; N=1000 homology, N=4000 background pairs.
- P1: spaced-8 sensitivity >= contig-8 + 0.05 at q=0.70.
- P2: contig-12 <= spaced-8 - 0.15 at q=0.70 (weight penalty of length).
- P3: background rates within 3x of theory (1/4)^w-window-corrected for the two weight-8 seeds (contig-12 underpowered, reported only).
- P4: sensitivity non-decreasing in q for all seeds (corrected check direction).
PASS if P1+P2+P4.
