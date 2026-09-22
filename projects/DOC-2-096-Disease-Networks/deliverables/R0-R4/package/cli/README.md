# Read-only curator-queue exporter

`curator_queue_export.py` (Python standard library only) exposes the frozen
DOC-2-096 R0-R4 outputs to a human curator. It selects frozen rows by explicit
round/status fields and exports them in stable sorted order. Every exported row
carries the source round, the frozen claim status, the source artifact path,
the source artifact SHA-256, and the original row identifier.

It does not score, rank, infer, merge evidence across rounds, or change labels.
It has no threshold, model, network, or file-write path.

Commands:
- `verify` - bidirectional package-manifest check, frozen row counts, frozen
  status-label custody, and figure source-hash sidecars.
- `rounds` - the five rounds with their frozen claim-status labels.
- `tables` - exportable frozen tables with per-file SHA-256.
- `summary` - frozen per-round gate/summary JSONs under their status labels.
- `round-summary R0|R1|R2|R3|R4` - one frozen summary artifact, verbatim.
- `export --round RX --table NAME [--format tsv|json]` or
  `export --status "EXACT FROZEN STATUS" --table NAME` - stable sorted rows.

Exported values are the stored strings from the frozen CSVs, unchanged.
Queue interpretation boundary: these are database-activity review queues.
They are never disease severity, patient risk, or variant pathogenicity.
