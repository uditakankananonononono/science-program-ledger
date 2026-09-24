# QC audit - P04 CBIO012 gene-synergy / drug-synergy

Auditor: Doc230 lane A v6 | 2026-09-24 11:03 IST | Every spec read in full; named data sources spot-checked by live fetch (HTTP 200 on portal/API, or an API query returning records). Specs name resources, not accession URLs - OK means the named resource is live and openly fetchable.

Verdicts: OK (build-ready) | FIX (small source/method edit before build) | REWRITE (controlled-access/dead core data or hand-wavy method)

Live checks: drugcomb.org and api.drugcomb.org both DOWN (connection failure, repeated) - full database mirrored on Zenodo (records 18756096 update, 18449193 raw, 4843919 oct2019-with-doses). NCI-ALMANAC wiki 200. GoBERT: official implementation exists (GitHub MM-YY-WW/GoBERT, "Gene Ontology Graph Informed BERT"). DrugCombDB 200. ClinicalTrials.gov API v2 200.

| id | verdict | note |
|----|---------|------|
| P04-01 | FIX | DrugComb portal down; use Zenodo mirror (record 18756096) - cite mirror, not portal. GoBERT repo verified. |
| P04-02 | OK | GoBERT repo + GO/GOA + BioGRID/STRING all public. |
| P04-03 | FIX | Same DrugComb mirror note; synergyfinder open. |
| P04-04 | FIX | Same mirror note; NCI-ALMANAC live. |
| P04-05 | FIX | Same mirror note; Chemprop public weights exist. |
| P04-06 | FIX | DrugCombDB live; mirror note for DrugComb. |
| P04-07 | FIX | Mirror note; GOA matching concrete. |
| P04-08 | FIX | Zenodo snapshots give versioned releases for the time-split - actually easier than the portal; still FIX for the citation swap. |
| P04-09 | FIX | Brochado dataset is on the EMBL-EBI GWAS/arrayexpress side - name the accession (E-GEOD/E-MTAB) before build; "GoBERT-equivalent embeddings" needs a locked substitute (protein LM embeddings). |
| P04-10 | FIX | DrugBank open tier is limited; swap to open DDI sources (TWOSIDES/FAERS, ONCOKB public) or state the license step. ClinicalTrials API live. |
