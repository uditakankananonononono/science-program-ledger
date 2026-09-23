# DOC-1-011 REPORT - Discovering Novel CRISPR Systems with Protein Language Models
EXP-1, 2026-09-24. Gates locked BEFORE outcomes (GATES.md commit 983f96f; Addendum A commit c3ce3300, feasible pool definitions, all thresholds unchanged). VERDICT: DOCUMENTED BOUNDARY - headline gate G1 FAILED; failure tree followed (single scoring passes, no new arms, no threshold changes).

## Pools (GATES + Addendum A; PROVENANCE.md)
Seeds: Cas9 n=150, Cas12a n=12, Cas13a n=20 (reviewed+unreviewed UniProtKB protein_name families). Dev: held-out family members n=239 (Cas9 200, Cas12a 15, Cas13a 24) vs 1,800 decoys (1,500 bacterial + 300 hard nuclease/polymerase). Frozen: 300 post-2022-01-01 deposits (name-filtered Cas9/12/13, 298/1/1 family mix - post-2022 deposits are overwhelmingly Cas9; documented) vs 300 fresh bacterial decoys. 2,821 ESM-2 t6_8M embeddings (cap 3,000).

## Results (single scoring passes; results/gate_scores.json)
- Dev: PLM AUROC 0.9228 (per-family: Cas9 0.949, Cas12a 0.954, Cas13a 0.906) vs MMseqs2 AUROC 0.9891. G1 (PLM strictly beats MMseqs2): FAIL (-0.066).
- Frozen temporal validation: PLM AUROC 0.9806 (bar >= 0.80) with drop vs dev -0.058 (bound <= 0.10): G2 PASS. MMseqs2 frozen 0.9949 (also above PLM).
- G3: nearest-centroid assignments - Cas9 held-out 186/200 correct, Cas12a 12/15, Cas13a 11/24 (10 assigned Cas12a). PCA (results/pca_dev_cas.csv): PC1 40.5% variance separates Cas9 from Cas12a/Cas13a; Cas12a and Cas13a clusters overlap. Interpretation: Cas9 is phylogenetically/structurally distinct (large multi-domain DNA nuclease); Cas12a and Cas13a are both compact single-effector class-2 RNA-guided nucleases with shared RecA-like recognition scaffolds (Makarova 2020), and with tiny Cas12a/13a seed sets (12/20) the centroids are noisy - the embedding space captures broad class-2 architecture more than subtype identity. G3: incoherence specifically explained: PASS as documented.
- G4: code/crispr_finder.py CLI (FASTA -> effector score + nearest family), smoke-tested on held-out and frozen sets. Nomination: Innovative Genomics Institute metagenome-mining program.

## Boundary analysis (why this matters)
The discovery-engine hypothesis fails at the 8M-parameter scale FOR THIS TASK SHAPE: for retrieval of well-conserved known families (Cas9/12/13 have deep alignable homologs), cheap sequence search (MMseqs2) already saturates (0.989-0.995) and PLM embeddings add nothing. The PLM's frozen-set 0.981 shows it DOES generalize across the 2022 annotation cutoff - its information is real but redundant with sequence similarity where similarity exists. Implication for the program: PLM-based discovery is only worth testing where sequence signal is ABSENT (remote homologs < 25% identity, novel folds, de-orphanization), not on alignable families. A future experiment testing PLM retrieval on remote-homology-only pools (sequence-identity-filtered) would be a DIFFERENT hypothesis needing its own locked gates; it is not an arm of this one.

## Honest limits
Cas12/13 UniProtKB scarcity forced small seeds (12/20) and small held-out n (15/24); frozen positives are 99% Cas9. Frozen freeze is on annotation date; some source sequences may have existed pre-2022 in metagenomic DBs (stated in gates). MMseqs2 -s 7.5 sensitive mode used for the baseline (strong, fair).
