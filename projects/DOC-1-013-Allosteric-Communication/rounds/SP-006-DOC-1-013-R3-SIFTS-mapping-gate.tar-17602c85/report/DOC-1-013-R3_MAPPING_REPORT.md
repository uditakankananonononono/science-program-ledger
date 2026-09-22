# DOC-1-013 R3: SIFTS mapping repair and outcome-protocol lock

## Result
The mapping preflight passed, so the R3 outcome protocol was frozen. No embedding or pathway model was run before this gate.

## Pinned sources
Two SIFTS flat files were downloaded live from EMBL-EBI and retained verbatim: `pdb_chain_uniprot.csv.gz` and `uniprot_segments_observed.csv.gz`. Both were last modified 13 September 2026. Their internal headers identify SIFTS 2026-09-13, PDB 37.26 and UniProt 2026.04. SHA-256 hashes are in the manifest. SIFTS is the authoritative PDBe-UniProt mapping source and explicitly handles missing observed regions, variants, isoforms, engineered mutations and chimeric structures.

## Benchmark-level mapping result
The 2,257 AlloBench records represent 429 targets and 2,146 PDB IDs. A target passed the segment preflight if at least one record had a SIFTS mapping joining its declared canonical UniProt accession to the chain encoded in its curated allosteric-site strings. 416/429 targets passed (96.97%), above the required 80%.

This is a segment-level feasibility result, not yet a residue-level outcome cohort. The frozen outcome protocol requires exact residue round trips, insertion-code preservation, residue-name agreement, observed-coordinate status, canonical accession identity, and exclusion of ambiguous/chimeric mappings.

## Mandatory contradiction: 4UC5
AlloBench record 4UC5/Q9K169 contains modulator chain A while every curated allosteric-site residue is on chain B. SIFTS maps Q9K169 on site chain B. These fields describe different roles and must not be conflated. R3 therefore keeps `modulator_chain` and `site_chain` separate. Site labels map only through chain B. This resolves the contradiction without rewriting source data or leaking across chains.

Across AlloBench, 252 records have a modulator chain that is not among the chain(s) encoded by the curated allosteric residues. All are flagged in `segment_mapping_audit.csv`.

## Independent control sample
Thirty records drawn from the beginning, middle and end of the eligible sorted audit were queried against the live PDBe UniProt mapping API. All 30 returned the expected canonical accession and site chain (100%), exceeding the 95% control threshold. URLs, status codes, byte counts and response hashes are retained. This check verifies accession/chain round trips at segment level. Exact author-number/insertion-code checks remain mandatory during cohort construction.

## Zero cross-chain leakage rule
A site chain is parsed from each curated residue string. Mapping joins require PDB ID, canonical accession and that exact chain. Modulator chain is never substituted. Outcome inclusion requires the exact site residue to return to the same author chain, residue number and insertion code. Any cross-chain return is an exclusion.

## Limitations and remaining work
- The bulk observed-segment file describes ranges, not every insertion code. Per-entry SIFTS residue records are required for final labels.
- The 30-control PDBe API check validates accession/chain consistency, not every residue.
- RCSB/PDBrenum-equivalent residue-level cross-check remains an outcome-cohort requirement under the frozen protocol.
- Construct mutations and sequence conflicts must be read from residue-level SIFTS annotations; they were not inferred from range files.
- Passing the mapping preflight says nothing about model performance. R0 remains preliminary until the family/physics replication runs under the now-frozen protocol.

## Files
- `results/preflight_gate.json`: exact benchmark gate result and 4UC5 record.
- `results/segment_mapping_audit.csv`: all 2,257 record-level joins and contradictions.
- `preflight/manual_control_sample.csv`: frozen 30-record sample.
- `results/manual_control_pdbe_api.csv`: live API cross-check.
- `protocol/LOCKED_OUTCOME_PROTOCOL_R3.md`: post-gate outcome lock.
- `provenance/http_ledger.jsonl`: live API request hashes.
