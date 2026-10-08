# U2 manual source evidence ledger

Source pin: Kivo0/UsMicroMagSet 1a0364c7509468dde0df86b4a82a8d8546b45818.
All 23 original pinned Git blob OIDs and sizes verified before diagnostics.
This ledger inspects the fixed seven static files, not extra source content. Exact
numbered text is retained in results/static_provenance.json and original bytes in
results/sources. Citations below use Python str.splitlines(), 1-based, INCLUDING
blank lines; VT/FF would create boundaries. The retrieved static files have no VT
or FF, so these particular citations have no VT/FF numbering divergence. Never
substitute UNIX line numbers without checking the exact bytes.

## Source-by-source inspection

README.md (213 splitlines rows): L19-21 describes probe, ten-minute videos and
40K extracted images in aggregate. This does not identify cube-1's original video,
extraction rule, skipped frames or FPS. L23-25 is a commented description of tracking
format 2 in USMicroMagSet_For_tracking, with no row/frame/coordinate definition.
L38-213 examples use detection readrobot/plotimage_withbbox, not a cube-1 parser.
L29-34 is publisher GPL assertion, commercial note and attribution, not clearance.

LICENSE (674 splitlines rows): GPLv3 title/version L1-2, general legal terms and
application boilerplate through L674. No dataset-specific row/frame/coordinate
schema, original-video mapping or origin convention found. This legal text cannot
supply a scientific binding or establish rights clearance.

USMMgSt.py (348 splitlines rows): all function definitions inspected statically,
not executed. L10-26 plotimage_withbbox explicitly describes normalized YOLO and
converts center to corners; L30-50 readrobot selects detection images/labels folders.
Neither binds tracking cube-1 text. L94-140 draw_bounding_box consumes gt[0:4] as
integer x,y,w,h with top-left rectangle endpoints, but has no cube-1 text loader
or evidence that those values come from the frozen groundtruth file. L159-179
plot_gridwithboundingbox extracts filename digits (L173) and indexes
annotations[number+i] (L176); index/start/ordering semantics are ambiguous, not
an authoritative row1->00000001 map. L189-199 distance consumer does not provide
that map either. L294-344 loaders parse space-delimited detection label files and
use directory order; no explicit cube-1 comma-groundtruth binding found. The
module mixes consumers/conventions; none establishes tracking coordinates.

USMicroMagSet_For_tracking/cube/cube-1/groundtruth.txt: 1,744 splitlines rows;
structural inspection of all rows finds four literal integer tokens per row,
no header, explicit image IDs or mapping prose. L1 is 1223,327,334,170;
L8 is 1078,314,359,184; L16 is 728,329,329,168; L1744 is 1284,303,323,212.
Numeric diagnostics remain first16 only. Four numbers and equal row/image counts
cannot determine ordering, origin, units or dropped-row behavior.

full_occlusion.txt: L1 contains 1,744 comma tokens, each literal 0. NOT 1,744
lines; no legend, polarity or frame-order binding. All-zero observed tokens do not
prove no occlusion, and no rows were suppressed under guessed flag semantics.

out_of_view.txt: L1 likewise contains 1,744 comma tokens, each literal 0. No
legend/meaning/polarity/frame-binding evidence; not proof that all frames are visible.

nlp.txt: L1 is exactly "cube swimming in invitro channel". This supplies the
observed source caption only, no numerical schema, frame map, timing or identity.

## Required binding decisions (separate gates)

| Required item | Evidence inspected | Decision |
|---|---|---|
| Row1 -> 00000001.jpg | groundtruth L1; README L23-25; module L159-179 | UNRESOLVED: no explicit binding |
| Order/start index | module L173/L176 ambiguous number+i consumer | UNRESOLVED, no offset repair |
| Dropped/missing/occluded row behavior | groundtruth L1-1744; both flag files L1 | UNRESOLVED: counts and zero tokens not a rule |
| Original-frame provenance | README L19-21 aggregate recording/extraction claim | UNRESOLVED: no cube-1 video map or extraction chain |
| Pixel vs normalized units | module L14-26 normalized detection; L135-140 integer rectangle consumer | UNRESOLVED: no cube-1-specific binding |
| x/y order | module L135-140 consumer | UNRESOLVED for cube-1 |
| Top-left vs center | module L22-26 versus L135-140 consumers | UNRESOLVED for cube-1 |
| Zero/one-based origin | all seven fixed static sources | UNRESOLVED: no definition found |
| Per-image dimensions | verified selected image headers/decodes | OBSERVED 1920x1080 for each16; not coordinate semantics |
| Occlusion/out-of-view polarity and encoding | each flag source L1 | UNRESOLVED: comma structure observed, semantic map absent |

## Classification and exclusions

Manual evidence agrees with the conservative machine rejection, but classification
is based on missing explicit source-specific evidence above, NOT merely the
executable's hardcoded unresolved output. Both gates remain UNRESOLVED; reject
tracking/dynamics use of this candidate slice. No positive-binding change or
refreeze is proposed. All16 candidates pass conditional finite four-number,
positive-width/height and in-frame geometry under HYPOTHETICAL pixel/top-left
row-n/frame-n assumptions. That is not 16 valid tracking annotations, calibration,
identity, timing or performance. Equal 1,744 counts are not an alignment proof.

No extra source fetch rescued this gate, no tracker benchmark or control-feedback
bottleneck inferred, no invention/rights-clearance claim. GitHub route is not proven
DataPort-identical. Resource caps are stated checks, not enforced CPU/RAM quotas or
measured peak memory. 40s transport deadline is checked BETWEEN reads with 20s
socket timeout, not a hard mid-read wall-clock bound. Missing any identity would
have produced early reject+manifest; this run verified all23.
