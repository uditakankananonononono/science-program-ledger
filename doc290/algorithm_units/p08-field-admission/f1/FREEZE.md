# F1 Gitblob format/provenance freeze

Prereg83d5103 published;selected data/notebook blob contents NOT fetched/peeked.
Additional pinned-tree API metadata fetched,not source content:new exact-tree
snapshot confirms commit/tree correspondence,retained and hash-bound. Original
selection/snapshots unchanged. All62identity checks before text/source analysis.
API envelope strict JSON/base64 parsing is needed for identity,NOT text analysis.
Envelopes separately retained;raw decoded originals retained only after identity.
No LFS dereference,pickle deserialization,code/notebook import/execution/training.

Reviewer conditions verbatim:
- Strict JSON: reject duplicate keys/nonstandard constants and bool-as-int identity fields; validate base64 syntax explicitly, normalizing only its declared line-wrapping, with decoded caps before analysis.
- Match every selected object to the pinned complete tree path/type/size/SHA1 and validate commit/tree binding - NOT current main.
- Exercise failure at all 62 positions plus notebook malformed-source/pointer boundary cases without executing anything.
- Retain API envelopes separately; distinguish envelope parsing needed for identity from post-all-62 text/source analysis.

Eight literal groups include all62missing-identity-position zero-analysis calls,
strictJSON/bool/canonicalbase64/decodedcap/binding,notebook malformed source/outputs
not used,pointer malformed/huge declared size not dereferenced,UTF8/Unicode separators.
131-byte metadata size is not a format classification. Pointer syntax yields only
literal declared SHA256/size,NOT payload rights/availability/calibration records.
Notebook raw source retains any stored output as original bytes but outputs are NOT
measurement/trial evidence. README claims remain assertions,not measurement replay.

20s socket/40s between-read checks,not hardwall.128KiBper envelope/decodedfile,
8MiBenvelope/512KiBdecoded combined,not peak-memory/output caps or enforced quotas.
No measured peak,stated2cores/2GB only. Mandatory manual ledger before classification:
device/gradient/slew/thermal/mobility limits remain explicit,no Tesla inheritance,
physiology or invention credit. OctoMag/LFS payloads excluded,not unavailable everywhere.
Chronology document-reported;replay reproducibility not historical ordering.

Run after review/publication: python3 admit.py NEW_OUTPUT_DIRECTORY
Replay: python3 admit.py NEW_DIRECTORY RETAINED_OUTPUT_DIRECTORY

Reviewer-requested classifier correction before source run: pointer recognition now
uses explicit ASCII byte LF-only grammar. CRLF is deliberately noncanonical/unresolved,
as are VT/FF/U+2028/NEL separators. Raw Unicode splitlines inventory unchanged and
separate from pointer syntax. Declared fields emitted only for exact LF grammar.
