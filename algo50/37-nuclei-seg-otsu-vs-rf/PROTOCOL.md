# 37 - Nuclei segmentation: random-forest 3-class pixel classifier vs Otsu + watershed (BBBC039)

Locked before any segmentation is run.

Data: BBBC039 (Broad Bioimage Benchmark Collection; U2OS Hoechst nuclei, 200 images 520x696, expert masks), official split: training 100, validation 50, test 50 (metadata/*.txt). Ground-truth objects: connected components of equal value in the mask red channel (touching nuclei carry different values), skimage label, connectivity 1.

Methods:
- Baseline B: Otsu threshold (Otsu 1979) on Gaussian-smoothed image, fill holes, then distance-transform watershed with peak_local_max seeds (the classical CellProfiler-style pipeline). Tuned on validation over sigma {1,2} x watershed {off; min_distance 5,7,10}; min object size 30 px fixed.
- Method R: random forest pixel classifier (ilastik-style multiscale intensity/edge/texture features from skimage multiscale_basic_features, sigma 1-8), 3 classes (background / nucleus interior / nucleus boundary, boundary = inner boundary of GT objects), trained on 5,000 randomly sampled pixels per training image (class-balanced sampling), 100 trees, max_depth 20, seed 37. Segmentation: seeds = connected components of P(interior) > t, foreground = P(interior)+P(boundary) > 0.5, watershed on -P(interior) restricted to foreground; min object size 30 px. t tuned on validation over {0.4,0.5,0.6}. The 3-class formulation follows Caicedo et al. 2019 (Cytometry A), with an RF instead of a CNN.
Images are percentile-normalized (1st-99.8th) per image for both methods.

Metric: per-image object F1 at IoU >= 0.5 (TP = GT/pred pairs with IoU > 0.5, unique by construction), averaged over the 50 test images; also F1 at IoU >= 0.75. 95% CI from 2000 paired bootstraps over test images (seed 37).
Gates:
- G1 (headline): mean F1@0.5 (R - B) >= 0.03, CI lower bound > 0.
- G2: mean F1@0.75 (R - B) > 0, CI lower bound > 0.
- G3: R >= B in F1@0.5 on >= 70% of test images.
If G1 fails: one post-hoc pivot, locked and pushed before scoring.
Caveats declared: a single cell line and stain; deep learning (e.g. U-Net, reported ~0.9 F1 by Caicedo 2019) is stronger and out of scope; the RF is a learned-feature-free classical pipeline.
