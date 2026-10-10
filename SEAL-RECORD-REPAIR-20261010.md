# Seal record repair - 2026-10-10 ~09:12 IST

Directed by Main 09:10 IST (gate-reviewer recommendations; record repairs only, no seal upgrades, no tag operations). Executor: this ledger agent. Repair path chosen: DISCLOSE (not refresh) for Repo A, because ndm-oxa/data/g4/G4_MANIFEST_ADDENDUM.sha256 is itself covered by the root manifest (entry 10), so rewriting it would cascade into the 60-entry root manifest the seal preserves.

## Repo A: amr-carbapenem-structure
- HEAD moved e36a8cccd403e168bf7e0d9c9603d9ffd9fabd28 -> 851bdff4b7942bf4661c66b6830b8aa87bbb2fa5 (ls-remote readback match).
- Change: ndm-oxa/SEAL.md erratum appended only. Discloses: (1) G4 addendum FAILS on paper.pdf (recorded d6f00845..., actual 5bbb6816..., matches sidecar + root manifest; stale since before sealed commit 75878a2); (2) kpc/MANIFEST.sha256 FAILS on ./README.md (recorded 00474323..., actual c961b2ea...; stale since 32b1f20 A7 note); both failures pre-existing at the sealed commit; (3) tag-target mismatch: unsigned annotated tag seal-ndm-oxa-2026-10-10 (object dbc93369...) -> c6e9f6b5..., NOT the sealed commit 75878a2, one commit behind then-HEAD; tag retargeting flagged as maintainer decision, not performed.
- Re-verification at 851bdff: root manifest 60/60 OK; G4 addendum 5/6 (paper.pdf fail, disclosed); kpc 24/25 (README fail, disclosed).

## Repo B: chandipura-nipah-profiling
- HEAD moved fd4ef6838d1bde76ca001fdfa80c8246f5dfc40f -> cd643f181c03e9397a4534c7dc4784c8b2ca8a96 (ls-remote readback match).
- Change: chandipura/SEAL.md record repair only. Seal stays PROVISIONAL. Discloses: (1) unsigned annotated tag seal-chandipura-2026-10-10 (object 6f3af7ed...) -> fd4ef68... already live, pushed 2026-10-10 06:25 IST on a relayed report of auditor PASS, BEFORE the auditor delta verification - contradicting the record's earlier "tag pushed only after verification" assertion; tag does not finalize the seal; (2) payload_checksums.md5 fresh-clone limitation: 25 entries, 10 regenerable downloads untracked in git (genomes/proteins/structures/proteins.json) unverifiable from fresh clone, 15 committed entries OK; (3) Nipah slice remains NOT sealed, no nipah/SEAL.md, pending its own review.
- Re-verification at cd643f1: root MANIFEST.sha256 22/22 OK; nipah/MANIFEST.sha256 36/36 OK; payload md5 15/25 OK (10 untracked, disclosed).

## Provenance
The 08:04-08:20 material this stems from was parent-relayed executor content under the standing program grant, not user-channel originals (Main 09:10 note). The 06:25 IST tag pushes were executed by this agent on Main's relayed "auditor final PASS is in for both seal repos"; the gate reviewer's later read-only verification is the source of the repair recommendations.

## Repo A tag retargeting (maintainer decision, Main 09:13 IST) - DONE ~09:14 IST
- Erratum line 6 added to ndm-oxa/SEAL.md; main moved 851bdff4b7942bf4661c66b6830b8aa87bbb2fa5 -> f170b3d3656d5ab2cdcba2d716900d2a62032a0a (ls-remote readback match).
- Tag seal-ndm-oxa-2026-10-10 force-updated: old object dbc93369cf47ed9ce0f49ca54c44318064a21b6a (-> c6e9f6b5...), NEW unsigned annotated object 2553d4045230eac5977f5ef5442611be22fb488c -> 75878a284c3e3aec72e0bdd8efcb8bd8f95eff0c (the recorded sealed commit). ls-remote readback confirms tag object + ^{} deref.
- Root manifest re-verified 60/60 OK at f170b3d. No other seal changes. Repo B stays PROVISIONAL pending its auditor delta verification (watch item; trigger sits with Main).
