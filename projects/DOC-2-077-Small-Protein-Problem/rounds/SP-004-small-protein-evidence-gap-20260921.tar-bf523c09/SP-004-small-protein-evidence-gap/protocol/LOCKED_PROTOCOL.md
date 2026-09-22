# SP-004 locked protocol

**Title:** The Small Protein Evidence Gap: a protocol-first, cross-resource audit of reviewed bacterial proteins
**Topic:** DOC-2-077, "The Small Protein Problem" (inventory topic 177)
**Protocol lock:** 2026-09-21 20:31 IST, before cohort retrieval or outcome calculation
**Status at lock:** no outcomes inspected

## Decision problem
Small proteins are often hard to discover and annotate. This study asks whether that difficulty remains visible even inside the high-confidence reviewed bacterial proteome, and whether a transparent evidence triage tool can identify records most in need of structural or functional follow-up. It is an evidence audit, not a predictor of biological function.

## Population and data freeze
Primary source is the live UniProtKB REST service, reviewed bacterial entries only (taxonomy_id:2), retrieved at execution time. Case cohort: sequence length 30-100 aa inclusive. Control cohort: 101-200 aa inclusive. Entries lacking accession, sequence length, or taxonomy ID will be excluded and logged. Full raw responses, HTTP headers, retrieval UTC time, query URL, and SHA-256 will be preserved.

Independent resource validation uses RCSB PDB's live search/data APIs for structure-linked accessions. NCBI/PMC, UniProt, and RCSB are literature/documentation sources only. Ensembl is excluded because it is unreachable in this environment.

## Frozen endpoints
### Primary
1. Proportion with at least one GO term.
2. Proportion with an explicit UniProt function comment.
3. Proportion with at least one PDB cross-reference.

### Secondary
EC annotation, transmembrane feature, signal peptide, annotation score, protein-existence evidence, and an evidence-completeness score (one point each for GO, function comment, PDB, EC; range 0-4).

## Hypotheses
H1: 30-100 aa proteins have lower GO coverage than 101-200 aa controls.
H2: 30-100 aa proteins have lower explicit function-comment coverage.
H3: 30-100 aa proteins have lower PDB cross-reference coverage.

All alternatives are one-sided only for gate evaluation; two-sided estimates and confidence intervals will also be reported.

## Sampling unit and independence
The UniProt accession is the descriptive unit. Taxonomic clustering can create pseudo-replication, so confirmatory uncertainty is based on organism-cluster bootstrap and organism-level paired summaries where both length classes exist. Entry-level estimates are descriptive, not treated as independent biological replicates.

## Confounder and robustness plan
Results must be reproduced after: (a) exact matching within organism, (b) excluding names containing "ribosomal", (c) excluding names containing "hypothetical", "uncharacterized", or "putative", (d) restricting to annotation score >=4 when present, (e) length bins 30-60 and 61-100 versus control, and (f) leave-one-major-phylum-out analysis if lineage is available. Protein-family labels will be reported to expose compositional dominance. No post-hoc subgroup may replace the primary cohort.

## Statistical plan
For each binary endpoint report counts, proportions, absolute risk difference (short minus control), risk ratio with Haldane-Anscombe correction when needed, organism-cluster bootstrap 95% CI (2,000 replicates; seed 20260921), and Benjamini-Hochberg q-values across the three primary tests. Organism-paired differences are the confirmatory effect estimate. Preserve missingness as a result; never impute evidence fields.

## Locked success gate
SP-004 is a **supported evidence-gap result** only if all conditions hold:
1. All three primary short-minus-control risk differences are negative.
2. At least two primary endpoints have organism-cluster-bootstrap 95% CIs entirely below zero.
3. At least two remain negative after both exact-organism comparison and ribosomal-name exclusion.
4. No endpoint reverses by more than +2 percentage points in a leave-one-major-phylum-out analysis.
5. Raw-data and analysis integrity checks pass and RCSB validation of a deterministic audit sample shows >=95% agreement with UniProt PDB-link presence.

If any condition fails, status is **gate failure or mixed evidence**, with the same artifacts retained. Passing does not establish under-discovery in unreviewed genomes and does not make a clinical or experimental claim.

## Negative controls and falsification
- Positive control: reviewed ribosomal small proteins should often carry GO and PDB evidence; failure signals parsing/API error.
- Negative-space control: uncharacterized-name records should not be expected to have richer function comments than named proteins.
- Resource concordance: deterministic accession sample checked independently against RCSB.
- Duplicate, range, missing-field, malformed-accession, and query-cohort leakage audits.

## Outcome-blind change policy
Any protocol correction after this lock requires a dated amendment describing reason and whether outcomes were visible. Primary gates cannot be loosened. API/schema break repairs may change parsing but not cohort, endpoints, or gate.

## Translation constraint
The product concept is an evidence triage report for curators and experimental groups. It may prioritize review, not assert function. Production claims require prospective curator-time and enrichment validation.
