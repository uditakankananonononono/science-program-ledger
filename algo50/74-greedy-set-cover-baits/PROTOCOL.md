# algo50/74 - Greedy set cover for bait/panel design vs the (1+ln n) bound

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55).

## Question
Probe/panel design is set cover: choose few baits (k-mers) covering all targets. Greedy achieves <= (1+ln n) * OPT. On biologically-shaped instances (targets = gene families with shared k-mers), how close is greedy to the LP lower bound, and how far is random picking?

## Data (simulated, seed 61)
Universe: 200 targets in 25 families (8 each); within a family, targets share a family-specific set of k-mers (60% overlap) plus unique k-mers. Candidate baits: all distinct 25-mers appearing in >= 1 target (k-mer covers target if substring).

## Methods
- Greedy: repeatedly pick k-mer covering most uncovered targets.
- Random: random k-mers until covered (100 trials).
- Lower bound: max over targets of 1/(min cover size)... proper bound: solve fractional LP? Cheaper valid bound: LB = max over disjoint-coverage witness: use the family-structure bound: LP relaxation via simple bound |T|/max-cover-per-bait is an upper bound on LB, not valid. Valid LB: maximum matching-style: set of targets no two coverable by one k-mer (pairwise k-mer-disjoint set) - compute greedily as a valid LB.
Metrics: greedy size, random size, valid LB, ratio greedy/LB.

## Gates
- G1: greedy <= (1+ln 200)*LB always (theory check, should hold).
- G2: greedy/LB <= 2.0 on this shaped instance (greedy near-optimal in practice).
- G3: random median >= 1.5x greedy (greedy earns it).
- G4: full coverage achieved by greedy (every target covered).
PASS if G2+G3+G4.

## Failure policy
Negatives preserved; pivots via locked amendments.

---

# AMENDMENT 1 (locked before pivot run on FRESH seed 67)
Original design degenerate: 40% per-position resampling leaves ~0.6^25 ~ 3e-6 chance any 25-mer survives between family members, so every target had unique baits and cover ~= 200 (greedy/LB = 1.0 trivially, G3 uninformative). Biology has ~95-98% identical family members; 15-25-mer sharing requires that.
Pivot P (fresh seed 67): bait length 15; within-family per-position identity 0.95 (=> ~46% of 15-mers shared pairwise); 60% family-consensus positions also resampled BETWEEN families to keep cross-family sharing low.
- P1: greedy covers all 200 targets.
- P2: greedy size <= 0.6x random median (greedy earns it).
- P3: greedy/LB <= 2.0 (near-optimal on shaped instance).
- P4: family structure exploited: average targets covered per chosen bait >= 3 (vs 1.0 in the degenerate original).
PASS if all.
