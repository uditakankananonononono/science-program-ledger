# QC audit - P01 CBIO003 CRC gut microbiome

Auditor: Doc230 lane A v6 | 2026-09-24 11:02 IST | Method: every spec read in full; named data sources spot-checked by live fetch (HTTP 200 on portal/API, or real API query returning records). Specs name resources, not accession URLs - a verdict of OK means the named resource is live and openly fetchable, not that every cohort was downloaded.

Verdicts: OK (build-ready) | FIX (small source/method edit before build) | REWRITE (dead or controlled-access core data, or hand-wavy method)

Live checks: curatedMetagenomicData Bioconductor page 200; SRA runinfo API for PRJEB10878 (Zeller) 200; GMrepo 200; MGnify studies API 200; ENA read_run for PRJNA743918 (Wastyk 2021) returns runs; IBDMDB/HMP2 200.

| id | verdict | note |
|----|---------|------|
| P01-01 | OK | 6 named cMD cohorts all in the package; Indian cohort must be named by BioProject before build (GMrepo search). Strongest build candidate. |
| P01-02 | OK | cMD metadata + SRA run tables both live. |
| P01-03 | FIX | SBS88 annotations need paired tumor WGS (PCAWG/TCGA raw = controlled). Drop the SBS88 link or use published summary tables only. |
| P01-04 | OK | cMD ships HUMAnN pathway tables. Note: Hannigan 2018 is not in current cMD - swap for Vogtmann 2016. |
| P01-05 | OK | Concrete stability selection + cost model. |
| P01-06 | FIX | "EOCRC-focused SRA submissions" is unnamed; lock the cohort list (age metadata exists in Yachida/Wirbel). TCGA tissue microbiome = use published contamination-corrected tables (Poore 2020 revised / Sepich-Poore), not raw reads. |
| P01-07 | OK | Zeller/Feng adenoma arms + Yachida stage labels are in cMD. |
| P01-08 | OK | iHMP-IBD live; CRC repeat-sampling "where available" is optional. |
| P01-09 | FIX | Wastyk verified; "Mediterranean-diet Prevotella studies" and FMT cohorts are unnamed - name BioProjects or cut to Wastyk + one named FMT cohort. |
| P01-10 | FIX | Paired FIT + metagenome is thin publicly (Zeller 2014 has FOBT). Lock the exact cohort(s) with FIT/FOBT columns before build; else it is a pure simulation and must say so. |

## Data-integrity rules (project-level, inherited by all P01 builds and future specs)
- 2026-09-24: curatedMetagenomicData ThomasAM_2019_c (Japan, 80 samples) duplicates YachidaS_2019
  (every profile has a Yachida match at cosine >= 0.9995). Never combine the two in one analysis;
  use YachidaS_2019. Found in P01-06 (see p01-06-early-onset-crc/REPORT.md).
- 2026-09-24: DE-Wirbel (Wirbel 2019 CCMD / cMD WirbelJ_2018) is confounded by sequencing instrument
  (54/54 HiSeq 2000 = CRC; 60/66 HiSeq 4000 = control). Do not use it for marker discovery or
  within-cohort accuracy claims. Found in P01-02.
- 2026-09-24: in P01-01/P01-04 data, labels "AT-Wirbel" = FR-Zeller and "CN-Feng" = AT-Feng (erratum 535ff418).
