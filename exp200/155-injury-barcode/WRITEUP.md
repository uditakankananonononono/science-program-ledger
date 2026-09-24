# 155 / DOC-2-055 - Transcriptomic barcode of tissue injury: BOUNDARY (not counted)

Question: do injured organs share a small, conserved expression "barcode"?
Gates were locked before any results (GATES.md, commit 908435e6).

## Result
| held-out organ | barcode | B1 Hallmark INFLAMMATORY | B2 Hallmark TNFA/NFKB |
|---|---|---|---|
| kidney GSE30718 | 0.825 | 0.731 | 0.568 |
| liver GSE38941 | 1.000 | 0.994 | 0.882 |
| skin GSE28914 | 0.943 | 1.000 | 1.000 |
| jejunum GSE37013 | 0.524 | 0.442 | 0.456 |
| mean | 0.823 | 0.792 | - |

- Label-permutation null for the whole leave-one-organ-out pipeline: mean 0.52, p = 0.02.
- G1 FAIL: mean 0.823 clears the 0.80 bar and wins 3 of 4 organs, but the margin over B1 is +0.03, short of the locked +0.05.
- G2 FAIL: on the frozen external GSE139061 (kidney RNA-seq, another lab), barcode AUROC is 0.60, tied with B1 (0.60); B2 scores 0.36.
- G3 PASS: TNFA/NFKB enrichment p = 1.9e-4 (overlap BCL2A1, CXCL6, PTX3, TNC).
- G4 done: the tool is code/score_injury.py, and the nomination is below.

## What the barcode actually is (mechanism)
The final 25 genes fall into three programs:
- Proliferation: RRM2, CCNA2, TYMS, MCM10, CEP55, PBK, KIF14, TRIP13, CKS2, CDKN3.
- Myeloid infiltration: CYBB, FCGR2A, SIGLEC7, SLAMF8, BCL2A1.
- Matrix remodelling: MMP1, TNC, TIMP1, PTX3.

So it is a repair-phase signal that builds over days, not a detector of injury itself. It works where the samples are days into repair (AKI biopsies, liver failure explants, wounds at days 3-7). It is blind to jejunal ischaemia-reperfusion at 0-120 min.

Post-hoc check (exploratory, not gated; code/explore.py): classic immediate-early genes (FOS, EGR1, ATF3, ...) also fail in the jejunum (AUROC 0.42). Surgical control tissue is probably already stressed, so this cohort has no clean acute contrast.

## Prospective nomination
GLIPR1. It is in the barcode, up in every training organ, and has only 2 PubMed title/abstract hits with "injury" (results/pubmed_counts.tsv). It is not a proliferation gene (unlike CEP55 and MCM10, which have 1 hit each). Untested proposal: a candidate pan-organ repair-phase marker.

## Follow-up that attacks the failure (not a gate retry)
- Stratify by injury age: acute (<24 h) vs repair (days), using time-course cohorts.
- Test whether a two-clock model (immediate-early plus repair) transports across organs.

## Data
URLs are GEO series matrices (ftp.ncbi.nlm.nih.gov/geo/series/...) plus the GSE139061 suppl QN csv. Checksums are in SHA256SUMS; raw files are gitignored.
