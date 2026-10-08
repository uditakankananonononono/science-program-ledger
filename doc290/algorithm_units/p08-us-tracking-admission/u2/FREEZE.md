# U2 executable freeze

Prereg 2131f5f90c1ea7eb5942fb4ab5c48a1ae0195309 published FF on reviewed
824310ba base. Post-push SSH tip and HTTPS branch page confirm exact 2131f5f;
HTTPS branch raw prereg and selection match byte-for-byte. Immutable raw readback
had transient 404, API was rate-limited; no repush or selection change.

This freeze implements only the published U2 contract. No U2 source diagnostic run,
image fetch or decode; tests use literal/synthetic bytes and fake transport/images.
Prior content exposure is recorded in PREREG.md, including reviewer exposure.

## Added implementation limits, disclosed before source run

Dimension ceiling 4,096 on EACH axis, 2,400,000 pixels, single frame only,
source mode L/RGB/RGBA only. All header/mode/frame checks precede image.load.
Working pixel ceiling 32MiB, conservatively tested as 8 bytes/source pixel plus
four simultaneous 800x620 RGB buffers. Sources decode serially; display code keeps
one original plus small display canvas, no full-resolution atlas. Total process
limit remains 2GB and <=2 cores; these are limits, not a measured memory result.
Only 23 fixed paths; 2MiB/image; 128KiB/static file; 896KiB/static combined;
40MiB total transport. No source-content expansion to rescue missing binding.

Zero redirects: redirect handler refuses; returned URL must equal requested pinned
URL. Identity transport only; declared Content-Length validation, EOF/cap-boundary
proof and truncation checks; per-file/cumulative streaming counters, timeouts.
All 23 pinned Git blob OIDs AND sizes verified BEFORE any source analysis/decode.
Failure of any identity yields reject output without source diagnostic continuation.
All received bounded original bytes, including mismatches, are retained with errors.

Strict UTF-8, blank-row ordinals kept; only first16 raw candidate rows receive
numeric/conditional geometry diagnostics. Whole bounded source text is retained
with numbered lines/token counts for manual provenance review, not automatic map.
Exact Fraction corners converted to rational strings plus finite float previews;
nonfinite/overflow conversion invalidates candidate, JSON allow_nan=False.
No repaired offsets, label clipping, guessed flag meaning, dropped invalid rows,
tracker, neural model or external schema substitution.

Machine evidence gate is intentionally conservative: it does NOT auto-admit either
binding. It reports UNRESOLVED -> reject tracking/dynamics use and shows images and
raw candidate rows separately without boxes. Source-specific explicit evidence,
if discovered in the fixed static files, is to be reported to reviewer with exact
citations before changing that unresolved classification; any code/classification
change needs separate review/refreeze. This restriction avoids turning plausible
geometry/counts into an established mapping. Both prereg endpoints remain possible
through reviewed evidence, not heuristic promotion by the executable.

## Test and output plan

8 fixture test groups pass: pinned blob/size mismatches; zero-redirect handler;
identity/status/URL/Content-Length/truncation/cap-boundary controls; UTF-8/empty,
blank row, malformed field, nonfinite token, huge exponent, derived overflow,
nonpositive width; rational-corner correctness/JSON safety; comma-token versus line
structure; synthetic valid image; pre-load dimension/pixel/frame/mode/memory rejection.
The tests executed no network request or author code. Executable checks its own
freeze-hashes, Python/Pillow environment and selection identity/count before run.

After freeze review/publication only:
python3 check.py NEW_OUTPUT_DIRECTORY
Independent replay without network uses retained exact fixed files:
python3 check.py NEW_OUTPUT_DIRECTORY RETAINED_SOURCES_DIRECTORY

Outputs: all fixed original bytes, inputs.json, static_provenance.json with exact
source lines, admission.json, three fixed image/raw-row figures, manifest.json.
If access identity fails, inputs/admission/manifest only, preserving error endpoint.
Actual pixels of figures must be inspected before result report. Manual evidence
ledger separates row/frame and coordinates, cites every required provenance item,
and preserves missing/conflicting evidence. No mapping/coordinates/tracker/identity/
time/dynamics/bottleneck/invention or rights-clearance claim from this freeze.
