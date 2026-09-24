# 011F GATES ADDENDUM B — scorer + seed-DB sourcing (locked 2026-09-24 12:59 IST, before any scoring)

Mechanics corrections only; all thresholds unchanged.
1. PLM SCORE: GATES.md wrote "max cosine similarity to any seed embedding". 011's exact
   executed scorer (code/crispr_finder.py) is max cosine similarity to the three committed
   seed-family CENTROIDS (results/centroids.json: Cas9/Cas12a/Cas13a). 011F uses 011's exact
   committed centroid scorer and the committed centroids, with embeddings from 011's exact
   embed.py pipeline (ESM-2 t6_8M, mean-pool, 512aa cap).
2. MMseqs2 seed DB: 011's seed sequences were not committed as a fasta; the 182 seed
   accessions (data/pool_ids.json: seed_cas9 150, seed_cas12a 12, seed_cas13a 20) are
   re-fetched from UniProtKB by accession (immutable sequences = identical pool).
