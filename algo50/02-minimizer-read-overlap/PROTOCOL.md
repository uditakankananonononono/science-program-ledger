# algo50/02 - Minimizer sketches for long-read overlap detection across error rates

Status: LOCKED before any method-vs-method results were computed (lock time recorded in results/lock.txt, sha256 of this file).
Lane: RES-2. Class: algorithm study (not counted toward the flagship 100).

## Question
Long-read assemblers find read overlaps by shared k-mer evidence. Minimizer sketches (Roberts et al. 2004; used by minimap/miniasm) keep roughly 2/(w+1) of k-mers and are the field's default heuristic, but how much overlap signal does the sketch actually lose as sequencing error rises? Does a minimizer sketch recover true overlaps as well as exact shared-k-mer counting, and at what speed?

## Data
Reference: E. coli K-12 MG1655, NC_000913.3, fetched via NCBI efetch (timestamp + sha256 in data/).
Simulated reads, seed 1, fully regenerable from the reference: 600 reads, 200 per error stratum epsilon in {5%, 10%, 15%}; read length uniform 3000-12000 bp; start uniform over the genome; strand 50/50 (reverse-complemented reads still overlap on reference coordinates). Errors: 90% substitution, 5% insertion, 5% deletion.
Ground truth: a read pair is a true overlap iff its reference intervals overlap by >= 1000 bp.
Reads are synthetic so ground truth is exact; the reference genome is public.

## Task
All-pairs candidate overlap detection. Unit = unordered read pair (179,700 pairs). Orientation handled by canonical k-mers.

## Methods
- EK: exact canonical k-mer (k=15) sets per read; pair score = number of shared distinct k-mers (inverted-index accumulation; pairs sharing nothing score 0).
- MIN (proposed comparator of interest): minimizer sketch per read, canonical k=15, window w=10, splitmix64 hash ordering; pair score = number of shared distinct minimizers.
Both scores evaluated threshold-free (AUROC, AUPRC) and at a fixed candidate budget.

## Candidate budget
Top N pairs by score with N = 2% of all pairs (3,594 pairs). Ties broken by pair index for determinism. Recall = fraction of true-overlap pairs inside the top N.

## Strata
High-error stratum: pairs where BOTH reads have epsilon = 15%.

## Success gates (MIN vs EK)
- G1: overall recall@2% budget MIN >= 0.95.
- G2: MIN AUPRC >= 0.95 * EK AUPRC (sketch loses < 5% of ranking quality, relative).
- G3: MIN end-to-end scoring wall time <= 35% of EK wall time (same machine, single process).
- G4: high-error stratum recall@2% budget (budget recomputed within stratum as 2% of stratum pairs) MIN >= 0.90.
Project PASSES if G1, G2 and G4 pass; G3 is a secondary product gate.

## Failure policy
Negative results are recorded as-is. Per standing instruction, a failed direction triggers a documented pivot with new gates locked in an amendment before new results are inspected; the original gates are never re-scored or re-tuned.

## Notes locked in advance
- Pure Python/NumPy, 2 cores; timings are relative, not absolute.
- Repetitive genomic k-mers create false positives for both methods; no repeat masking, since masking policy would itself be a tunable.
