# SP-004 Round 6: Proteomics Harmonization Build
## Prospectively frozen PRIDE projects, schemas, and a transport-gated stop

**Date:** 21 September 2026  
**Status:** **HARMONIZATION SYSTEM BUILT; FEASIBILITY GATE FAILED BEFORE OUTCOMES**

## What was built
R6 converted the R5 feasibility inventory into a prospectively frozen measurement plan. Selection used metadata only, before candidate contents or protein outcomes. The deterministic rank preferred mzIdentML/mzTab, then peptide/PSM tokens, smaller processed volume, and accession. Two projects per species were frozen:

- Human: PXD083239 and PXD082999, both mzIdentML, 12 candidate files totaling 509 MB.
- Mouse: PXD084070 (mzIdentML) and PXD082960 (explicit 1% search output spreadsheets), 12 candidate files totaling 213 MB.
- Yeast: PXD077377 (peptide list + SDRF) and PXD077491 (two MSF search files), 4 candidate files totaling 359 MB.

The selected candidate manifest totals 1.08 GB, reducing R5's 112 GB bounded inventory by a prespecified format/size rule rather than outcome-aware convenience.

## Harmonization contract
The included machine-readable schema fixes PSM fields, q <=0.01, decoy/contaminant removal, canonical-only mapping, no shared-peptide assignment, >=2 unique peptides per protein, peptide length 7-35, and required search/database provenance. The manifest includes every API-returned project file location, category, byte size and frozen candidate choice. A validator prevents outcome computation until two studies per species pass download, schema and support gates.

## Transport result
Six representative locked candidates, one per project, were requested from the API-returned PRIDE HTTPS locations. Every transfer failed after retries with OpenSSL `unexpected eof while reading`. The failures affected tiny SDRF, XLSX, mzIdentML and MSF files alike, so this is an environment-to-PRIDE FTP transport blocker, not a size or format result and not evidence that files are missing.

Because zero representative files were retrievable, no candidate schema could be verified. The locked requirement of two schema-valid studies per species failed. No peptide or protein outcome was calculated.

## Why no fallback was used
The protocol allows RAW reprocessing only after standardized processed files fail schema, with a fixed three-run subset and <=20 GB estimate. Here, bytes never arrived, so processed files did not fail schema; transport failed first. Switching to arbitrary mirrors, different projects or outcome-aggregated matrices would break the frozen manifest. The honest action is to preserve the build and hand the exact URLs to an environment with PRIDE FTP/Aspera access.

## Reusable system
- `frozen_projects.csv`: deterministic project choices.
- `frozen_file_manifest.csv`: selected processed candidates.
- `frozen_project_api_files.csv`: all files and API-derived transfer URLs for the six projects.
- `harmonization_schema.yaml`: common accepted PSM/protein contract.
- `download_status.tsv`: exact six transfer outcomes.
- `feasibility_gate.csv`: machine-readable stop state.
- code to regenerate selection and validate the gate.

## Next execution
Run the frozen manifest unchanged on a host with working PRIDE FTP/Aspera. Inspect only the six representative files first. If two projects/species expose the required peptide/q-value/protein fields, download the remaining frozen candidates and freeze canonical proteome FASTAs/checksums. If a project has a pre-outcome schema failure, use the next deterministic ranked candidate with an amendment. Only after protein opportunity, arm size and family gates pass should underdetection be estimated.

## Conclusion
R6 delivered the measurement architecture and reduced the data burden to 1.08 GB of prospectively selected processed candidates. It did not deliver a biological answer because external file transport blocked the required schema validation. That boundary is explicit, reproducible and safer than substituting incomparable summary tables.
