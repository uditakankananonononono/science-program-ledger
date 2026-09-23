# algo50/07 - Minimum-length HMM segmentation for intrinsic-disorder regions

Lane RES-1. Algorithm study (not counted toward the flagship 100). Protocol hashed and timestamped before any model was fit (`results/lock.txt`).

## Bottom line
- Primary result PASSED. Thresholding a per-residue disorder score breaks each true region into flickering fragments: 14.3 predicted regions per 1,000 residues vs 2.7 true. A two-state segmentation (Viterbi DP with a switch penalty and minimum region length) on the same score predicts 2.8 regions per 1,000 residues. That more than doubles region-level F1 on held-out DisProt clusters (0.233 -> 0.527, +0.29, bootstrap 95% CI 0.27-0.31) at no residue-level cost (MCC 0.309 -> 0.313, CI of the change -0.003 to +0.012).
- The segmenter is a drop-in post-processor: with switch penalty 0 and minimum length 1 it reduces exactly to thresholding, so it can sit on top of any disorder predictor's per-residue output. Code: `code/seg.py` (numba, linear time).
- Learned composition score: residue AUROC 0.750 vs 0.663 for FoldIndex (charge-hydropathy) and 0.685 for TOP-IDP (+0.087 over FoldIndex, CI 0.071-0.104).
- Transfer gate narrowly FAILED: non-human test AUROC 0.744 (gate 0.75). The useful reading is that there is no transfer gap. Non-human (0.744) is essentially the same as all test proteins (0.750), so the limit is the score itself, not human-specific fitting. The region-level gain transfers unchanged (non-human region F1 0.236 -> 0.526).

## Data
DisProt current release via the public API (URL, retrieval time, sha256 in `data/`; raw file not committed). 3,275 proteins after QC, 19% residues disordered (consensus Structural-state D regions). Split by UniRef50 cluster: 1,842 train, 458 tune (for the segmenter's 2 parameters only), 975 test.

## Results (test, 975 proteins)
| | residue AUROC | residue MCC | region F1 | regions / 1,000 res |
|---|---|---|---|---|
| FoldIndex | 0.663 | - | - | - |
| TOP-IDP (21-window) | 0.685 | - | - | - |
| P score, thresholded | 0.750 | 0.309 | 0.233 | 14.3 |
| **P score + segmentation** | 0.750 | **0.313** | **0.527** | **2.8** (true 2.7) |
Gates: G1 PASS, G2 PASS, G3 PASS, G4 FAIL (0.744 vs 0.75). Full numbers incl. tuning grid: `results/results.json`; fitted model `results/model.pkl`.

## Caveats
- Unannotated DisProt residues are treated as ordered (CAID "DisProt" convention). Some are really disordered, which depresses every model's precision.
- The chosen penalty (8) sits at the edge of the pre-locked grid, and minimum length barely mattered (region F1 is flat across L for a given penalty). A larger penalty might do better. That was not tested, to keep the grid as locked.
- Residue AUROC 0.75 is well below modern deep predictors (CAID top methods). This study is about the segmentation step, not about beating them.
- Bootstrap: 2,000 resamples for region F1 and MCC as locked. The AUROC CI uses 500 resamples (compute limit, not locked). Deviation noted here.

## Next
Apply the segmenter to a strong predictor's per-residue output (e.g. published CAID predictions) to test whether the region-F1 gain holds when the underlying score is much better.

## Reproduce
`python3 code/prep.py; python3 code/run.py` (numpy, scikit-learn, numba), with `data/disprot.json.gz` downloaded from `data/source_url.txt`.
