# Deploy Keys

Write deploy keys for science-program builders, maintained by the orchestrator. Keys are identified by fingerprint, not title. Revoke only on respawn instructions from the orchestrator.

Note: GitHub allows a given deploy key on only one repository, so a builder that pushes to both a slice repo and this ledger needs a separate key per repo.

| Added (UTC) | Title | Fingerprint (SHA256) | Lane / agent | Deployed on | Notes |
|---|---|---|---|---|---|
| 2026-09-24 | B01 v3 PB2 builder | r6of2QA9CbmipjNWsmV2uaSBk2+JWc6ZKl5xchyAKS0 | B01 v3 (H5N1 PB2), agent-01M38M9CPHDBHJ2QDXA97XMP8K | h5n1-mammal-jump (write) | Key self-labeled "b14-builder-v4" and quoted the B14 v4 agent id while reporting from the B01 v3 envelope; identity tracked by fingerprint per orchestrator. Ledger add failed (GitHub: key already in use on h5n1-mammal-jump); needs a separate keypair for ledger write access. The actual B14 v4 (dengue) key will be added separately when it reports. |
