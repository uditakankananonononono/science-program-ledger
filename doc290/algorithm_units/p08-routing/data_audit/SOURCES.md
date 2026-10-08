# Retinal source/access audit, October 8, 2026

HRF official page: https://www5.cs.fau.de/research/data/fundus-images/
The fetched page states CC BY 4.0, 45 images (15 each healthy, diabetic retinopathy,
glaucoma) with vessel labels, and requests citation to Budai et al., Robust Vessel
Segmentation in Fundus Images, International Journal of Biomedical Imaging, 2013.
Only the healthy annotation archive was downloaded here, not all 45 images.
Observed download href resolved to:
https://www5.cs.fau.de/fileadmin/research/datasets/fundus-images/healthy_manualsegm.zip
Archive SHA256/member listing is in hrf_download_manifest.json. All 15 TIFFs were
decoded using Pillow 12.3.0, with dimensions/modes/pixel-value inventories recorded
in hrf_image_inventory.json. No image data is redistributed in this code overlay.
A resized preview of 01_h was visually inspected: vessel foreground on black
background, not a skeleton or a flow graph. No graph extraction/routing on these
annotations has occurred, no independent validation or physiological claim.

DRIVE: https://drive.grand-challenge.org/DRIVE/
Fetched current official page describes 40 images, 20/20 train/test, available
training segmentations but no test annotations on its current challenge route.
Download page https://drive.grand-challenge.org/Download/ failed web fetch.
This is an access-attempt gap, not proof data is unavailable.

STARE: https://cecas.clemson.edu/~ahoover/stare/probing/index.html
Fetched page describes 20-image archives and hand labelings, citing Hoover et al.,
IEEE Transactions on Medical Imaging 19(3), 203-210, March 2000. Direct Python HTTPS
access failed certificate verification. No certificate check was disabled, no
STARE bytes acquired, and licensing remains unverified in the fetched excerpt.

Limitations: annotations are masks, not ready-made directed vascular graphs.
Segmentation/skeletonization, physical spacing, flow and cost calibration remain
unbuilt. All acquired annotations are exposed development inputs; not untouched
validation. Reading masks is not completion of P08 G1 (three datasets).

## First HRF extraction, development only

01_h.tif was thinned using scikit-image 0.25.2 skeletonize(method='zhang'), an
established thinning algorithm, not our invention. Documentation fetched:
https://scikit-image.org/docs/stable/auto_examples/edges/plot_skeleton.html
Documentation describes Zhang/Suen (1984). First annotation: 833,888 foreground
pixels -> 75,057 skeleton pixels; 14 eight-neighbor connected components before
and after. Extracted bidirectional eight-neighbor pixel graph: 75,057 vertices,
151,218 directed edges. Component-count agreement alone does not prove anatomical
or full-topological fidelity. A 700x700 native-resolution crop was visually
inspected and shows thin connected vessel lines. No routing/flow result claimed.

hrf_extract.py requires optional Pillow/numpy/scipy/scikit-image dependencies;
core routing remains standard-library only. Full-image Python list/graph creation
can use substantial memory; no 2-GB resource-limit claim. Synthetic TIFF tests
cover a known chain and rejected gray values; missing optional packages skip
these tests explicitly, rather than certify image ingestion.

Access continuation: the exact official STARE HTTP page returned archive hrefs
successfully, avoiding the failed HTTPS certificate route without disabling TLS
verification. HTTP bytes lack transport authentication; no STARE download or
identity/hash correspondence verified yet. Observed label href:
http://cecas.clemson.edu/~ahoover/stare/probing/labels-ah.tar

DRIVE third-party candidate fetched:
https://www.kaggle.com/datasets/andrewmvd/drive-digital-retinal-images-for-vessel-extraction
The mirror says no original license specified and credits original authors;
this is not an official grant. Mirror identity/license/download checks are pending.

## FIVES transferred masks and first extraction

Publisher source/license record: https://api.figshare.com/v2/articles/19688169
Publisher paper: https://www.nature.com/articles/s41597-022-01564-3
Dataset license name verbatim: "CC BY 4.0"; license URL
https://creativecommons.org/licenses/by/4.0/
Transfer agent reports full RAR MD5 matching 789c80dd5376a82063e27fa49192bac9.
This lane independently verified all three transfer part hashes, concatenated ZIP
SHA256 e5df9ba3f301e3d1858ecdfc75384bca6ecc203f91850703656dbd70786da70d,
ZIP CRC, and all 800 file sizes/SHA256s against its transferred manifest.

First training mask 100_A.png is RGB with exactly equal binary channels 0/255.
HRF-only 2D contract rejected it initially. Extractor was explicitly extended to
accept equal RGB channels only, preserve original_shape and reject differing
channels; no averaging/thresholding introduced. 314,052 foreground pixels became
23,952 skeleton vertices and 48,304 directed edges; three eight-neighbor components
before/after. Native skeleton crop visually inspected. This is one development
mask, not all-800 extraction QC. No new routing/flow or anatomy fidelity claim.

## FOVEA transfer and first-mask extraction

Publisher article: https://www.nature.com/articles/s41597-025-04965-2
Dataset metadata: https://api.figshare.com/v2/articles/28329338
License name verbatim: "CC BY"; URL https://creativecommons.org/licenses/by/4.0/
Dataset CC BY is separate from article CC BY-NC-ND. Verified TLS range-fetch
observed ZIP signature; transfer agent reports complete ZIP MD5 equal to publisher
36ca4a0cf119a63f8ff14de7a30ad91b. This lane independently checked transferred ZIP
CRC, exact 160-mask membership, and all per-mask sizes/SHA256s in transfer manifest.
160 vessel masks are 80 preoperative and 80 intraoperative, two annotators over
40 patients. No image/video/optic-disc files in the transfer.

First intraoperative mask FOVEA001_i_ve_1.png: L, 1080x1920, values 0/255.
31,399 foreground -> 10,964 skeleton vertices, 22,206 directed edges. One
8-neighbor component before/after. Native crop visually inspected: thin continuous
centerlines and branch crossings visible. Crossings/loops are pixel topology,
not verified anatomy. No threshold/channel conversion needed. Only first-mask QC.

The narrow three-independent-source first-mask extraction check is now 3/3:
HRF, FIVES, FOVEA. It does not certify whole-dataset extraction, anatomical
fidelity, calibrated flow, independent validation or P08 G2-G4. All inputs are
exposed development; patient/annotator correlation must be preserved in splits.
DRIVE/STARE/CHASE stay pending, not declared unavailable.

## Full-set exact-contract QC, frozen result

All 975 supplied masks were processed once by the unchanged extractor:
HRF 12/15 passed, FIVES 790/800 passed, FOVEA 160/160 passed. Total 962 passed,
13 rejected. HRF rejections were nonbinary grayscale values; FIVES rejections were unsupported
RGBA shape despite exact binary channel values. No component-count failures; rejected values and image SHA256s recorded separately. Full-set QC run
is complete but not passed. No mask dropped or threshold relaxed. All accepted
masks passed component-count equality, which remains limited QC only. The first
interim incorrectly attributed HRF rejection to components; corrected promptly
and per-file records preserve the actual reason.

A future binarization rule would be a new development preprocessing protocol,
not an invisible correction to this frozen result. It requires source-grounded
meaning of intermediate pixel values and sensitivity analysis. Reprocessing must
retain original rejection counts and keep new outcomes separately labeled.

## Separate reject-protocol outcomes

Protocols frozen before application in REJECT_PROTOCOLS.md; per-mask effects are
in reject_protocol_effects.json. HRF threshold >=128 changed diagnostic >0 component
counts 24->13, 50->17, 24->11, so all three stay rejected. FIVES opaque RGBA conversion
changed zero foreground/RGB pixels, preserved component counts and passed the
unchanged skeleton check in all ten derived masks. Original ledger remains
962 accepted / 13 rejected. Separate channel-normalized development QC permits
ten FIVES derived masks; it is not a claim that the original contract passed.
No anatomy/flow validation. No threshold rule promoted into the production extractor.

## Analysis-only three-first-mask topology application

Topology audit is in independent review pending freeze-verification verdict.
Applied without extraction/QC changes to the same HRF/FIVES/FOVEA development
first-mask skeletons. Source and skeleton hashes match earlier audit records.
Components and vertex/edge counts match the extractor's records. Statistics:
HRF endpoints 320, branches 1230, cycle rank 566; FIVES 83/419/203; FOVEA
40/238/140. Zero isolated vertices in these three graphs. Cycle rank is an
8-neighbor pixel representation statistic, not anatomical vascular loops.
These selected masks do not establish dataset-wide behavior or biological fidelity.

## Three-first-mask chain analysis

Chain algorithm independently reviewed; application result still in independent
review. "Lossless" means topological pixel-path representation ONLY: original
edge COSTS are not serialized; no physiological cost inference; not a routing
input. On the same hashed skeletons, HRF 75,057 vertices become 1,550 anchors/2,102
chains; FIVES 23,952 become 502/702; FOVEA 10,964 become 278/417. Every original
undirected edge is represented exactly once. Compressed multigraph cycle ranks
match 566/203/140; this is pixel topology, not biological loops or performance.
No extraction, masks, routing or QC gates changed.

## Exact thinning reproduction independent verdict

VERIFIED exact thinning reproduction for these 3 hashed annotation masks ONLY:
HRF 01_h, FIVES train 100_A, FOVEA001_i_ve_1. Independent review in a fresh pinned
environment checked original byte hashes, channel/binary contracts and external
Zhang thinning, matching all three delivered bool hashes. This closes exact
reproduction uncertainty for those masks only. Still NO anatomical/biological
fidelity, correct vessel-crossing topology, scientific validation, or whole-QC
certification. Real-chain partition verdict is scoped to reproduced-equivalent
skeletons, not biological correctness.
