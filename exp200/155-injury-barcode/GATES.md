# 155 / DOC-2-055 - Transcriptomic barcode of tissue injury
Locked 2026-09-24 ~11:50 IST, before any expression analysis.

## Data (public GEO, checksums in data/SHA256SUMS)
- Kidney GSE30718 (GPL570): AKI (28) vs protocol biopsy + nephrectomy (19).
- Liver GSE38941 (GPL570): HBV acute liver failure (17) vs normal (10).
- Skin GSE28914 (GPL570): post-op day 3 + day 7 wounds (11) vs intact (8). "Acute wound" (t=0) is excluded.
- Jejunum GSE37013 (GPL6947): ischaemia, and ischaemia + reperfusion at 30 and 120 min (21), vs control (7).
- Frozen external: GSE139061 (Eadon, kidney RNA-seq, a different lab and platform): AKI (39) vs reference (9).

## Method (fixed)
- Within-sample percentile ranks over the shared genes (order-based; no cross-cohort normalization).
- Per organ, compute the Cohen's d of rank, injury vs control. Barcode = top 25 genes by Stouffer-combined d across the training organs, keeping only genes with d > 0 in every training organ.
- Score = mean percentile rank of the barcode genes.
- Leave-one-organ-out (LOOO): train on 3 organs, test AUROC on the held-out organ.
- Final barcode: trained on all 4 organs, frozen, then applied to GSE139061.

## Baselines (named, published)
- B1: MSigDB Hallmark INFLAMMATORY_RESPONSE (Liberzon et al. 2015, Cell Systems), same rank-mean score.
- B2: Hallmark TNFA_SIGNALING_VIA_NFKB (same paper).
- Null: 1000 random 25-gene sets; label permutation for the barcode derivation.

## Gates
- G1 (LOOO): mean held-out AUROC >= 0.80, AND barcode - max(B1, B2) >= +0.05 on mean, AND barcode >= best baseline in >= 3 of 4 held-out organs.
- G2 (frozen external): the all-organ barcode on GSE139061 has AUROC >= 0.75 and is >= the best baseline.
- G3 (mechanism): the barcode is enriched (hypergeometric p < 0.01 vs the shared-gene universe) for >= 1 of Hallmark TNFA_NFKB, P53_PATHWAY, HYPOXIA, UNFOLDED_PROTEIN_RESPONSE, APOPTOSIS. These are stress programs literature ties to injury (e.g., ATF3/KLF6/HBEGF immediate-early injury response).
- G4 (tool + nomination): a CLI that scores any gene-by-sample matrix, plus one prospective nomination: the barcode gene with the fewest PubMed hits for "<gene> AND injury", named as an untested pan-organ injury marker.
- PASS = G1 and G2 and G3 and G4. Otherwise it is a documented boundary. Negatives are kept; no re-fishing (no changing K, organs or contrasts after results).
