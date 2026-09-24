# QC audit - P05 CBIO013(2023) mcSTR cancers

Auditor: Doc230 lane A v6 | 2026-09-24 11:03 IST | Every spec read in full; named data sources spot-checked by live fetch (HTTP 200 on portal/API, or an API query returning records). Specs name resources, not accession URLs - OK means the named resource is live and openly fetchable.

Verdicts: OK (build-ready) | FIX (small source/method edit before build) | REWRITE (controlled-access/dead core data or hand-wavy method)

Live checks: GDC API 200, but all 23,723 TCGA WGS BAM files are access=controlled (dbGaP). 1000 Genomes high-coverage FTP 200; HPRC 200; STRchive 200; ExpansionHunter repo 200; DELFI cohort (Cristiano 2019) is EGA controlled (EGAS00001003611); PCAWG portal 200 but raw reads also controlled; ICGC ARGO 200.

THE core blocker: STR genotyping needs raw reads. TCGA WGS is controlled-access, so P05-01 (and everything downstream that says "genotypes from P05-01") cannot run on TCGA without dbGaP approval.

| id | verdict | note |
|----|---------|------|
| P05-01 | REWRITE | TCGA WGS is controlled (verified via GDC API). Open WGS with cancer labels: CCLE cell-line WGS (DepMap/SRA, open) and PCAWG/ICGC summary-level calls. Rewrite around CCLE tumors + 1000G/HGDP controls, or mark dbGaP application as step 0 with the CCLE fallback. |
| P05-02 | FIX | HPRC/HGSVC truth sets fine; drop TCGA from the genotyper benchmark, use 1000G + CCLE. |
| P05-03 | FIX | DELFI raw data is EGA-controlled; the in-silico fragmentation simulation from open WGS (1000G/CCLE) carries the build - say so. |
| P05-04 | REWRITE | Depends on P05-01 genotypes; same CCLE pivot. ICGC/PCAWG validation must use open summary data. |
| P05-05 | REWRITE | TCGA expression is open at gene level but needs P05-01 STR burden; inherits the pivot. MANTIS/MSIsensor public calls OK. |
| P05-06 | REWRITE | Same P05-01 dependency; MSI/MMR calls themselves public. |
| P05-07 | OK | 1000G + HGDP fully open; strongest P05 build, no dependency on P05-01. |
| P05-08 | REWRITE | Inherits P05-01; Liu 2018 endpoints public. |
| P05-09 | FIX | HCC cfDNA raw cohorts are mostly controlled (EGA); lock open-access SRA cfDNA studies by accession or simulate from open HCC WGS (CCLE). |
| P05-10 | FIX | TCGA CRAMs controlled; benchmark on 1000G open CRAMs only (spec already allows - make it the primary). |
