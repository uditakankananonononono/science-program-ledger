# DOC-2-096 R0-R4 submission package

Packaging-only backfill of the frozen disease-networks-from-negative-evidence arc: R0 bounded descriptive topology, R1 temporal-identifiability stop, R2 archived temporal validation, R3 ranking-only triage, R4 competing-risk-set redesign.

**Conclusion:** Predictive triage is closed. The graduated contribution is descriptive: bounded benign/conflict evidence rewires disease-network topology (R0), and simple evidence-burden rankings transport for database-activity queues (R4) without added model value. No calibrated predictor, no clinical-risk, pathogenicity, or disease-severity claim is made.

Contents:
- `paper/` - submission-ready A4 PDF and LaTeX source (Times, blue-border house style)
- `frozen/` - complete project tree (summary plus all five round trees), unchanged
- `figures/` - byte-identical R0 figure plus two deterministic views of frozen CSVs, with source-hash sidecars and renderer
- `cli/` - read-only curator-queue exporter
- `tests/` - golden, determinism, scope, and custody tests
- `provenance/` - source chain, environment, external/missing registry, complete source-hash map and per-round maps
- `closeout/` - clean-restore evidence and closeout ledger
- `MANIFEST.sha256` and `PACKAGE_MANIFEST.json` - package custody

Restore and verify:
```
tar xzf DOC-2-096-R0-R4-package.tar.gz
cd DOC-2-096-R0-R4-package
sha256sum -c MANIFEST.sha256
python3 cli/curator_queue_export.py verify
python3 tests/run_tests.py
```

Large raw ClinVar downloads remain external references with frozen SHA-256 values and URLs. No repository push or Drive upload was performed.
