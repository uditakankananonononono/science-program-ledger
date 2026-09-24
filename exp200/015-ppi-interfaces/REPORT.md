# DOC-1-015 REPORT - Predicting PPI Interfaces with Multimodal Embeddings
EXP-1, 2026-09-24. Gates locked BEFORE outcomes (commit c465bf4f). VERDICT: DOCUMENTED BOUNDARY - G1 PASS (narrow), G2 FAIL, G3 PASS; failure tree followed (single passes, no tuning).

## Results (results/gate_scores.json; 183/71/164 proteins, 34k/16k/33k residues)
- G1: multimodal (ESM-2 residue emb 320d + PSSM 20d, logistic C=1.0) Dset_72 AUROC 0.6697 vs PSSM-only 0.5853 (named baseline, SPPIDER lineage) AND ESM-only 0.6674: strict exceed of both -> PASS, but the multimodal gain over ESM-only is +0.0023 - marginal, documented.
- G2: frozen bars AUROC >= 0.72 (Dset_72) / >= 0.70 (Dset_164): got 0.6697 / 0.6310 -> FAIL. (AUPRC: 0.228 / 0.261 vs 16.8% prevalence.)
- G3: top-decile aromatic (W/Y) enrichment 12.7% vs 1.9% bottom (6.7x) - coherent with aromatic hot-spot literature (Bogan & Thorn 1998); bulk hydrophobics REVERSED (17.5% top vs 30.7% bottom) - consistent with modern interface knowledge: hot spots enrich aromatics + charged/polar residues, not bulk hydrophobics. PASS as locked (either direction coherent).
- G4: ppi_interface.py CLI (sequence -> per-residue probabilities + top-decile flags), smoke-tested; Dror lab (DIPS) nomination. Erratum: initial model pickle saved the PSSM-only head from the ablation loop; caught at CLI smoke test, multimodal head re-saved before any report (no outcomes touched).

## Boundary analysis
Fourth consecutive small-PLM boundary with a sharper shape: the 8M PLM DOES carry interface-relevant signal (0.667 ESM-only vs 0.585 classical PSSM - the PLM beats the classical evolutionary feature), and PSSM adds ~nothing on top (+0.002) - consistent with PLMs internalizing evolutionary covariation (Rives et al. 2021). But a linear head on a small PLM stays ~5 AUROC points below the locked bar and ~12 points below published full models (DeepPPISP ~0.79 with DSSP structure features + deep attention head). The gap lives in model scale + task-specific architecture + structure features, not in the data. Program-level rule now supported by 011/012/014/015: small PLMs = strong feature extractors, weak stand-alone predictors/designers; closing residual gaps needs scale or task heads outside this compute envelope.

## Honest limits
512-aa truncation (4 proteins dropped, locked rule); per-residue class imbalance (16.8% positives); linear head fixed at C=1.0 (locked); single-sequence CLI mode uses flat PSSM (documented in CLI).
