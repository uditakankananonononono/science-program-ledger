# QC audit - P02 CBIO006 ferroptosis / AD antibodies

Auditor: Doc230 lane A v6 | 2026-09-24 11:02 IST | Every spec read in full; named data sources spot-checked by live fetch (HTTP 200 on portal/API, or an API query returning records). Specs name resources, not accession URLs - OK means the named resource is live and openly fetchable.

Verdicts: OK (build-ready) | FIX (small source/method edit before build) | REWRITE (controlled-access/dead core data or hand-wavy method)

Live checks: AD Knowledge Portal, SEA-AD, CELLxGENE, FerrDb V2, SAbDab, SKEMPI 2.0, FinnGen R10, iLINCS all 200; AlphaFold Q9NP59 200; RCSB 6W4S 200; gnomAD GraphQL returns SLC40A1. OpenGWAS API 401 without token.

Access: AMP-AD on Synapse needs a free account + terms. UK Biobank and ADNI need applications.

| id | verdict | note |
|----|---------|------|
| P02-01 | OK | Synapse + GEO + FerrDb; concrete classifier. |
| P02-02 | FIX | CSF SomaScan/Olink sets unnamed; name PRIDE accessions or restrict to AMP-AD TMT. |
| P02-03 | OK | SAbDab/SKEMPI live; good docking/DL candidate. |
| P02-04 | OK | Structure + variant sources verified. |
| P02-05 | FIX | OpenGWAS needs free token; add GWAS Catalog FTP route. |
| P02-06 | OK | Census live; cohorts present. |
| P02-07 | OK | L1000 public via iLINCS. |
| P02-08 | OK | Hepcidin-ferroportin PDB structures live; ChEMBL + open ADMET tools named. |
| P02-09 | OK | Literature PK compilations + TfR shuttle factors; analysis spec, no data block. |
| P02-10 | FIX | ADNI + UK Biobank Olink both need applications; restrict to AMP-AD/Emory public CSF-plasma sets or mark as registered-access. |
