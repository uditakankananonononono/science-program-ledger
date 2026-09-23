# GATES ADDENDUM A - DOC-1-011 (locked 2026-09-24 05:02 IST, BEFORE any embeddings, retrieval scoring, or outcomes; only data-availability scouting has occurred)
GATES.md as written specified "UniProtKB/Swiss-Prot REVIEWED Cas9/Cas12a/Cas13a, capped at 150/family". Live UniProt counts show this is infeasible: reviewed gene-name queries return Cas9=14, Cas12a/cpf1=5, Cas13a=6; full-KB gene-name queries return Cas12a/cpf1=32, Cas13a=19. Cas12/13 are rare systems with scarce UniProtKB annotation. The following definitions replace the corresponding pool definitions in GATES.md. ALL thresholds, methods, baselines, frozen-validation criteria, and the failure tree are UNCHANGED.

- Family membership via protein_name query: Cas9 (1,768 entries), Cas12a (27), Cas13a (44).
- Seeds (anchors): Cas9 n=150, Cas12a n=12, Cas13a n=20, sampled with seeded RNG (seed 42) from the full family lists.
- Dev held-out positives (disjoint from seeds): Cas9 n=200, Cas12a n=15, Cas13a n=24.
- Dev decoys: 1,500 reviewed E. coli K-12 (4,508 available) + B. subtilis 168 (4,190) entries excluding CRISPR, seeded sample; plus 300 hard decoys from 7,150 reviewed non-CRISPR restriction-endonuclease / DNA- or RNA-polymerase entries. Unchanged in spirit.
- Frozen positives: free-text (cas9 OR cas12 OR cas13) with date_created >= 2022-01-01 (35,332 hits), filtered to protein name containing Cas9/Cas12/Cas13 and length 400-2000 aa; seeded sample n=300.
- Frozen decoys: reviewed bacterial (taxonomy_id:2) entries created >= 2022-01-01 NOT CRISPR (2,135 available), seeded sample n=300.
- Consequence: per-family dev AUROC for Cas12a/Cas13a rests on small held-out n (15/24); pooled dev AUROC and frozen AUROC remain primary for G1/G2 as locked. CIs reported.
