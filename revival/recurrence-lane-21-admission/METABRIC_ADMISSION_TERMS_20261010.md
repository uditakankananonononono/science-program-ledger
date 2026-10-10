# METABRIC source-admission policy checkpoint
October 10, 2026. Documentary-only. NOT CLEARED.

Study-specific LICENSE:
https://github.com/cBioPortal/datahub/blob/master/public/brca_metabric/LICENSE
Quote: "keep the resulting data-sets open; and offer your shared or adapted version of the data-set under the same ODbL license."

The study's LICENSE explicitly applies ODbL. The inspected study metadata and Readme supply no independently permissive exception. Exact metadata:
https://github.com/cBioPortal/datahub/blob/master/public/brca_metabric/meta_study.txt
Identifiers: brca_metabric; publications 27161491, 30867590, 22522925.

The parent's October 10 06:45:02 IST instruction requires the owner's explicit yes before accepting share-alike duties for derived public-repo datasets. No acceptance is established here. Stop at that gate; no dataset admission, payload download, derived dataset creation or release in this unit.

## Product mapping state
Committed source record docs/PREREG_SIGNATURE_PROXY_20260928.md identifies:
- data_mrna_illumina_microarray_zscores_ref_diploid_samples.txt
- SHA256 f2ec4e1badc6f3a49c5db323e90faf3cb091cd29e880f58b3163bf24d30f6b7c
The filename appears in the live study directory:
https://github.com/cBioPortal/datahub/blob/master/public/brca_metabric/data_mrna_illumina_microarray_zscores_ref_diploid_samples.txt
The recorded source URL points to mutable master. Exact historical source commit and current object/hash are not verified in this unit. Filename match alone is not byte integrity.

## Broader policy evidence
- https://docs.cbioportal.org/user-guide/faq/ : default ODbL, study-specific exceptions possible.
- https://github.com/cBioPortal/datahub : ODbL share-alike duties; separate TCGA terms.
- https://datacatalog.mskcc.org/dataset/11457 : Free to All access, not a substitute for reuse terms.

Fine-Gray hold and existing verdicts unchanged.

## Exact-object verification and alternative-route scout
Live GitHub pointer declares oid SHA256 f2ec4e1badc6f3a49c5db323e90faf3cb091cd29e880f58b3163bf24d30f6b7c and size 303120338.
Under a separately scoped verification instruction, the recorded object URL was streamed through SHA256 without storage or analysis:
https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/brca_metabric/data_mrna_illumina_microarray_zscores_ref_diploid_samples.txt
Actual digest: f2ec4e1badc6f3a49c5db323e90faf3cb091cd29e880f58b3163bf24d30f6b7c. MATCH. Historical source commit remains unidentified; master is mutable. Byte identity to the recorded source hash is verified, not its analysis or licensing acceptance.

No verified permissive route to the identical transformed matrix found in this bounded scout:
- https://ega-archive.org/datasets/EGAD00010000210 : normalized expression discovery product; access request required.
- https://ega-archive.org/datasets/EGAD00010000211 : normalized expression validation product; access request required.
- https://rdrr.io/github/bhklab/MetaGxBreast/man/METABRIC.html : points to original EGA study; no verified exact-object equivalence or independent data license found in inspected documentation.
These are possible research leads, not substitutes cleared for use. Original normalized data are not the same declared product as the cBioPortal diploid-reference z-score matrix.

Admission remains held for owner share-alike acceptance; no access request, acceptance, derived output or manuscript change.
