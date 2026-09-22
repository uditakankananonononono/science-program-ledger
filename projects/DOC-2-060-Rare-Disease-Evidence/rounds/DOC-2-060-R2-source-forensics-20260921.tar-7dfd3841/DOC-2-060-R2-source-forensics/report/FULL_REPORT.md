# DOC-2-060 Dedicated HPO 2020 Source Forensics

**Date:** 21 September 2026  
**Outcome:** IMMUTABLE 2020 ANNOTATION BUNDLE NOT FOUND IN BOUNDED SEARCH

## Acceptance test
A valid artifact required exact disease-phenotype and gene-phenotype association bytes or a content-addressed commit, timestamp no later than 31 December 2020, stable IDs, checksum and license.

## Search performed
The search went beyond current docs. It queried the GitHub commits API and recursive tree for the last 2020 `human-phenotype-ontology` commit; tested likely historic annotation repository names; inspected the legacy HPO archive; searched Zenodo, Software Heritage and web results; queried Internet Archive CDX for legacy Jenkins/PURL annotation paths; and inspected Monarch archive/source documentation.

## Findings
GitHub commit `ecee89074440fbb340e00d20aa9b29c624f24a36` is dated 23 December 2020 and content-addressed, but its complete 302-file tree contains ontology/editor scripts and no disease/gene annotation bundle. It cannot satisfy the channel requirement.

The `iamkoehler/HPO-archive` repository contains genuine `diseases_to_genes_to_phenotypes`, `genes_to_phenotype`, and `phenotype_to_genes` files with stable OMIM/Orphanet partitions. Its repository head is from 2017 and observed builds are older, around 2015. It is temporally wrong for the locked 2020 estimand.

Likely former `hpo-annotation-data` repository names returned 404 through GitHub API. Software Heritage/web search did not reveal a verifiable matching origin/content object. Internet Archive CDX returned no 2020 captures for tested legacy annotation URLs. Zenodo returned HPO ontology/current or derived datasets, not an official immutable December 2020 annotation release satisfying all criteria. Monarch's observed public archive did not expose the target bundle.

## Decision
The 2020 route remains closed/parked. No candidate universe or outcomes were inspected. The absence claim is bounded: not found after this explicit search, not proof the artifact never existed.

## Next decision
Either obtain the bundle from HPO maintainers/institutional storage with checksum/license, or preregister a distinct 2015-era question using the verified legacy annotation archive and era-appropriate channels. Do not silently substitute the 2015 files into the 2020 study.
