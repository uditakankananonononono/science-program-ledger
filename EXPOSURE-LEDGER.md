# Exposure Ledger

Program-wide record of every dataset/source any agent has opened VALUES from, so no lane can accidentally claim an "untouched" locked test on a touched source.

**Rule: any lane planning a locked/frozen test must check this ledger AND send candidate accessions to parent for a cross-agent exposure check BEFORE opening values. "Untouched" means untouched by ANY agent on the program.**

| Source accession/ID | Lane/agent | What was opened | Date | Status |
|---|---|---|---|---|
| Townsend 2021 Figure 3 matrix | phage lane agent-01M3MNEJHBME8Y4RZYJ9RNTQKF | matrix image viewed (no transcription by lane; independent analyst transcribed later under protocol) | 2026-09-29 00:27 IST | outcome-exposed (disclosed in prereg v0.1.2) |
| PXD005144 processed CSV | biomarkers-25 agent-01M39X0ERCTCN72VNWC4J7G7MQ | header + 2 rows incl author ANOVA p/fold-change + abundance cells | 2026-09-29 03:56 IST | outcome-exposed, exploratory-only |
| PXD039273 processed TSV | biomarkers-25 agent-01M39X0ERCTCN72VNWC4J7G7MQ | 1 protein quantity pre-prereg | 2026-09-29 03:56 IST | values-exposed, exploratory-only |
| GSE45603 (PPD) | biomarkers program history | values analyzed previously | pre-2026-09-29 | values-exposed |
| GSE290313 (PPD) | biomarkers program history | values analyzed previously | pre-2026-09-29 | values-exposed |
| GSE238208 (IC, P25) | biomarkers program history | values analyzed previously | pre-2026-09-29 | values-exposed |
| GSE271363 (PCOS, P46) | biomarkers program history | values analyzed previously | pre-2026-09-29 | values-exposed |
| GSE7846 (endometriosis) | biomarkers program history | values analyzed previously | pre-2026-09-29 | values-exposed |
| GSE47360 (endometriosis) | biomarkers program history | values analyzed previously | pre-2026-09-29 | values-exposed |
| GSE67311 (fibromyalgia) | biomarkers program history | values analyzed previously | pre-2026-09-29 | values-exposed |
| preeclampsia datasets (exact accessions TBD by lane from metadata, no value viewing) | biomarkers program history | prior completed outcomes exist in shared-core results dir (pe_p21/p24/p42/p44) + NOVELTY_PLAN files with past failed tests and exposed leads | pre-2026-09-29 | values-exposed |
| long-COVID datasets (exact accessions TBD by lane from metadata, no value viewing) | biomarkers program history | prior completed outcomes exist in shared-core results dir (longcovid_p36/p37/p38) + NOVELTY_PLAN files with past failed tests and exposed leads | pre-2026-09-29 | values-exposed |
| ME/CFS datasets (exact accessions TBD by lane from metadata, no value viewing) | biomarkers program history | prior completed outcomes exist in shared-core results dir (mecfs_p29/p32/p41 + p33_test_predictions.csv) + NOVELTY_PLAN files with past failed tests and exposed leads | pre-2026-09-29 | values-exposed |
| Macadangdang Bov/Bfi (S4/S5) | item-27 lane (self-report) | S4/S5 outcome values opened | 2026-09-29 | exploratory/source-curation-exposed - NEVER usable as untouched locked-test data |
| Hankyphage jmh42/jmh47/jmh51 (PLOS S1 Data/S3) | item-27 lane (self-report) | S1 Data/S3 source values opened | 2026-09-29 | exploratory/source-curation-exposed - NEVER usable as untouched locked-test data |
| BA000039.2 (decoy source) | item-27 lane (self-report) | source features opened | 2026-09-29 | exploratory/source-curation-exposed - NEVER usable as untouched locked-test data |
| CP008934.1 (decoy source) | item-27 lane (self-report) | source features opened | 2026-09-29 | exploratory/source-curation-exposed - NEVER usable as untouched locked-test data |
| MN270259.1 (decoy source) | item-27 lane (self-report) | source features opened | 2026-09-29 | exploratory/source-curation-exposed - NEVER usable as untouched locked-test data |

## 2026-09-29 16:07 IST - item-27 / CZI genome-scale T-cell Perturb-seq (CD4 cohort) - EXPOSED (self-correction)

Source: item-27 lane self-correction via Main; grounding docs in mega27-27-isef-bioinf-derived-tools: docs/CELLPERTURB-CD4-COHORT-LEAD.md, docs/CELLPERTURB-CD4-ELIGIBILITY-AUDIT.md.
- EXPOSED (exploratory only, NEVER to be called untouched): CD4 author DE-summary CSV (outcome-derived values) + guide library/QC flag values; prior inspection documented of author guide library, DE-summary CSV, and the 24-target CD8/CD4 crosswalk with QC flags.
- NOT downloaded but SHARE SOURCE/STUDY with exposed summaries, therefore NOT pristine test material: the 16.79GB gene-wise DE matrix (.h5ad) and 44.57GB pseudobulk.
Earlier same-day check (16:05): GSE314342 absent program-wide; CZI cohort references then found were the lead/manifest metadata - superseded by this self-correction.

## 2026-09-29 16:08 IST - item-27 / CZI CD4 GWCD4i.DE_stats.h5ad - METADATA-PROBE exposure (development-only)

Approved development-only probe (item-27 lane via Main): S3 object GWCD4i.DE_stats.h5ad, ETag c9ff52fcc6d6ce8a387a76dc757a5b97-2002, version IJHj.CZ2Hhw9sa41IuovIGpBZimEZo7I. 21,498,456 bytes read via 86 HTTP 206 range requests; HDF5 metadata/layout only (six DE layers, 33,983 x 10,282). NO numerical DE cell values read.
Lane finding noted: this matrix is pooled target/condition DE, NOT donor-specific labels; donor-heldout prediction would require the separate donor-pair .h5mu (not probed, not downloaded).

## 2026-10-10 06:23 IST - mega27-13-synthetic-lethal-rl - PUBLIC visibility flip + 57 unrecorded commits

Found during DOC-1-047 collision screen (Main 06:22 record-fix instruction):
- Repo is now PUBLIC (GitHub API: private:false, updated_at 2026-10-08T10:07:40Z). Created PRIVATE 2026-09-26. No record in this ledger of who flipped visibility or when. The flip is consistent with her all-repos-public direction, but the missing record is noted here.
- Live main HEAD 263e7d484cf98bb971abef417e12a641b09891c4; last ledger-recorded head was 3b12bd54 (2026-09-28). 57 commits landed between them, NONE recorded in this ledger: 43 authored "Instinct Agent <agent@instinct.com>", 13 "Udita PHOOKAN", 1 "lane <lane@example.invalid>". Latest commit 2026-10-08 04:32 IST.
- Content of the unrecorded span: paper/ directory now exists (Sep 28 record said "no paper exists"), judge round R01 v2 archived with adjudication, frozen gene-disjoint contextual experiment (HARLE-GENE-DISJOINT-CONTEXTUAL-FREEZE/RESULT: frozen pre-run, executed, "no demonstrated value" recorded), Harle benchmark negatives (HARLE-CATEGORY-BENCHMARK-NEGATIVE), GSE154112 negatives. HEAD commit 263e7d4 is a README pointer to those recorded negatives.
- Lane status: active as recently as 2026-10-08 04:32 IST by commit evidence; quiet since (~46h at time of record). Builder deploy keys synthetic-lethal-rl-builder-20260926/-20260928 remain the recorded write path; private halves in lane workspace(s) unknown to registry.
