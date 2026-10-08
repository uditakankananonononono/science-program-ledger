# Separately frozen development protocols, October 8, 2026

Original exact-contract ledger: 975 processed, 962 accepted, 13 rejected. Never
modify these outcomes or accepted masks. Corrected failure classes: HRF 3 with
intermediate grayscale, FIVES 10 unsupported RGBA, not nonbinary FIVES values.

## HRF-gray-v1

Only 11_h.tif, 12_h.tif, 13_h.tif. Use original 2D grayscale data. Baseline foreground
for this diagnostic is every nonzero pixel (value > 0), not a claim about publisher
intended segmentation. Proposed binary foreground is value >=128, output 0/255.
No other mask touched. Report changed pixel count, baseline/proposed foreground
counts and 8-neighbor components. If component count changes, keep mask rejected.
Component equality is only limited QC and does not authenticate this threshold's
biological meaning. No clean-mask retuning or scientific claim.

## FIVES-opaque-RGBA-v1

Only the 10 originally rejected FIVES RGBA masks listed in the frozen pixel audit.
Require 4 channels, exactly equal R/G/B, RGB values only 0/255, and alpha==255 at
every pixel. Strip the constant opaque alpha and select the unchanged R channel.
Otherwise retain rejection. No averaging, compositing, thresholding, resizing or
pixel modifications. Compare 8-neighbor components of original R foreground and
output foreground, record changed RGB pixel count (must be zero), alpha range and
channel-equality checks. Run unchanged skeleton/component gate on derived 2D masks.
Originals and original ledger retained; derived QC is a separate result only.
