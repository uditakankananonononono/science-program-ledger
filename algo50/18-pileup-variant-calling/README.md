# algo50/18 - Beta-binomial vs fixed-threshold pileup for diploid SNP calling (simulated ground truth)

Lane RES-2. Algorithm study (not counted toward the flagship 100). Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`).

## Bottom line
- At 30x both callers saturate: fixed-threshold het F1 0.9987 vs beta-binomial 0.9995, zero false positives on 281k non-variant sites. The locked +0.02 margin gate FAILS - there is no headroom. Calling SNPs at 30x with clean reads is solved; method choice does not matter.
- The methods separate exactly where expected: at 8x BB het recall 0.737 vs FT 0.519 (precision 0.991 vs 0.998); at 4x (pivot) BB het F1 0.513 vs 0.175 (both precision ~0.97), zero FPs. All pivot gates PASS.
- Honest asymmetry: at 4x FT keeps higher hom-alt recall (0.56 vs 0.34) - BB's 0.9 posterior threshold is conservative exactly when reads are scarce.

## Data
Simulated on NC_000913.3 (sha256 `data/sites.npz` + `results/pileup_*.npy`): 2000 het + 1000 hom-alt SNPs (>=50 bp spacing) + 281,066 non-variant control sites; 300 bp reads, 1% substitution, 30x/8x/4x, seed 1.

## Gates
- G1 FAIL: 30x BB 0.9995 < FT 0.9987 + 0.02 (ceiling, no headroom; predicted in protocol).
- G2 PASS: BB FP 0 <= FT FP 0. - G3 PASS: 8x BB recall 0.737 >= 0.519+0.05, prec 0.991.
- G4 PASS: 30x BB hom-alt recall 0.999.
- Pivot (4x): P1 PASS (+0.34 F1), P2 PASS (0.968), P3 PASS (0 FP).

Original project FAILS G1 (documented ceiling); pivot PASSES. Net: likelihood callers earn their complexity only below ~10x.

## Caveats
- No mapping error, indels, or base-quality variation - best case for both; real callers win their keep on messier data.
- Priors fixed at 0.001/0.0005; a variant-dense genome would shift BB's operating point.

## Reproduce
`python3 code/run.py` (needs numpy, biopython; ~15 s).
