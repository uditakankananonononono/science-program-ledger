# algo50/62 - Local (Smith-Waterman) vs global (Needleman-Wunsch): domain-detection sensitivity

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55).

## Question
When a short conserved domain is embedded in long unrelated flanks, local alignment finds it while global alignment dilutes it. Quantify: score of the embedded domain under both algorithms, and the score distribution on unrelated sequence pairs (null), as a function of domain identity and flank length.

## Data (simulated, seed 19)
Domain length 60; flank length F in {0, 200, 1000}; domain identity in {0.6, 0.8, 1.0} (mutation rate 1-identity, substitutions only). 300 pairs per cell + 300 unrelated pairs (independent random, same lengths) for the null.
Sequences length 60+2F: query = flank1+domain+flank2; subject = independent flanks + mutated domain copy.

## Methods
Implement NW (global) and SW (local) DP, scoring +2/-1/-2 (match/mismatch/gap), from scratch; sanity: SW score on identical domain-only pair = 120; NW on same = 120.
Metrics: median SW and NW score per cell; null 95th percentile; "detected" = score > null95.

## Gates
- G1: sanity checks pass exactly (identical domain-only: SW=NW=120; SW >= NW always, since local is global with free end gaps... verify empirically SW>=NW on all pairs).
- G2: at identity=0.8: SW detects the domain in >= 95% of pairs at all flank lengths.
- G3: at identity=0.8, F=1000: NW detects <= 30% of pairs (dilution demonstrated).
- G4: on null pairs, SW false-positive rate at null95 threshold ~5% (0.03-0.08) - threshold sanity.
PASS if all.

## Failure policy
Negatives preserved; pivots via locked amendments.

---

# AMENDMENT 1 (locked before any pivot scoring)
Pure-Python DP cannot complete 300 pairs/cell at F=1000 within compute budget (est. 13 min). Amendment: (a) numpy anti-diagonal vectorization of the identical recurrences (no affine gaps); (b) N per cell = 120 (F=0), 60 (F=200), 30 (F=1000); null sets same sizes. Thresholds unchanged. Detection-rate CIs widen at F=1000 (+/-1/30 quantization); reported. The abandoned pure-Python run's partial output (F=0 and one F=200 cell) is discarded; pivot scores come only from the vectorized implementation.

---

# AMENDMENT 2 (locked before pivot scoring)
G2+G3 failed and the failure is the finding: against length-matched nulls, local and global detection power are nearly identical (F=1000,i=0.8: SW 0.43 vs NW 0.37) because the null score distribution shifts up with sequence length for both. The textbook local-vs-global difference is about LOCALIZATION, not raw detection.
Pivot P: measure localization. SW best alignment (traceback from argmax) vs true domain interval on F=1000 cells.
- P1: at i=0.8 and i=1.0, the SW interval covers >= 50% of the true 60 bp domain in >= 90% of pairs.
- P2: NW precision for the domain <= 10% by construction (domain is 60/2060 of the forced full-length alignment) - reported as the localization cost of global alignment.
PASS if P1.
