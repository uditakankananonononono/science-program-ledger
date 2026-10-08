# U1 executable freeze

Preregeaeffad published before implementation. No selected source image/label content
retrieved or scored yet. Three literal-only tests cover single/multiple/empty labels,
nonfinite/class/size/corner errors,bounded stream/declared-length refusal,image decode
and dimension refusal. No author module/YAML execution. Exact YAML route:dataset.yaml
for cube,cylinder,flagella,helical,rollingcube,sheetrobot,sphere3; sphere1/sample.yaml.
YAML nc parsed only if literal integer; names/path text retained for manual review,
unknowns stay unresolved. Exact pair case/path/stem,not directory-list position.

Pinned raw.githubusercontent.com HTTP individual path retrieval,no redirects,no
compressed transport; timeout20seconds per operation,40second elapsed per stream;
no retries/replacement records. Stops at caps without reading an excess-byte sentinel;
if byte cap reached without content-length/EOF proof,unsupported record. Source cap
64MiB,58files,2MiB image/64KiB label/128KiB metadata. No git show/blob hydration.
Metadata path-only tree is frozen/copied,hash checked; no whole-tree blob size walk.

Decoded limits:PNG/JPEG single frame,<=4096each dimension,<=2.4million pixels;
Pillow decompression guard enabled. One source image at a time,maximum working image
pixel buffers96MiB (RGBA decode+RGB copy+resized originals/eight640x400panels+
1280x800canvas well below this under limits). No batch original-image decode.
64MiB transport cap refers to received source bytes,not decoded memory. Environment
pins Python/Pillow; manifest retains code/environment/selection/output hashes plus
source raw SHA/bytes/paths/URLs. Sampled missing/unsupported records never replaced.

Reviewer prior exposure:cube/test/Cube2-000008.png+YOLO label already viewed during
admission. Deterministic selection remains fixed,NOT blind/unseen or held-out. All
24checks and up to8fixed overlays descriptive. Empty labels explicit 'empty',multirow
all rows retained; invalid rows recorded,not repaired/dropped. Invalid boxes not drawn
as valid boxes; overlay invalid count visible,full raw issues retained. No class rename.
Whole-tree path inventory and sampled content duplicates/adjacency distinct; prefixes
not established videos,three-way split not paper80/20. Tracking alignment NOT admitted.
Publisher GPL claims evidence with limits,not legal clearance;commercial note retained.

Run after review/publication: `python3 check.py results` from this directory. New output
directory only; partial retrieval records retained explicitly,not mistaken for complete
source slice. Actual overlays inspected before results report. No imaging admission
reopens rejected wall/rheology/dynamics calibration or establishes a new algorithm.

Review HOLD fixes before any source retrieval: derived normalized/pixel arithmetic
finiteness checked,overflow retains null corners+explicit issue,invalid UTF8 label
keeps unavailable panel rather than dereferencing absent annotation,declared body
length checked at EOF. New fixtures include all three plus end-to-end24mocked pairs/
overlays for UTF8 failure and finite overflow. No source measurements executed.
