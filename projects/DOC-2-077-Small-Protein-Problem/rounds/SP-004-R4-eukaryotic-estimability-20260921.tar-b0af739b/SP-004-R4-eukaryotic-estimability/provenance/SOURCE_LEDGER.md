# SP-004 Round 2 source ledger

## Live data
- UniProtKB REST API, reviewed records, exact cohort URLs in `uniprot_*_url.txt`; retrieved 2026-09-21 UTC with headers and SHA-256. https://rest.uniprot.org/
- GOA GAF releases for human, mouse and yeast from EMBL-EBI FTP; exact URLs, timestamps and hashes retained. https://ftp.ebi.ac.uk/pub/databases/GO/goa/
- QuickGO annotation browser/documentation for evidence-code interpretation. https://www.ebi.ac.uk/QuickGO/annotations
- InterPro official resource for family/domain cross-references. https://www.ebi.ac.uk/interpro/
- UniProt programmatic query guidance. https://www.uniprot.org/help/api_queries
- UniProt manual curation guidance. https://www.uniprot.org/help/manual_curation
- RCSB API documentation. https://www.rcsb.org/docs/programmatic-access/web-apis-overview

## Literature read for interpretation
1. "Exposing the small protein load of bacterial life." https://pmc.ncbi.nlm.nih.gov/articles/PMC10723866/
2. "A Practical Guide to Small Protein Discovery and Characterization Using Mass Spectrometry." https://pmc.ncbi.nlm.nih.gov/articles/PMC8765459/
3. "Hidden in plain sight: challenges in proteomics detection of small ORF-encoded polypeptides." https://pmc.ncbi.nlm.nih.gov/articles/PMC10117744/
4. "A catalog of small proteins from the global microbiome." https://pmc.ncbi.nlm.nih.gov/articles/PMC11364881/
5. "The structural coverage of the human proteome before and after AlphaFold." https://pmc.ncbi.nlm.nih.gov/articles/PMC8812986/ (discovery result; fetch returned no readable content, so no exact claim depends on it)
6. "Microproteins - Discovery, Structure, and Function." https://pmc.ncbi.nlm.nih.gov/articles/PMC10841188/ (discovery result; fetch returned no readable content, so no exact claim depends on it)

## Tooling
Python 3 with pandas, NumPy, SciPy and Matplotlib; versions in `ENVIRONMENT.txt`. MMseqs2, DIAMOND, BLAST, HMMER and Foldseek were not installed, so they were not falsely claimed or emulated. Family information came from live UniProt-linked Pfam and InterPro fields. Sequence features were calculated directly by pinned code.

## Round 4 additions
- All Pfam assignments reparsed from the retained live UniProt TSVs; official Pfam is served through InterPro: https://www.ebi.ac.uk/interpro/entry/pfam/
- UniProt REST cross-references for PeptideAtlas, ProteomicsDB, MassIVE and PRIDE were fetched live after protocol lock. Exact query URLs, UTC times and raw TSV hashes are retained. UniProt API: https://rest.uniprot.org/
- MMseqs2 release binary downloaded from https://mmseqs.com/latest/mmseqs-linux-avx2.tar.gz ; binary version `d401e78c2d18a822cdb1527d7464a043f6035a15`; archive SHA-256 `1fb6d8dfe3c83379d2d59ccda19ffc151b69b80d0a62be4691abcd8b4c19e4f2`.
