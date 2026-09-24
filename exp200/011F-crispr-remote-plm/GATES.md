# DOC-1-011F: PLM Discovery in the Remote-Homology Regime — GATES (locked 2026-09-24 12:55 IST, before any scoring)

Follow-up to DOC-1-011 (boundary: ESM-2 8M retrieval loses to MMseqs2 on alignable Cas
families - PLM information real but redundant where sequence similarity exists). 011F tests
011's own nominated complement hypothesis: PLM discovery value specifically in the
remote-homology regime. Parent-approved sketch 12:54:54 ("lock G0-G3 numerically
pre-scoring... If G0 halts, report rather than re-scope"). All thresholds numeric below.

## Data (all live-verified 2026-09-24 12:54)
- SEEDS: 011's exact seed pools (exp200/011-crispr-plm-discovery/data/: Cas9 n=150,
  Cas12a n=12, Cas13a n=20; same UniProtKB accessions, reused unchanged).
- REMOTE POSITIVES (dev): UniProtKB protein_name:Cas12f1 (1,824 live count; type V-F,
  TnpB-derived, ~400-500aa) - random sample n=300 (rng seed 7) + all protein_name:Cas12b
  (n=12) + all protein_name:Cas12k (n=25).
- DECOYS (dev): 011's decoy queries (bacterial E. coli/B. subtilis reviewed non-CRISPR +
  hard nuclease/polymerase), LENGTH-MATCHED to the remote-positive length distribution:
  each decoy's length must fall within the [p5, p95] range of the remote-positive lengths;
  n=1,500 bacterial + n=300 hard, sampled (rng seed 7) from length-eligible pools.
- FROZEN: protein_name:Cas12f1 date_created >= 2023-01-01 (717 live count) random sample
  n=300 (rng seed 7) + all post-2023 Cas12k (n=20); fresh length-matched bacterial decoys
  date_created >= 2023-01-01, n=300 (011's date_created frozen protocol).
- Any accession failing retrieval/embedding is dropped and counted in REPORT before verdicts.

## Locked mechanics
- EMBEDDINGS: 011's exact pipeline (code/embed.py, ESM-2 t6_8M_UR50D, mean-pool, 512aa cap,
  budget-capped resumable batches).
- MMseqs2 BASELINE: 011's exact baseline (sensitive mode -s 7.5); score of a query = best
  alignment bitscore against the seed database; AUROC vs decoys.
- PLM SCORE: 011's exact scorer (max cosine similarity to any seed embedding).
- AUROC computed once per locked gate; no re-scoring with alternative parameters.

## Gates
- G0 (premise audit, pre-modeling, halt-no-patch per parent 12:54:54): MMseqs2 retrieval
  AUROC of dev remote positives vs dev decoys must be < 0.70 (sequence signal verifiably
  weak). Identity distributions disclosed. If AUROC >= 0.70 -> the regime has sequence
  signal; HALT, report to parent, no re-scope.
- G1 (dev): PLM retrieval AUROC >= 0.80 AND >= MMseqs2 AUROC + 0.20 on the identical pool.
  Both clauses required.
- G2 (frozen): single-pass PLM AUROC >= 0.75 AND dev->frozen drop <= 0.10 (011's G2 form).
- G3 (mechanism, documented): per-family nearest-centroid assignment rates in embedding
  space (011's G3 statistic); Cas12f cluster separation vs decoys reported against 011's
  PCA picture; literature: Makarova 2020 classification, Pausch 2020, Altae-Tran 2021.
- G4: crispr_finder.py remote-mode CLI + REPORT.md + one prospective nomination.
- Failure tree: G0 halt -> report to parent (no re-scope). G1 fail -> the 011 boundary
  generalizes: PLM adds no retrieval value even without sequence signal at 8M scale;
  document + parent adjudicates. G2 fail -> dev-only effect, boundary documented.
