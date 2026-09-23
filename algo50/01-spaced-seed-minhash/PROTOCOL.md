# algo50/01 - Reduced-alphabet spaced-seed MinHash for alignment-free protein family assignment

Status: LOCKED before any method-vs-method results were computed (lock time recorded in results/lock.txt, sha256 of this file).
Lane: RES-1. Class: algorithm study (not counted toward the flagship 100).

## Question
Alignment-free sketches (Mash/MinHash on exact k-mers) are fast but lose sensitivity once sequence identity drops into the twilight zone (<40%). Does sketching k-mers over a reduced amino-acid alphabet with spaced seeds recover protein family membership better than plain exact-k-mer MinHash, and how close does it get to Smith-Waterman nearest neighbour at what speed?

## Data
UniProtKB/Swiss-Prot reviewed human proteome (organism 9606), fields accession, Pfam xrefs, length, sequence; retrieved via rest.uniprot.org stream (timestamp + sha256 in data/).
Inclusion: exactly one Pfam accession; length 80-600; standard amino acids only. Families with >= 6 members; at most 10 members per family sampled with seed 1; at most 120 families sampled with seed 1.

## Task
Leave-one-out 1-nearest-neighbour family assignment over the sampled set. Unit = query protein.

## Methods
- SW: Smith-Waterman, BLOSUM62, gap open 11 / extend 1, score normalised by min(self-score) (reference ceiling).
- K3: exact Jaccard on plain 3-mers.
- MH3: MinHash (bottom-s, s=256) on plain 3-mers (primary comparator).
- RA-C4: MinHash s=256, Murphy-10 reduced alphabet, contiguous k=4 (ablation: alphabet without spacing).
- RA-SP (proposed): MinHash s=256, Murphy-10 alphabet, union of spaced seeds 11011 and 1101011 (weight 4 and 5).

## Strata
Twilight stratum: queries whose best same-family SW percent identity (identities / aligned columns) is < 40%.

## Success gates (proposed method RA-SP vs MH3)
- G1: overall accuracy RA-SP >= MH3 + 5 points, exact McNemar p < 0.05.
- G2: twilight accuracy RA-SP >= MH3 + 10 points.
- G3: RA-SP accuracy >= 90% of SW accuracy AND all-vs-all wall time >= 20x faster than SW.
Project PASSES if G1 and G2 pass; G3 is a secondary product gate.

## Failure policy
Negative results are recorded as-is. Per standing instruction, a failed direction triggers a documented pivot with new gates locked in an amendment before new results are inspected; the original gates are never re-scored or re-tuned.
