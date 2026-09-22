# Closeout ledger

- Scope: packaging-only synthesis of the frozen DOC-2-096 R0-R4 disease-network arc (one coherent negative-evidence synthesis; each round's status preserved separately).
- Science changes: none. No recomputation, re-ranking, threshold change, new cross-round statistic, post hoc combined score, or replacement artifact.
- Conclusion preserved per round: R0 locked-gate success with bounded claim; R1 clean temporal-identifiability stop; R2 locked-gate failure; R3 locked ranking gate failure; R4 predictive triage closed with descriptive topology retained.
- Tool: read-only curator-queue exporter over existing frozen outputs. It selects by explicit round/status fields and exports stable sorted rows carrying source round, frozen claim status, source artifact SHA-256, and original identifier. It does not score, rank, infer, merge evidence across rounds, or change labels.
- New figures: deterministic renderings of two frozen CSVs with source-hash sidecars; R0 figure reused byte-identically. No new analysis.
- Large raw ClinVar downloads: external references only, with frozen SHA-256 values and URLs retained.
- Custody: package manifest + complete source-hash map (87/87 MATCH) + per-round maps + outer archive hash + clean restore.
- Preflight of the four DOC-2-033 custody defects: source map nonempty and complete (PASS); clean-restore evidence inside the archive and standalone beside it (PASS); every renderer/script required for restore transferred (`figures/render_figures.py`, exporter, tests) (PASS); internal and outer custody metadata regenerated from final bytes and in agreement (PASS).
- Release state: prepared for independent audit. No repository push or Drive upload performed.
