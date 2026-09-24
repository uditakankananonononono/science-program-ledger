# GATES - DOC-1-028 (locked 2026-09-24 08:16 IST, BEFORE any scoring)

## Claim
A spatially-AWARE biomarker (tumor cholesterol-synthesis score vs CD8 T-cell neighborhood exclusion)
separates anti-PD1 responder from non-responder MC38 tumors, while the spatially-AGNOSTIC
pseudo-bulk cholesterol score does NOT - a quantitative replication of the published claim
(GSE284989 paper: bulk RNA-seq detected immune correlates but MISSED cholesterol synthesis;
spatial analysis detected it, linked to cytotoxic CD8 exclusion).

## Data (eligibility verified BEFORE this lock)
GSE284989: 10x Visium of 16 MC38 tumors, 8 IgG / 8 aPD1 (5-day treatment). Response labels in
sample titles: aPD1_NR = m09-m14 (6 mice, 6 sections), aPD1_R = m15 (2 sections) + m16 (3 sections).
Response definition per the paper: level of immune cell infiltration (clinical hallmark).
Verified on m09 h5 (08:15): 20,551 genes x 3,211 barcodes; all 15 signature genes present
(Hmgcr/Sqle/Mvd/Ldlr/Srebf2/Fdft1 + Cd8a/Cd8b1/Gzmb/Prf1 + Cd3e/Ptprc/Col1a1/Epcam).
IgG controls are NOT response-labeled and are excluded from all gates.
Small-n disclosure: 6 NR vs 2 R; all inference is exact-test based, no AUROC claims.

## Locked gene lists and scores (parameter-free, no fitting anywhere)
- CHOL (cholesterol synthesis, HALLMARK_CHOLESTEROL_HOMEOSTASIS core enzymes):
  Hmgcs1, Hmgcr, Mvk, Pmvk, Mvd, Idi1, Fdft1, Sqle, Ldlr, Srebf2 (10 genes).
- CD8 (cytotoxic T): Cd8a, Cd8b1, Gzmb, Prf1 (4 genes).
- TPAN (T-cell panel, sanity): Cd3d, Cd3e, Cd8a, Cd8b1, Gzmb, Prf1 (6 genes).
Per-spot score = mean log1p(counts/library*1e4) over signature genes. If any listed gene is absent
from a sample's matrix, that sample is dropped and the fact reported (no list edits post-lock).

## Locked features (per section, then per tumor = median over its sections)
- F1 (spatial arm): kNN graph k=6 on spot coords (tissue-covered spots only);
  exclusion index = Pearson corr over spots of (CHOL_i, mean CD8 of i's graph neighbors).
  Strongly negative = cholesterol-high spots sit in CD8-poor neighborhoods = exclusion.
- F2 (bulk baseline, published negative): mean CHOL over all tissue spots (pseudo-bulk).
- F3 (sanity, published positive): mean TPAN over all tissue spots (pseudo-bulk infiltration).

## Gates
- G1 (sanity halt): F3 ranks BOTH R mice in the top 3 of the 8 treated tumors. Else labels/data
  incoherent (the label IS infiltration level) - document, stop.
- G2 (dev claim): F1 separates perfectly - both R mice rank in the TOP 2 of 8 by F1
  (least exclusion), exact p = 1/C(8,2) = 0.036 - AND F2 fails to separate (at least one NR
  mouse with F2 below at least one R mouse), replicating the published bulk miss.
- G3 (frozen validation): (a) section replication - F1 computed per SECTION ranks every m15/m16
  section above the median F1 of the 6 NR tumors; (b) leave-one-mouse-out - G2's perfect
  separation holds in all 8 LOO iterations. No independent external cohort of aPD1-treated MC38
  Visium with response labels exists publicly; section replication + LOO is the frozen leg,
  documented as such.
- Failure tree: if G2 fails on imperfect F1 separation -> ONE pre-registered rescue P1 =
  bivariate Moran's I (CHOL x neighbor-CD8) as the spatial statistic, same cohort, same gates.
  If P1 also fails, or G3 fails -> DOCUMENTED BOUNDARY (no further arms).
- G4 (mechanism, runs regardless): which CHOL genes drive F1; per-region localization of
  exclusion (tumor-core vs edge via Epcam/Col1a1); comparison to the paper's reported subsets.
- G5: working CLI spatial_biomarker.py + one prospective lab nomination.

## Prospective lab nomination (locked)
An immuno-oncology spatial core running Visium on pre-treatment biopsies from ICI trials
(e.g. neoadjuvant anti-PD1 cohorts): apply the locked exclusion index as a candidate spatial
biomarker with marker-concordance readout.

## Scoring discipline
Sample manifest + hashes committed before ANY feature is computed. Thresholds never relax after
seeing results; errata go in a GATES_ADDENDUM locked before the outcomes they govern.
