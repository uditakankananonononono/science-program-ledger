# algo50/14 - Shine-Dalgarno signal at annotated starts vs shadow ORF starts

Status: LOCKED before any method-vs-method results were computed (lock time in results/lock.txt, sha256 of this file).
Lane: RES-2. Class: algorithm study (not counted toward the flagship 100).

## Question
How discriminative is the plain Shine-Dalgarno motif (best match to AGGAGG in the -20..-5 window upstream of a start codon) between real annotated translation starts and shadow-ORF "starts" (same ORFs as algo50/04), and where is it positioned? Cross-genome: B. subtilis (canonical SD) and M. tuberculosis (reports of weaker SD usage) as boundary.

## Data
Same three GenBank genomes as algo50/04 (NC_000913.3, NC_000964.3, NC_000962.3; sha256 in data/). Positives: upstream 100 nt of each annotated CDS start (same filters as 04). Negatives: upstream 100 nt of each shadow ORF start (maximal stop-to-stop ORFs >=150 nt containing no annotated CDS; start = ORF 5' end in its reading direction), 1:1 subsample, seed 1.

## Methods
- M1: best match count (0-6) to AGGAGG over all 6-mers in window -20..-5 relative to the start codon.
- M2 (control): same score in window -60..-45.
Scoring per region; AUROC real vs shadow.

## Success gates
- G1: E. coli M1 AUROC >= 0.70.
- G2: fraction of real E. coli starts with M1 >= 5 is >= 2x the shadow fraction.
- G3 (position specificity): mean M1 over real E. coli starts >= 1.5x mean M2 over the same starts.
- G4: B. subtilis M1 AUROC >= 0.65; M. tuberculosis reported as a boundary observation (no gate).
Project PASSES if G1 and G2 pass.

## Failure policy
Negative results recorded as-is; a failed direction triggers a documented pivot with gates locked in an amendment before new results are inspected.

## Notes locked in advance
- Leaderless transcripts and atypical RBS (M. tuberculosis is known for these) depress AUROC legitimately - the boundary report is descriptive.
- Shadow ORF "starts" are stop-to-stop ORF 5' ends, not true start codons; they approximate "where a naive ORF caller would call a start".
