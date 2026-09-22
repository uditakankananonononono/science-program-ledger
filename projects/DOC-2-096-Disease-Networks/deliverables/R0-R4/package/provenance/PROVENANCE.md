# Provenance - DOC-2-096 R0-R4 negative-evidence arc package

Scientific source: https://github.com/uditakankananonononono/science-program at commit `9b59730945b74a7059cf09ac5ae2aa5b2be634d4`, tree `projects/DOC-2-096-Disease-Networks`. The five frozen round trees arrived in that repository as extracted seal directories named `<round-tar-name>-<tar-hash-prefix>` (commit `b5e31ebb02ecbe762b05b9c31ae3fcb6495f62e3`); the original tar bytes are not stored in the repository, so this package preserves the extracted trees byte-for-byte and records the seal directory names.

The complete project tree (`PROJECT_SUMMARY.md` plus all five round trees) was copied byte-for-byte into `frozen/`. `SOURCE_HASH_MAP.tsv` is the independent one-to-one comparison: 87 copied items, 87 MATCH, 0 mismatches. Per-round maps `SOURCE_HASH_MAP_R0.tsv` through `SOURCE_HASH_MAP_R4.tsv` split the same comparison by round. No scientific code was run. Packaging added only synthesis, deterministic views of frozen CSVs, a read-only curator-queue exporter, tests, and custody records.

Locked-protocol SHA-256 sidecars were re-verified against the packaged bytes: all seven locked files (R0 protocol.md + protocol.json, R1 protocol.md + protocol.json, R2/R3/R4 protocol.md) match, and the R1 crosswalk lock `2d068fee2bf4f56233e1c3bc18389dc42a4ea4bc75aac3cabab90ded02c2a3ab` matches `data/processed/condition_crosswalk.csv`.

Protocol lock timestamps (IST, 2026-09-21, before each round's outcomes): R0 22:22, R1 22:32, R2 22:39, R3 22:44, R4 22:51.

Figure sources:
- `figures/r0_source_instability.png` is the frozen R0 figure reused byte-identically; its sidecar records the frozen figure's own SHA-256.
- `figures/r2_locked_transport.png` reads only R2 `results/locked_temporal_metrics.csv`.
- `figures/r4_competing_risk_enrichment.png` reads only R4 `results/competing_risk_metrics.csv` (test-split rows only, as stored).

Each new PNG embeds the source SHA-256 in its metadata and footer and has a `.SOURCE.sha256` sidecar. Figures present stored values only and add no analysis.
