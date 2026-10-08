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
