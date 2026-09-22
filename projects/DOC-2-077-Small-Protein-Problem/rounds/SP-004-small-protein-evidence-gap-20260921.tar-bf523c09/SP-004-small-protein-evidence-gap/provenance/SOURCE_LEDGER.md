# Source and provenance ledger

## Data sources
| Source | Exact URL | Use | Retrieval record | Confidence |
|---|---|---|---|---|
| UniProtKB REST, reviewed bacteria 30-100 aa | See `uniprot_short_url.txt` | Primary case cohort, live TSV | UTC time, response headers, raw SHA-256 preserved | High; authoritative database export |
| UniProtKB REST, reviewed bacteria 101-200 aa | See `uniprot_control_url.txt` | Primary control cohort, live TSV | UTC time, response headers, raw SHA-256 preserved | High; authoritative database export |
| RCSB PDB Search API | https://search.rcsb.org/ | Independent structure-link audit | 80 deterministic raw JSON responses | High for database concordance, not biological truth |

Raw hashes:
- `uniprot_short.tsv`: `e1e7bd309473525e619ac405462d0c3c3cee9fe09258a7cd6fa1e237acdaa92e`
- `uniprot_control.tsv`: `e1c081a7a716dcf59e8bd4eca030933b64f6dc9f1d57b67a0c7372efc584d8fb`

## Literature and documentation read before interpretation
1. Hemm et al./FEMS Microbiology Reviews, "Exposing the small protein load of bacterial life." https://pmc.ncbi.nlm.nih.gov/articles/PMC10723866/ - current review of discovery burden, definitions, and experimental/computational limits.
2. Storz et al., "Small Proteins; Big Questions." https://pmc.ncbi.nlm.nih.gov/articles/PMC8765408/ - biological roles and open questions.
3. "Hidden in plain sight: challenges in proteomics detection of small ORF-encoded polypeptides." https://pmc.ncbi.nlm.nih.gov/articles/PMC10117744/ - size-dependent proteomics detection limitations.
4. "Unraveling the hidden universe of small proteins in bacterial genomes." https://pmc.ncbi.nlm.nih.gov/articles/PMC6385055/ - search lead; fetch returned no readable content, so no result claim relies on its text.
5. UniProt manual curation documentation. https://www.uniprot.org/help/manual_curation - interpretation of reviewed records and manual curation.
6. UniProt protein-existence documentation. https://www.uniprot.org/help/protein_existence - interpretation of protein-existence fields.
7. RCSB PDB Web APIs overview. https://www.rcsb.org/docs/programmatic-access/web-apis-overview - API semantics.
8. RCSB PDB Search API documentation. https://search.rcsb.org/ - independent accession query design.

## Claim boundaries
The experiment measures evidence fields in a frozen export of reviewed UniProtKB bacterial entries. It does not estimate how many small proteins exist, prove that an empty field means unknown biology, or infer causation from sequence length. Reviewed-entry selection likely removes much of the discovery deficit and must be treated as selection on evidence.
