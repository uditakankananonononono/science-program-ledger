# algo50/06 - Simplified stacking-energy DP vs max-base-pair Nussinov for RNA secondary structure

Lane RES-2. Algorithm study (not counted toward the flagship 100). Protocol hashed and timestamped before scoring (`results/lock.txt`).

## Bottom line
- A simplified stacking-energy DP (pair energies + stack bonuses + hairpin penalty; interior loops free) beats max-pairs Nussinov decisively: mean base-pair F1 0.532 vs 0.289 on tRNA (+0.243) and 0.313 vs 0.203 on 5S rRNA (+0.110). Both primary gates PASS with large margin.
- The sanity gate FAILED in an informative direction: plain Nussinov recovers only 33.6% of tRNA pairs (gate was >= 40%, the textbook "about half") at 25% precision - max-pair counting folds far too much, pairing bases promiscuously. Removing GU pairs (WC) makes tRNA better (0.358) and 5S worse (0.133): GU pairs carry real signal in larger RNAs.
- Specificity holds: on shuffled tRNAs the energy model predicts a median 26 pairs vs 27 on real (gate <= 1.25x) - it does not invent extra structure on composition-preserved noise.

## Data
Rfam 15.1 seed alignments (Rfam.seed.gz, sha256 in `data/SHA256_raw.txt`, retrieved `data/retrieved_at.txt`): RF00005 tRNA (952 eligible, 100 sampled, 21 consensus pairs) and RF00001 5S rRNA (684 eligible, 100 sampled, 34 consensus pairs), seed 1. Reference pairs = SS_cons consensus pairs where the sequence has ACGU at both columns, >=80% coverage required. `data/eval.json`.

## Results (results/results.json)
| method | tRNA F1 | 5S F1 |
|---|---|---|
| NUSS (max pairs, GU allowed) | 0.289 | 0.203 |
| WC (GU disallowed) | 0.358 | 0.133 |
| ENERGY (simplified stacking) | 0.532 | 0.313 |

NUSS tRNA: recall 0.336, precision 0.254. Specificity: ENERGY median predicted pairs 27 (real) vs 26 (shuffled).

## Gates
- G1 PASS: tRNA ENERGY-NUSS = +0.243 (needed >= 0.03).
- G2 PASS: 5S ENERGY-NUSS = +0.110 (needed >= 0.03).
- G3 FAIL (sanity): NUSS tRNA recall 0.336 < 0.40 - max-pairs Nussinov is worse than the textbook expectation at precision 0.25.
- G4 PASS (specificity): shuffled/real pair ratio 0.96 <= 1.25.

Project PASSES (G1+G2).

## Caveats
- Reference structures are covariation-consensus (Rfam SS_cons), not crystal structures; crossing/pseudoknot pairs in the reference cannot be predicted by any nested DP, capping recall.
- The shuffle control permutes non-overlapping dinucleotide blocks (seed 1): it preserves block composition but is NOT a true Altschul-Erickson dinucleotide shuffle.
- The energy model is deliberately simplified (interior/bulge loops free, no multiloop penalty, three pair types): absolute F1 is not comparable to RNAfold; the comparison is NUSS vs ENERGY under identical recurrences.
- 5S F1s are low for all methods: the family has long-range pairs and few stacked runs per sequence.

## Reproduce
`python3 code/prep.py && python3 code/fold.py` (needs numpy; ~1 min).
