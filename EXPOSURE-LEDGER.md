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
