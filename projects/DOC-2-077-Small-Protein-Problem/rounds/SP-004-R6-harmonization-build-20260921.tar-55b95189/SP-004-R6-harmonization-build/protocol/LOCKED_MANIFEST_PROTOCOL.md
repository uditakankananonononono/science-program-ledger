# SP-004 Round 6 locked harmonization protocol

**Locked:** 2026-09-21 22:17 IST before inspecting candidate file contents or biological outcomes.

## Sampling frame and prospective selection
Sampling frame is the checksum-frozen R5 inventory: first 25 live PRIDE species-keyword results per human/mouse/yeast phrase. Selection uses metadata only.

Priority 1 requires open standardized identification/result files ending mzid, mzIdentML, mzTab, SDRF plus peptide/PSM TSV, or an explicit search/result TSV/TXT/CSV under 200 MB. Projects must have explicit 1% FDR prose in R5 metadata. Rank deterministically by: mzIdentML/mzTab present; then peptide/PSM filename token; then smaller total candidate bytes; then accession. Freeze the top two projects per species. Human and mouse mzIdentML projects are preferred when available. Yeast may use TSV/TXT candidates because no mzIdentML appeared in the frame.

No project is replaced based on biological outcome. A replacement requires a pre-outcome schema failure and uses the next ranked manifest candidate with a dated amendment.

## Harmonization contract
For each frozen project: validate species/sample metadata; inventory files/checksums; parse PSM/peptide sequence, q-value or PEP, decoy/contaminant, protein accession, run/sample. Primary accepts peptide q <=0.01 and requires >=2 unique peptides per canonical protein per study. Shared peptides do not assign detection. Canonical UniProt mapping uses a frozen reference FASTA including reviewed/unreviewed records and a SHA-256. Search parameters recorded: enzyme/digestion, fixed/variable modifications, precursor/fragment tolerance when available.

If standardized processed files cannot expose all fields, the project fails schema. RAW reprocessing is allowed only for a prelocked fixed subset of three runs/project and one identical open pipeline across all species; no RAW bytes are downloaded until storage estimate <=20 GB total and tool/database checks pass.

## Feasibility gate before outcomes
Per species: >=2 schema-valid independent studies; >=200 theoretical-opportunity proteins per arm; >=10 shared Pfam or prelocked MMseqs families; identical acceptance rules across arms; decoy/contaminant removal and q-value verified. If any species fails, it remains non-estimable and is not pooled. Biological outcomes are computed only for species passing all gates.
