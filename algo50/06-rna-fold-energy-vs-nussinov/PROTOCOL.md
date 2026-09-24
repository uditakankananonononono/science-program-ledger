# algo50/06 - Simplified stacking-energy DP vs max-base-pair Nussinov for RNA secondary structure

Status: LOCKED before any method-vs-method results were computed (lock time recorded in results/lock.txt, sha256 of this file).
Lane: RES-2. Class: algorithm study (not counted toward the flagship 100).

## Question
Does adding a simplified nearest-neighbor stacking energy model to RNA folding DP actually recover more real structure than the textbook max-base-pairs Nussinov algorithm, on curated covariation-derived structures? And does the energy model invent spurious structure on shuffled sequences?

## Data
Rfam 15.1 seed alignments (ftp.ebi.ac.uk/pub/databases/Rfam/15.1/Rfam.seed.gz; timestamp + sha256 in data/): RF00005 (tRNA) and RF00001 (5S rRNA). Consensus structure from SS_cons. Per sequence, reference pairs = consensus pair columns where the sequence has ACGU at both. Sequences with non-ACGU chars dropped; exact duplicates dropped; 100 sequences sampled per family (seed 1; all if fewer).

## Task
Per-sequence base-pair prediction. Precision/recall/F1 against the sequence's reference pairs, averaged per family.

## Methods (all min loop length 3, i.e. pairs only if j-i >= 4)
- NUSS: Nussinov max-pairs DP; canonical pairs GC, AU, GU each scoring 1.
- WC (baseline): same DP, GU pairs disallowed.
- ENERGY (proposed): minimization DP, simplified stacking model.
  pairE: GC -3.0, AU -2.0, GU -1.0.
  hairpinE(l) = 4.0 + 0.5*l.
  stackE(outer pair type, inner pair type): GC-GC -3.0; GC-other -2.5; AU-GC -2.0; AU-AU -1.5; AU-GU -1.0; GU-any -0.5.
  Recurrences: V(i,j) = pairE + min(hairpinE(j-i-1); stackE + V(i+1,j-1) if inner pairable; W(i+1,j-1)); W(i,j) = min(W(i+1,j), W(i,j-1), min_k W(i,k)+W(k+1,j), V(i,j)); empty structure scores 0. Interior loops/bulges free, multiloops unpunished: documented simplification, NOT Turner-complete.
- Specificity control: ENERGY on dinucleotide-shuffled tRNAs (seed 1), median predicted pair count vs real.

## Success gates
- G1: tRNA mean F1 ENERGY >= NUSS + 0.03.
- G2: 5S mean F1 ENERGY >= NUSS + 0.03.
- G3 (sanity): NUSS mean recall on tRNA >= 0.40 (textbook expectation: roughly half the pairs).
- G4 (specificity): ENERGY median predicted pairs on shuffled tRNAs <= 1.25x its median on real tRNAs.
Project PASSES if G1 and G2 pass; G3/G4 are sanity/specificity gates, reported either way.

## Failure policy
Negative results are recorded as-is. A failed direction triggers a documented pivot with new gates locked in an amendment before new results are inspected; original gates are never re-scored or re-tuned.

## Notes locked in advance
- Reference pairs come from covariation-annotated consensus structures, not crystal structures; some "wrong" predictions may be real in specific sequences.
- Pseudoknots in the reference (Rfam SS_cons may nest <([ ) are all kept as reference pairs; the DPs cannot predict crossing pairs, capping achievable recall.
