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
