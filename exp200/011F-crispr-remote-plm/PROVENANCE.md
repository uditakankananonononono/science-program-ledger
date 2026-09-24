# PROVENANCE — 011F
- All sequences: UniProtKB REST API (rest.uniprot.org/uniprotkb), live queries 2026-09-24
  12:55-12:58 IST. Query strings + counts: results/pull_meta.json, results/pool_meta.json.
- Seeds/decoys inheritance: exp200/011-crispr-plm-discovery/data/ (pool_ids.json seed
  accessions re-fetched by accession; dev_decoys/hard_decoys fastas length-filtered).
- Centroids: exp200/011-crispr-plm-discovery/results/centroids.json (011's committed).
- Baseline: MMseqs2 release 16-747c6 static AVX2 build, sensitive mode -s 7.5 (011's exact).
- Model: ESM-2 t6_8M_UR50D via fair-esm, mean-pooled layer 6, 512aa cap (011's exact).
