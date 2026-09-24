# algo50/16 - k-mer spectrum genome-size and coverage estimation (GenomeScope-style, simulated ground truth)

Lane RES-2. Algorithm study (not counted toward the flagship 100). Protocol and Amendment 1 each hashed before the results they gate (`results/lock.txt`).

## Bottom line
- The naive error-cutoff + area estimator underestimates genome size by 12.7% at 30x (4.05M vs 4.64M) and 30% at 5x: it throws away the ~19% of k-mer instances corrupted at 1% base error and never pays them back. Primary gate G1 FAILS; G4 (5x) FAILS.
- A 2-parameter Poisson fit over multiplicities 8-50 (Amendment 1) recovers 30x size within 2.7% (4.514M) and error-thinned coverage 23.9 (expected ~24.3) - P1+P3 PASS - but still fails at 5x (-32%): at 5x the true peak sits on top of the error valley and a single-Poisson fit cannot separate them. P2 FAILS.
- Contamination robustness is real: 1% B. subtilis reads move the 30x estimate by 0.07% (G3 PASS, both estimators).
- Spectrum observation (locked protocol predicted only the error cutoff): identical single-error corruptions of the same true k-mer recur across reads, producing a real multiplicity-2 bump (536k distinct k-mers) above the main-peak height - naive "first minimum after 2" rules can mis-place the cutoff.

## Data
Simulated from NC_000913.3 (+NC_000964.3 contaminants), seed 1, 300 bp reads, 1% substitution, k=21 canonical; conditions 30x clean, 30x +1% contamination, 5x clean. Histograms in `results/hist_*.npy`.

## Results (results/results.json, results/pivot_metrics.json)
| condition | naive size | naive cov | PFIT size | PFIT lambda |
|---|---|---|---|---|
| 30x clean | 4.049M (-12.7%) | 27.4 | 4.514M (-2.7%) | 23.9 |
| 30x +1% contam | 4.046M (-0.07% vs clean) | 27.1 | 4.514M | 23.7 |
| 5x clean | 3.246M (-30.0%) | 5.6 | 3.162M (-31.9%) | 4.4 |

## Gates
- G1 FAIL: naive 30x size -12.7% (gate 10%).
- G2 PASS: naive 30x coverage 27.4 (-8.7%, gate 10%).
- G3 PASS: contamination shift 0.07% (gate <5%).
- G4 FAIL: naive 5x -30.0% (gate 20%).
- Pivot: P1 PASS (-2.7%), P2 FAIL (-31.9%), P3 PASS (23.9 in 21.1-25.9).

Original project FAILS G1/G4 (naive estimator biased low); pivot shows the model fit fixes 30x but NOT 5x (P2 FAIL). Documented boundary: k-mer spectra at 5x with 1% error do not support genome-size estimation without mixture modeling.

## Caveats
- Simulated uniform 1% substitution error; real error is clustered (ONT) or lower (Illumina/HiFi), shifting where the 5x failure kicks in.
- Haploid single genome; heterozygosity (diploid peak splitting) is the other classic failure mode, untested here.
- Poisson fit ignores repeats as a class (they inflate the right tail; least-squares on 8-50 partially absorbs them into D).

## Reproduce
`python3 code/run.py` then the PFIT block in git history (`code/run.py` + amendment block; needs numpy, scipy, biopython; ~1 min per condition, disk-bucketed counting for low RAM).
