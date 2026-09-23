# DOC-2-068 The Mechanism-First Drug Fingerprint - locked gates (22:42 IST, before any data download)

## Sandbox-fit slice
LINCS L1000 perturbation signatures don't fit in 1 GB. Slice: represent each approved drug by the Reactome pathways its annotated mechanism targets sit in (ChEMBL mechanism -> UniProt -> Reactome lowest-level human pathways). No drug names, target identity or class labels are used in the representation.

## Data (public)
ChEMBL REST: mechanism (max_phase 4, direct_interaction), target (components -> UniProt accessions, human), molecule (ATC classifications). Reactome UniProt2Reactome.txt (current; human rows, R-HSA).

## Question
Does the pathway-space fingerprint recover pharmacological class (ATC level 3) BEYOND sharing a target? That is the forward-useful part: finding mechanistically similar drugs that hit different proteins.

## Protocol
Drugs: parent molecules with >= 1 human target mapped to >= 1 Reactome pathway and >= 1 ATC code. Fingerprint = binary vector over pathways; similarity = Jaccard.
For each drug: nearest neighbour by Jaccard among drugs sharing NO target UniProt with it (ties -> random, seed 0). Hit = neighbour shares any ATC level-3 code.
Null: 1000 permutations of ATC label sets across drugs (fingerprints fixed).
Comparator: nearest neighbour by target-set Jaccard across all drugs (the "target identity" baseline, reported).

## Gates
G1 no-shared-target NN precision >= 0.25.
G2 >= 3x null mean, empirical p < 0.01.
G3 >= 150 drugs evaluated (i.e. have a no-shared-target neighbour with Jaccard > 0).
Failure policy: negative preserved; pivots appended with new locked gates before computation.

## Primary result (22:45) - FAIL on G1, preserved
1,446 drugs, 1,292 pathways. No-shared-target NN precision 0.129 (< 0.25, fail); null 0.020, 6.6x, p = 0.001 (G2 pass); n = 1,391 (G3 pass). Target-identity NN baseline 0.625. Precision does not rise with pathway Jaccard (0.12 / 0.16 / 0.10 across bins), which points to generic, hub pathways dominating similarity.

## Pivot 1 (locked 22:46, before computation): specificity-weighted mechanism space
Same drugs and protocol. Fingerprint weights = IDF over drugs (log(n / drugs containing pathway)); pathways present in > 10% of drugs are dropped; similarity = cosine.
P1-G1 no-shared-target NN precision >= 0.20.
P1-G2 >= 1.3x the primary precision (0.129) and >= 5x its own permutation null (p < 0.01).
P1-G3 precision in the top similarity tertile >= precision in the bottom tertile (similarity becomes informative).

## Pivot 1 result (22:46) - FAIL, preserved
Precision 0.138 (< 0.20, fail); 1.07x primary (< 1.3x, fail); 7.0x null, p = 0.001; tertiles 0.104 / 0.201 / 0.110 (G3 technically met, non-monotonic). Closed as a documented boundary: a further re-weighting on the same data would be fishing.
