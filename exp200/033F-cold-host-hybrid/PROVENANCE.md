# 033F PROVENANCE
- All data inherited from DOC-1-033 (see exp200/033-phage-host-gnn/PROVENANCE.md): CHERRY
  benchmark (KennthShang/CHERRY, MIT license) Interactiondata VHM/TEST pairs, allCRISPRs
  spacer DB (1,236,304 spacers), 60,105-prokaryote candidate panel, k=4 kmer profiles.
- CRISPR edges: 033's P1 artifact crispr_edges.npy (14,433 deduped virus->panel-prokaryote
  edges; qualification: length/slen>0.95, pident>95, first hit per virus; BLAST word_size 11
  equivalence verified per 033 Addendum E).
- Cold subset: recomputed from manifest033.json (committed in 033, hash-pinned) — no new
  downloads, no new external data. cold_pairs033.json committed pre-scoring.
