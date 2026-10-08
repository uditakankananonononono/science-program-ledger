# T3 literal XML admission freeze

Prereg c5b24f2 published/readback before build. Commit fe7eb12c, tree dbd8f7c6;
source XML bodies not fetched/read/parsed before this freeze. Previous exposure
in PREREG, not blind validation. Two exact original identities gate ALL parsing.

Strict original UTF8 decoding, optional BOM accepted; only UTF8/utf-8 declaration
allowed. Explicit forbid_dtd=True (including entity-free DTD), forbid_entities=True,
forbid_external=True. No XInclude/schema/stylesheet/network processing. Actual Python
executable and defusedxml/__init__/ElementTree/common plus stdlib ET bytes pinned.
Built-in parser engine has no separate module file; Python executable pin includes
built-in engine, not proof against all transitive environment changes.

Paths are JSON arrays of expanded {URI}local names, same-expanded-name sibling
ordinal and all-element-child ordinal (both 1based); preorder document element
ordinal 1based. Root ordinals 1. Text AND tails and attributes kept as literal
strings, never numbers. Namespace prefix spelling/comments/processing instructions
not in element inventory; original bytes retain them. No complete XML token claim.

Declared caps: depth128, nodes200000, text+tail8388608 Unicode characters,
attributes2097152 Unicode characters. Caps checked AFTER parser allocations; not
peak-memory quotas. Records in memory before return; failed syntax/unsafe/cap or
encoding yields no partial inventory. One file failure does not convert other
file syntax to endpoint proof; original bytes and SHA256 retained.

Transport no redirects, exact URLs, identity encoding; 5MiB/file, 8MiB combined,
20s socket/40s between-read deadline checks, not hard wall quota. JSON/path expansion
not measured peak/output cap. No 2core/2GB empirical claim. Static paths only, no
pixels/bbox correctness/tracker/physics/dropout/rights/invention credit.

Tests: literal Unicode namespace repeated-sibling paths, tails/nonfinite-as-strings;
entity-free DTD/entity/external/malformed/nonUTF8 declaration+bytes rejection;
each cap no partial output; PI/XInclude inert; each identity-position parse trap;
transport exact-route/redirect rejection. Traps don't authenticate all environment
behavior. Run AFTER review+publication: python3 admit.py NEW_OUTPUT_DIRECTORY
Replay: python3 admit.py NEW_DIRECTORY RETAINED_SOURCES_DIRECTORY
Manual source-field annotation/provenance ledger required before classification.
