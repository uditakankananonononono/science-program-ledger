# Unit 192 - expression deconvolution (variance-aware reweighted simplex LS vs NNLS / nu-SVR)
Status: DROPPED pre-lock at DEV gate. No prereg locked, no TEST mixture scored or opened.
Data: GSE19830 (rat brain/liver/lung mixtures, RMA log2, known proportions), GSE11058 (human immune cell-line mixtures, MAS5; true proportions parsed from the GEO series overall_design text: relative amounts MixA-D, normalized to sum 1; amounts are relative cell inputs, not RNA fractions - caveat).
Split: D1 DEV = mixtures with sha256(label)[0] hex < 8 (5 of 11 mixtures, 15 samples); D2 DEV = MixA, MixB. TEST mixtures never loaded in dev.py.
Degraded arm (DEV only): Poisson thinning of intensities at total counts 3e5, 1e5, 3e4, seed 20261010, 3 draws each; references stay clean.
Grid (DEV): signature genes/type N in {50,100,200,500}; nu in {.25,.5,.75}; lambda in {.01,.1,1}.
DEV gate (stated before running): candidate must beat the DEV-best baseline by >=5% RMSE on the DEV degraded arm.
Results (mean per-sample RMSE of proportions, DEV):
D1 best baseline: natural 0.0395 (nuSVR .75, N=200); degraded 0.0417 (nuSVR .75, N=500).
D1 best candidate: natural 0.0411, degraded 0.0428 (vwsr lam .01, N=100) -> 2.5% WORSE than best baseline degraded, 4% worse natural.
D2 best baseline 0.0659 nat / 0.0674 deg (nuSVR .25, N=50); best candidate 0.0728 nat / 0.0749 deg -> worse.
Candidate also collapsed at N=500 on D1 (RMSE ~0.066-0.071).
Verdict: candidate does not clear the gate on either dataset. Dropped. Not a TEST result; no claim. Note: nuSVR best nu sits at the grid edge (.75) on D1, so the baseline is if anything under-tuned; this does not change the drop.
Hashes: u192.py 39bf7911..., dev.py faf06ecf..., dev_results.json 24e5b30f..., dev.log 703f229f...

Drive: drop record https://drive.google.com/file/d/1s5tI7d8x7-P-WbtivHsW2pdTKf0Zvx4V/view ; code+results tgz https://drive.google.com/file/d/1RdBbV_xJnhIFKF5qPdMzy20VhfArVxIK/view
Ledger row: 192 | expression-deconvolution-vwsr-vs-nusvr | DROPPED at DEV gate, pre-prereg (candidate failure vs nuSVR) | 2026-10-10
