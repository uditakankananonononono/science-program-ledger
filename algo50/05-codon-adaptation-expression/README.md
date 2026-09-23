# algo50/05 - Reference-free codon adaptation and the codon ceiling for predicting yeast protein abundance

Lane RES-1. Algorithm study (not counted toward the flagship 100). Protocol and amendment were hashed and timestamped before the results they gate (`results/lock.txt`).

## Bottom line
- Primary result PASSED. A label-free, self-consistent CAI (SC-CAI) finds its own reference genes from the genome and needs no prior list of highly expressed genes. It matched and slightly beat classic ribosomal-protein CAI on three independent abundance datasets (+0.005 Spearman rho each, paired CIs excluding 0). It converged in 4 iterations. Its 101-gene reference set is 68% ribosomal proteins, and most of the rest are glycolytic genes (TDH1-3, PDC1, ENO1/2, FBA1, TPI1, GPM1) and elongation factors (TEF1/2). It rediscovers the textbook highly-expressed set from sequence alone. Practical use: CAI for any newly sequenced organism with no annotation of ribosomal genes.
- Component failed: codon usage is saturated. A supervised ridge model on all 59 synonymous codon frequencies added only +0.016 / +0.032 rho over one-number CAI (gate +0.05). On genes it had never seen labels for, it did not beat CAI at all on one dataset.
- Pivot PASSED (all 3 gates). The missing signal is in which amino acids a protein uses, not which codons. Adding amino-acid composition and CDS length to codon frequencies raised rho to 0.746 (Kulak) and 0.764 (Mueller), vs 0.653 / 0.670 for CAI (+0.09 each, CIs 0.080-0.107). On clean held-out genes with no training labels, it scored 0.627 vs 0.542 and 0.617 vs 0.535. Amino-acid composition alone reaches rho 0.62, nearly as much as all codon information. That fits the known cost-selection effect: abundant proteins use cheaper amino acids. The 5' "ramp" of slow codons carried no abundance signal (rho ~0, removing it changes nothing).

## Data
SGD S288C verified ORFs (5,080 after QC). PaxDb per-dataset abundances (not the integrated set): Ghaemmaghami 2003 TAP-western (training labels), Kulak 2014 and Mueller 2020 mass spectrometry (evaluation). Retrieval time + sha256 in `data/`; raw files not committed (URLs in `PROTOCOL.md`).

## Results (Spearman rho vs log abundance)
| Index / model | Ghaemmaghami | Kulak | Mueller |
|---|---|---|---|
| GC3 | 0.093 | 0.106 | 0.104 |
| ENC (neg) | 0.424 | 0.522 | 0.544 |
| CAI, ribosomal reference | 0.540 | 0.653 | 0.670 |
| **SC-CAI, label-free** | **0.545** | **0.658** | **0.675** |
| 59-codon ridge (CV) | 0.555 | 0.669 | 0.702 |
| amino-acid composition only (CV) | 0.496 | 0.617 | 0.616 |
| **S2: codons + aa comp + length + ramp (CV)** | **0.620** | **0.746** | **0.764** |
Ablation (Kulak): removing codons -0.124, amino-acid composition -0.050, length -0.012, 5' ramp +0.000.
Gates: G1 PASS, G2 PASS, G3 FAIL; A1 PASS, A2 PASS, A3 PASS. Full numbers: `results/results.json`, `results/amend1.json`; per-gene indices `results/indices.npz`.

## Caveats
- One organism (yeast). The SC-CAI top-2% reference size was fixed in advance, not tuned. Sensitivity to that choice is untested.
- Ghaemmaghami-trained models are evaluated on datasets that share many genes. The clean held-out subset (876 / 1,046 genes) is the honest transfer number, and it is lower.
- The amino-acid composition effect is a known biology result (cost selection). What's new here is its size relative to codon bias on these datasets, not its existence.
- Ribosomal genes identified by name pattern RPL/RPS.

## Next
Run SC-CAI on E. coli and a poorly annotated microbe; test whether the S2 model transfers across species with retraining only on codon weights.

## Reproduce
Download the files listed in `PROTOCOL.md` into `data/`, then `python3 code/run.py; python3 code/amend1.py` (numpy, scipy, scikit-learn, biopython).
