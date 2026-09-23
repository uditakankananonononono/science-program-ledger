# algo50/03 - Explicit n/h/c segmentation scoring for signal-peptide detection

Lane RES-1. Algorithm study (not counted toward the flagship 100). Protocol and amendments were hashed and timestamped before the results they gate (`results/lock.txt`).

## Bottom line
- Primary result PASSED. A small dynamic-programming segmenter that scores an explicit n-region / h-region / c-region parse plus the -3/-1 cleavage motif (6 interpretable features + hydrophobicity) was trained on human and tested on yeast and E. coli with no tuning on those organisms. It beat the amino-acid composition logistic regression on pooled external MCC (0.317 vs 0.261, +0.056, bootstrap 95% CI 0.009-0.105). Compared with the classic hydrophobicity rule, it cut false positives on N-terminal transmembrane anchors (the classic confusion) from 69% to 29%.
- Transfer failed. Absolute MCC outside human is low (0.31 yeast, 0.30 E. coli, gate needed 0.6), even though ranking transfers well (pooled AUROC 0.94). The problem is the operating point, not discrimination.
- Pivot (label-free prior-shift correction, EM of Saerens et al. 2002) FAILED and is informative. At E. coli prevalence (4.6%) it estimated 6.8% and nudged MCC 0.296 -> 0.317. At yeast prevalence (0.65%) EM collapsed to ~0 and predicted no SPs at all (MCC 0). Useful boundary: EM prior correction on a balanced-weight logistic model is unsafe when the target prevalence is below about 1%, so it should not be used for proteome-scale SP screening in organisms with few secreted proteins without a calibration step.
- Bacterial N-terminal TM anchors remain the dominant error: 38% hard-negative FPR in E. coli vs 15% in yeast. Eukaryote-trained n/h/c emissions do not separate them.

## Data
UniProtKB/Swiss-Prot reviewed, protein existence 1, length 60-2000; human (train), yeast S288c and E. coli K-12 (external test); retrieval time + sha256 in `data/`. Positives = SIGNAL at residue 1 with experimental evidence (ECO:0000269/ECO:0007744). Proteins with prediction-only SIGNAL annotations were removed entirely so no model learns SignalP-style labels. Negatives = no SIGNAL. Hard negatives = negatives with a TRANSMEM starting at <= 40. First 70 residues only.
Train: 15,547 human proteins (744 SP). Test: yeast 5,044 (33 SP, 417 hard), E. coli 2,878 (133 SP, 632 hard).

## Results (external, thresholds fixed on human CV)
| Model | pooled MCC | pooled AUROC | hard-neg FPR | yeast MCC | E. coli MCC |
|---|---|---|---|---|---|
| B1 hydrophobicity rule | 0.295 | 0.906 | 0.691 | 0.245 | 0.295 |
| B2 composition LR | 0.261 | 0.937 | 0.235 | 0.229 | 0.246 |
| **P n/h/c segmenter** | **0.317** | **0.939** | **0.288** | **0.313** | **0.296** |
Human 5-fold CV MCC: B1 0.531, B2 0.688, P 0.680.

Gates: G1 PASS, G2 PASS, G3 FAIL. Amendment 1/1b (prior shift): A1 FAIL (pooled 0.307, needed 0.40), A2 FAIL (yeast fell to 0), A3 FAIL for yeast (estimated prevalence 1.5e-6 vs true 0.0065), passes for E. coli (0.068 vs 0.046). Amendment 1 as first written was a no-op decision rule; it was caught and corrected (Amendment 1b) before any result was computed.

Files: `results/results.json`, `results/amend1.json`, `results/nhc_tables.json` (learned emission log-odds), code in `code/`.

## Caveats
- The composition baseline slightly beats P in human CV (0.688 vs 0.680). P's advantage appears only out of distribution.
- Small positive count in yeast (33); yeast MCC intervals are wide.
- The DP emission tables were fit on all human positives before the CV used to pick C and the threshold. That leaks inside human CV only, not into the external tests.
- No comparison with SignalP 6 (licence-restricted download). This is a transparent baseline study, not a SignalP competitor.

## Next direction
Add a bacterial-anchor state (lipobox L-A/S-G/A-C and long uncleaved h-region) to the parse and test on E. coli. Replace EM with a calibration-robust prevalence estimate (for example, the BBSE / black-box shift estimator) for low-prevalence proteomes.

## Reproduce
Download with the query in `PROTOCOL.md` into `data/{human,yeast,ecoli}.tsv.gz`, then `python3 code/run.py; python3 code/amend1.py` (numpy, scikit-learn).
