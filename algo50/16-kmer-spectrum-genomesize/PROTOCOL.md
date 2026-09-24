# algo50/16 - k-mer spectrum genome-size and coverage estimation (GenomeScope-style, simulated ground truth)

Status: LOCKED before any method-vs-method results were computed (lock time in results/lock.txt, sha256 of this file).
Lane: RES-2. Class: algorithm study (not counted toward the flagship 100).

## Question
From the k-mer count spectrum of an error-prone read set, can a simple error-cutoff + area method recover genome size and mean coverage accurately, and how does it degrade with contamination and low coverage?

## Data (simulated, ground truth known)
E. coli K-12 reference NC_000913.3 (as algo50/04; sha256 in data/). Reads: 300 bp, seed 1, uniform starts, 1% substitution error. Conditions: (a) 30x clean; (b) 30x + 1% reads drawn from B. subtilis NC_000964.3 (contamination); (c) 5x clean. k=21 canonical.
Method: histogram of k-mer multiplicities (hash-table counting, 2-bit encoding). Error cutoff = first local minimum of the spectrum between multiplicity 2 and the main peak (locked: multiplicity 3 if no local minimum found). Genome size estimate = (total k-mers with multiplicity >= cutoff) / (spectrum-weighted mean multiplicity of k-mers >= cutoff). Coverage estimate = that mean multiplicity. No GenomeScope model fitting - the naive estimator is the object of study.

## Success gates
- G1: 30x clean genome-size estimate within +/-10% of 4,641,652.
- G2: 30x clean coverage estimate within +/-10% of 30.
- G3: 1% contamination changes the genome-size estimate by < 5% relative to clean.
- G4: 5x clean genome-size estimate within +/-20%.
Project PASSES if G1 and G2 pass; G3/G4 boundary gates reported either way.

## Failure policy
Negative results recorded as-is; failed direction triggers a documented pivot with gates locked in an amendment.

## Notes locked in advance
- Repeats (rRNA etc.) inflate high multiplicities and are expected to bias the naive estimator slightly high on size; documented, not corrected.
- 1% substitution error is mild vs real ONT/HiFi; the estimator's error-cutoff behavior at high error is untested here.
