# DOC-2-060 R1: Historical Source Reconstruction

**Status:** CLEAN SOURCE-GATE FAILURE

## Result
The HPO archive lead was inspected directly. It contains genuine disease-phenotype and gene-phenotype association content, including all-source and OMIM/Orphanet partitions. However, the repository head is dated 9 March 2017 and its observed monthly annotation directories end around the older build series (97-99; revision pointer 3054, consistent with late 2015-era data). It does not provide or prove a December 2020 HPO annotation bundle.

The prespecified cutoff is 31 December 2020. Using a 2015/2017 phenotype channel would create a five-year information gap and a different estimand; using current HPO would leak later annotations. Neither substitution is allowed after lock. The three-channel source gate therefore failed before literature dictionary construction, candidate freezing or outcome inspection.

## What was verified
The archive is not ontology-only. It contains `diseases_to_genes_to_phenotypes`, `genes_to_phenotype`, and `phenotype_to_genes` files with source-specific OMIM and Orphanet variants. Thus it may support a separately preregistered 2015 cutoff experiment. It cannot silently support the 2020 design.

## Next routes
1. Reframe prospectively to a 2015 cutoff, with ClinVar 2015/2020/2023 releases and gnomAD constraint unavailable as-of-2015 handled honestly, likely requiring ExAC constraint instead.
2. Locate a 2020 HPO annotation artifact from GitHub releases, Zenodo or institutional archive with immutable checksum and license.
3. Do not proceed until the exact bundle is found.

No predictive claim, candidate list or later-label count was generated.
