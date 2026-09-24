# QC audit - P03 CBIO008(2024) EZH2 drug discovery

Auditor: Doc230 lane A v6 | 2026-09-24 11:03 IST | Every spec read in full; named data sources spot-checked by live fetch (HTTP 200 on portal/API, or an API query returning records). Specs name resources, not accession URLs - OK means the named resource is live and openly fetchable.

Verdicts: OK (build-ready) | FIX (small source/method edit before build) | REWRITE (controlled-access/dead core data or hand-wavy method)

Live checks: ChEMBL target API 200; RCSB full-text search returns 43 EZH2/PRC2 entries; DUD-E 200; DepMap portal 200; PRISM repurposing page 200; CryptoSite 200; MOSES repo 200; PubChem resolves tazemetostat (CID 66558664).

| id | verdict | note |
|----|---------|------|
| P03-01 | OK | PDB + ChEMBL actives + decoy generators all live; strongest docking build. |
| P03-02 | OK | DepMap 24Q public downloads live. |
| P03-03 | OK | CryptoSite + PocketMiner sets live; GROMACS open. |
| P03-04 | FIX | "Pocket2Mol weights if license permits" is a hedge; lock the generator + license check as step 0, fallback MOSES-only. |
| P03-05 | OK | PRC2 holo structures verified via RCSB search. |
| P03-06 | OK | ChEMBL dual-potency query is concrete; AlphaFold EZH1 available. |
| P03-07 | OK | PRISM 19Q/24Q public on DepMap portal. |
| P03-08 | OK | Co-crystals + COSMIC public tier; FoldX/Rosetta academic-free. |
| P03-09 | OK | DepMap co-dependency public; NB screens on GEO. |
| P03-10 | OK | Meta-build over P03-01..06 data; all free tooling named. |
