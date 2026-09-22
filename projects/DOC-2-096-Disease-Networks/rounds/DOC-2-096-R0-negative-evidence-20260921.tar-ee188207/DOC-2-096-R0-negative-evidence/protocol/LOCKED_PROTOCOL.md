# DOC-2-096 R0 locked protocol

**Title:** Disease Networks from Bounded Negative Evidence in ClinVar
**Locked:** 2026-09-21 22:22 IST before ClinVar outcome download

## Scientific premise
ClinVar benign/likely-benign classifications are variant-condition assertions, not proof that a gene has no role in a disease. R0 tests a narrower network claim: gene-condition edges supported only by pathogenic assertions differ topologically from edges whose submitted variants include both pathogenic and benign evidence, and contradiction burden identifies unstable evidence neighborhoods.

## Data
Live NCBI ClinVar `variant_summary.txt.gz` and `submission_summary.txt.gz`, frozen with retrieval UTC, headers and SHA-256. Human GRCh38 records only when assembly filtering applies. Conditions require a MedGen/OMIM/Orphanet identifier when available; names without stable identifiers are retained only in sensitivity. Genes must have a non-placeholder symbol.

## Edge evidence
For each gene-condition edge, count distinct variants classified pathogenic/likely pathogenic (P), benign/likely benign (B), uncertain significance (VUS), and conflicting. A variant contributes to a class by normalized aggregate clinical significance. Primary positive edge: P>=2. Bounded negative burden: B/(P+B), defined only where P+B>0. Contradictory edge: P>=1 and B>=1, or any conflicting-class variant.

Benign burden never deletes a positive edge and is never called gene-disease refutation. It is an evidence-context attribute.

## Networks and endpoints
Positive gene-condition bipartite graph and disease projection weighted by shared P-supported genes. Primary endpoints: edge contradiction prevalence; degree/centrality difference for high versus low benign burden; change in disease projection under reliability weight P/(P+B+conflicting+1); enrichment of future/recently modified or low-review edges among high contradiction burden where dates/review status permit.

## Bias controls
Stratify by review status, assertion count, gene degree, condition degree, submission recency, molecular consequence when available, and disease identifier source. Preserve missing identifiers. Negative controls: synonymous benign burden and accession/identifier-prefix associations. Sensitivity thresholds P>=1/2/5, excluding no-criteria assertions, excluding cancer predisposition, and disease-name versus stable-ID mapping.

## Locked gate
Supported result requires: (1) >=10,000 stable-ID gene-condition edges and >=1,000 contradictory edges; (2) contradiction/benign burden remains associated with at least one prespecified instability endpoint after exact strata or regression adjustment; (3) direction replicates in two disease-ID source strata or two review-status strata; (4) network reliability weighting changes at least 5% of top-decile disease neighbors while preserving >=80% of high-review neighbors; and (5) negative controls do not show equal or larger effects.

If submission-level clinical-significance linkage cannot be reconstructed from the two public tables, the project stops at an evidence-resolution feasibility result rather than treating aggregate labels as independent submissions.
