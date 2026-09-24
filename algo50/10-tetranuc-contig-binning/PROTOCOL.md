# algo50/10 - Tetranucleotide composition for metagenomic contig binning

Status: LOCKED before any method-vs-method results were computed (lock time in results/lock.txt, sha256 of this file).
Lane: RES-2. Class: algorithm study (not counted toward the flagship 100).

## Question
In metagenomic binning, tetranucleotide frequency (TETRA) is the classic composition feature. Against simple GC and shorter k-mers, how much better does TETRA assign contigs to their source genome, and how fast does it degrade at short contig lengths?

## Data
Three complete genomes (distinct GC: ~51%, ~44%, ~66%): NC_000913.3 E. coli, NC_000964.3 B. subtilis, NC_000962.3 M. tuberculosis (NCBI efetch GenBank; sha256 in data/, same accessions as algo50/04 downloads). Fragment each into non-overlapping 5 kb contigs (tail dropped), and separately into 1 kb contigs. Per genome, contigs split into halves A (centroid training) and B (test), alternating.

## Task
Per-contig assignment to one of the three genomes. Accuracy on B-half contigs with A-half centroids.

## Methods
- GC: contig GC fraction; nearest centroid in 1-D.
- K2/K3/K4: canonical k-mer frequency vectors (forward + revcomp merged), TETRA-style z-scores per k-mer ((obs - exp)/sqrt(exp), exp from contig mononucleotide... locked simplification: exp from the contig's own mononucleotide product), assignment by highest Pearson correlation with genome centroid z-vector.

## Success gates
- G1: 5 kb K4 accuracy >= GC accuracy + 0.30.
- G2: 5 kb K4 accuracy >= K2 accuracy + 0.10.
- G3: 1 kb K4 accuracy >= 0.70 (length-degradation boundary).
- G4: 5 kb K4 accuracy (A-centroid on B) >= 0.95x the same-half (A on A, 2-fold) accuracy (within-genome composition is stable).
Project PASSES if G1 and G2 pass; G3/G4 boundary/stability gates reported either way.

## Failure policy
Negative results recorded as-is; failed direction triggers a documented pivot with gates locked in an amendment before new results are inspected.

## Notes locked in advance
- Three genomes with deliberately spread GC; real communities with close relatives will be far harder (GC gate margin is partly free signal).
- Contigs are clean single-genome fragments; no strain mixture, no assembly error.
