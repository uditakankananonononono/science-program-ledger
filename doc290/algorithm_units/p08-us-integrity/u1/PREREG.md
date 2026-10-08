# U1 measured ultrasound detection annotation-integrity admission/prereg

One surface: USMicroMagSet normalized YOLO detection annotations. Not dynamics,
wall/rheology calibration,tracking evaluation,detector comparison or invention.
Source https://github.com/Kivo0/UsMicroMagSet at exact commit
1a0364c7509468dde0df86b4a82a8d8546b45818. Official DataPort source:
https://ieee-dataport.org/documents/usmicromagset (29.96GB full archive,not retrieved).
This pinned GitHub tree is a distinct bounded route,NOT demonstrated DataPort-identical
or the full40k corpus. Publisher claims GPLv3 dataset and invites commercial-license
contact: retain LICENSE/README and note,no permissive relicensing,contact,payment.

## Frozen selection and retrieval bounds

Tree inventory via metadata-only no-checkout partial clone and git ls-tree,not image
checkout/author code execution.83,867 paths recovered; initial HTTP tree query failed
and clone timed out but retained readable tree. No image diagnostic executed.
selection.json locks24robot/split cells: robots explicitly cube,cylinder,flagella,
helical,rollingcube,sheetrobot,sphere1,sphere3; splits test,train,val. In each cell
lexicographically FIRST image path at exact <robot>/images/<split>/ with PNG/JPG/JPEG
extension; no quality/outcome choice. Empty cells retained,not replaced. Pair exact
<robot>/labels/<split>/<same case-sensitive stem>.txt,NOT positional directory order.
Lock source-prefix/frame tokens from stem where parseable,otherwise record unresolved.
These tokens are observed IDs,NOT verified independent video sequence IDs.

At most24images+24labels,8dataset/sample YAMLs,README.md and LICENSE=58source files.
Hard per-image2MiB,per-label64KiB,metadata128KiB,total64MiB before committing bytes;
stream downloads with byte counter and stop on overrun,no fallback bigger fetch.
Retrieve individually from pinned source by path (git blob at pinned tree or bounded
HTTP source route),never whole-tree checkout/LFS pull/full archive. Retain originals,
path/blob/hash/byte count/decoded dimensions,source commit and normalized IDs. Git/LFS
pointer or unsupported format yields unavailable/unsupported record,not assumed image.
No paid/login action needed for this GitHub route. Retrieval error/oversize retained,
no replacement sample. Local metadata clone9.4MiB already present,not corpus data.

## Measurement contract after prereg review/publication

Whole-tree PATH inventory only: counts by robot/split/type,exact path-stem missing
counterparts and repeated stems across splits. No whole-tree pixel/hash conclusions.
Sampled content checks only: selected image decodes; label row count,exact5fields
per row,class integer/nonnegative,finite xc,yc,w,h,positive w/h,computed normalized
corners inside[0,1] and decoded-frame coordinates. Report every row/invalidity,never
repair/drop/clip boxes or silently relabel classes. Unknown class mapping remains gap;
check YAML class counts/names only statically,author-local paths and cube2/Cube
inconsistency retained. Use per-robot dataset.yaml if present,else sample.yaml,first
exact path rule; no YAML/module execution.

Distinct counts: duplicate filename/stem,sampled exact image-content SHA256 collisions,
and numerical frame adjacency within observed source prefix. No duplicates is NOT
video-level independence; source-prefix to original-video map may be unresolved.
GitHub three-way directory split not paper80/20 split,do not claim agreement/leakage-
free evaluation. No inference of temporal rate/dropout or physical scale from frames.

Fixed overlays chosen BEFORE diagnostics: selected test image for EACH robot cell,
including invalid/missing annotations shown as such. At most8panels,grouped4per
figure. Original dimensions retained,decoded labels with computed corners,IDs visible.
Actual pixels inspected; no outcome-picked frame/box adjustment. Images retained
unchanged. Report counts as sampled checks versus whole-tree inventory explicitly.
Literal label/box fixtures precede sampled content checks. Environment/code/protocol/
selection/input/output hashes retained. Any post-freeze rule change disclosed/refrozen.

Tracking groundtruth comma-delimited schema is SEPARATE and NOT admitted here.
No tracking image/row alignment assumption,even if robot names look similar. A later
tracking question would require its own alignment/units/frame admission.

Endpoint: usable bounded annotation slice,metadata/rights/access gap,or invalid
annotations all acceptable. Observation evidence only; no learned model or scientific
P08 physical gate closed. No algorithmic improvement/novelty claim.
