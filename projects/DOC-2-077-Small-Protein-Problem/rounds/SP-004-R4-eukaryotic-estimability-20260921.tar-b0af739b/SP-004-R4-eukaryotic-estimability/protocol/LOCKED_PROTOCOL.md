# SP-004 Round 4 locked protocol

**Title:** Eukaryotic Common-Support Expansion with All-Pfam and Sequence Clusters
**Locked:** 2026-09-21 22:05 IST before R4 family construction or orthogonal-evidence outcome retrieval

## Goal
R3 identified family composition as the bacterial mechanism but human/mouse/yeast were non-estimable using only the first Pfam assignment. R4 attacks estimability without pooling domains.

## Populations
Checksum-frozen R2 reviewed UniProtKB records, 20-200 aa, human 9606, mouse 10090, yeast 559292. Short <=100 aa, control 101-200 aa. Original raw Pfam lists and sequences are reparsed. Domains stay separate.

## Shared-family definitions
A. **All-Pfam membership:** each protein contributes to every Pfam accession listed by UniProt. Family-specific estimates require >=5 proteins per arm; a domain requires >=10 families and >=200 unique proteins per arm across eligible families. Protein duplication across families is handled by family-cluster bootstrap and by an accession-equalized sensitivity weighting each protein by inverse eligible-family count.

B. **Sequence clusters:** MMseqs2 linclust/cluster, separately by domain, prespecified grid: minimum sequence identities 0.30, 0.50, 0.70 crossed with bidirectional coverage 0.50 and 0.80. Coverage mode requires overlap of the shorter sequence where supported. Each definition requires >=10 mixed clusters, >=5 proteins per arm per cluster, and >=200 unique proteins per arm. If MMseqs2 cannot be installed or executed, definition B is unavailable, not replaced by a hand-built approximation.

Primary family estimand is equal weight per eligible family/cluster of short-minus-control risk differences. Secondary accession-equalized and harmonic-size estimands are reported.

## Evidence outcomes
Primary: function comment, experimental GO, PDB. Third orthogonal source: proteomics-detection cross-reference, defined as any live UniProt cross-reference to PeptideAtlas, ProteomicsDB, MassIVE, or PRIDE if those return fields are supported. Individual sources remain separate and `any_proteomics` is their union. Unsupported fields are recorded and omitted, never guessed. Protein-existence tier 1 is a sensitivity proxy, not the primary orthogonal source. AlphaFold is a negative control.

## Uncertainty and gates
Two thousand family/cluster bootstrap replicates, seed 20260921. A domain-definition pair is estimable only if family and unique-protein thresholds pass and no arm contributes >50% through a single family.

A within-family deficit is supported only if family-equal RD <=-5 pp, 95% CI excludes zero, narrow 80-120 aa direction agrees, accession-equalized direction agrees, and >=70% of leave-top-family-out estimates agree.

**R4 success gate:** the same outcome deficit must be supported in >=2 of human/mouse/yeast under all-Pfam and must agree in direction in >=2 estimable MMseqs grid definitions per successful domain. For `any_proteomics`, success additionally requires >=10% outcome prevalence in at least one arm to avoid a sparse-link artifact. If MMseqs is unavailable or no grid is estimable, success is impossible; all-Pfam results remain informative but not confirmatory.

Non-estimable strata cannot be pooled. Contradictions are reported by domain and definition. No gate relaxation after outcomes.
