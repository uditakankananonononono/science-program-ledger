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
