# Small Protein Evidence Triage - product specification

## User and decision
Primary user: UniProt-like database curator or a microbial small-protein experimental group. Decision: which already-reviewed short-protein records merit a manual evidence review or targeted experiment next.

## Tested input and interface
Input is the included analysis-cohort CSV schema. Output is a CSV, not a black-box score: accession, length, organism, phylum, protein-existence evidence, annotation score, explicit booleans for missing GO/function/PDB/EC evidence, ribosomal/uncertain-name flags, and reason codes. Every rank must be decomposable into reason codes.

## Forbidden behavior
Do not infer protein function, call missing evidence biological absence, recommend clinical action, or silently favor taxa with richer metadata. Never hide negative or ambiguous fields.

## Operational comparison
Manual ad hoc search has high curator control but poor repeatability. Generic annotation scores are reusable but combine evidence dimensions and may obscure the specific gap. This triage adds a short-protein-specific, reason-coded view. It has not yet shown improved curator yield or cost.

## Prospective acceptance test
Randomize 400 eligible accessions to triage-ranked versus random review. Primary endpoint: actionable evidence updates per curator hour. Secondary: redundant-review rate, inter-curator agreement, time per record, taxonomic distribution, and false-priority rate. Success requires >=25% improvement with 95% CI above zero and no major phylum receiving less than half its eligible proportional representation.

## Deployment and monitoring
Nightly or release-based ingestion, schema validation, checksum freeze, human approval, immutable audit logs, and no automatic database writes. Monitor missing-field rate, taxa mix, reason-code mix, API/schema failures, and curator overrides. Roll back on schema mismatch, >5-point unexplained cohort drift, failed checksums, or evidence of systematic taxonomic exclusion.

## Security and economics
No credentials belong in exports; API tokens, if later needed, must be stored separately. Public records reduce privacy risk but not license/attribution duties. Costs are API transfer, storage, and curator time. A commercial value claim requires the prospective time-yield trial and a documented licensing review.
