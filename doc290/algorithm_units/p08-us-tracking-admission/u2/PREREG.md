# U2 prereg: cube-1 tracking source admission

One live surface: whether the pinned USMicroMagSet cube/cube-1 tracking source
supports a source-grounded binding between annotation rows, numbered images and
box coordinates. This is admission, not a tracker, benchmark or invention.
Original source: https://github.com/Kivo0/UsMicroMagSet
Exact source commit: 1a0364c7509468dde0df86b4a82a8d8546b45818.
DataPort context: https://ieee-dataport.org/documents/usmicromagset (29.96GB,
login archive, not retrieved). GitHub is NOT proven DataPort-identical. Publisher
GPL assertion and commercial-contact note are source evidence, not clearance or
permissive relicensing. No contact, payment, account change or author code execution.

## Prior exposure and bounded access gate

NOT blind: U1 retained the pinned path inventory and source README/LICENSE.
Before this prereg, developer retrieved and statically inspected USMMgSt.py
(12,650 bytes), cube-1 groundtruth.txt (28,928 bytes; first three rows previewed)
and full_occlusion.txt (3,487 bytes; retrieved but not semantically interpreted).
Reviewer independently statically read those three sources; reviewer reports
full_occlusion as 1,744 comma tokens, NOT 1,744 lines. This is prior exposure, not a
new frozen result. Tree metadata lists 1,744 cube-1 image paths with endpoints
00000001.jpg and 00001744.jpg; first-image blob size 82,519 bytes. No U2 source
image was retrieved/decoded, no diagnostic or tracker was built/run. Equal path
counts or filename endpoints are NOT demonstrated alignment or temporal provenance.
Access is unauthenticated pinned individual GitHub blobs, not full-corpus checkout.
If any required source lacks bounded access, record unavailable and reject the
binding; do not enlarge caps, replace a file or fetch the DataPort archive.

## Exact frozen files and resource bounds

selection.json freezes all exact paths, original pinned Git blob OIDs and known
blob sizes. Exactly 23 original files maximum: 16 images and 7 static sources.
Static sources: README.md, LICENSE, USMMgSt.py, and these four cube-1 files:
groundtruth.txt, full_occlusion.txt, out_of_view.txt, nlp.txt, each under
USMicroMagSet_For_tracking/cube/cube-1/. No inferred semantics from names.
Images are exactly img/00000001.jpg through img/00000016.jpg under that same
cube-1 directory, each path enumerated in selection.json. No outcome-picked
replacement. Fixed display IDs are 00000001, 00000008, 00000016, enumerated there.

Per-image cap 2MiB; decoded-image cap 2,400,000 pixels; each metadata file 128KiB;
metadata combined cap 896KiB; total retrieved source bytes cap 40MiB. Stream byte
counter enforces each file and cumulative cap before accepting bytes; Content-Length
is only a hint. Strict UTF-8 for text, decoding errors/truncation/empty/missing files
retained as errors, not coerced or silently repaired. Retain originals, URL, pinned
blob OID, Git blob verification, SHA256, byte count and per-image header/decoded
size. Git/LFS pointers are unsupported, not images. Fetch complete bounded text
files, never a prefix presented as complete. No full-image-tree fetch, model training,
GPU or neural inference. Use <=2 cores/2GB RAM, serial image decode. Metadata-only
existing tree inspection is permitted; no content retrieval outside the exact set.

## Two separate evidence gates, before any tracking use

A. Row/frame binding requires SOURCE-SPECIFIC EXPLICIT evidence for row 1 mapping
to 00000001.jpg, order and start index, whether rows are dropped for missing,
occluded/out-of-view frames, and original-frame provenance. Record exact source
file/line citations or unresolved/conflicting status for each item. Token counts,
contiguous image IDs and visually plausible boxes are necessary controls at most,
not an authoritative frame map. No index-offset repair by visual fit.

B. Coordinate binding separately requires source-specific evidence for pixel versus
normalized units, x/y order, top-left versus center, zero/one-based origin and the
actual per-image dimensions. USMMgSt.py draw_bounding_box treats gt as top-left
x,y,w,h, but no binding to the cube-1 parser has been demonstrated. Its
plot_gridwithboundingbox extracts filename digits then indexes annotations[number+i];
this ambiguous consumer is NOT an authoritative map. A generic tracking-standard
four-field convention does not establish cube-1 semantics. Cite exact evidence or
retain each coordinate item unresolved/conflicting. No retuning conventions to fit.

Static provenance audit includes all four text sources: groundtruth, full_occlusion,
out_of_view and nlp. Determine observed delimiter/token/line structure, but do NOT
assume flag polarity, line-per-frame encoding, out-of-view meaning or nlp schema.
Raw values and missing/invalid/occluded rows remain visible; no suppression based on
unproven semantics. No access to more source content to rescue a failing gate without
separate reviewed amendment/refreeze. A missing explicit binding is a valid endpoint.

## Frozen diagnostic contract, only after review/publication

First literal fixtures test strict UTF-8, empty/truncated/oversize files, malformed
field/token counts, nonfinite/overflow arithmetic, missing rows, and exact frame IDs.
Use exact decimal/Fraction arithmetic for derived box corners when finite; reject
nonfinite arithmetic, do not clip/round/repair labels. Count blank lines separately;
never drop them before assigning raw row ordinals. Report observed schema, metadata
counts and image-ID inventory as separate controls, not provenance proof.

For all 16 selected images retain dimensions and access/decode status. For the first
16 raw groundtruth row ordinals retain original text, parse status, field count and
finite-number status without presuming the row/image binding. Under a clearly labeled
candidate pixel/top-left x,y,w,h convention only, report positive width/height and
in-frame corner checks; those are conditional geometry, NOT annotation validity if
binding remains unresolved. Keep every missing/invalid row and unsupported image.

Fixed figures show IDs 00000001, 00000008 and 00000016. If BOTH gates establish
binding, show source-cited boxes with per-image dimensions. Otherwise show original
image and raw candidate row separately, labeled UNRESOLVED row/frame and/or coordinate
binding. Do not draw an unlabeled apparently authoritative box; any hypothetical
candidate overlay must say HYPOTHETICAL row-n/frame-n alignment AND hypothetical
coordinate convention. Visual plausibility cannot upgrade either gate. Inspect actual
pixels of every finished figure. No selection change after inspection.

Retain code/environment/protocol/selection/input/output hashes and tests. Report
all access errors, invalidities and scope limits. Any post-freeze change is disclosed
and requires review/refreeze before affected diagnostics; no silent offset or policy fix.

## Frozen outcomes and exclusions

Outcome 1: both bindings established with exact source citations for every required
item, yielding only a bounded source-admitted slice. Outcome 2: any item unresolved,
conflicting or unavailable -> reject tracking/dynamics use, preserving raw candidate
rows and source images and naming the missing evidence. Equal counts and plausible
boxes do not establish calibration, track identity, time, frame rate, physical scale,
independent-video validation or original-video provenance. No tracker benchmark,
control-feedback bottleneck, performance/dynamics improvement or invention credit
follows from admission alone. Failure is a valid endpoint. Prereg review and
publication precede implementation and scoring.
