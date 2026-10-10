# ST1 frozen-reference recovery assessment
October 10, 2026. No execution or counts.

## Exact recovery route
`git ls-files` and path-specific `git log --all` show no tracked human_sites.tsv/human_utrs.tsv objects. data/TARGETSCAN_SOURCE.md explicitly says the TSVs are git-ignored and supplies an extraction recipe; it has no historical byte hashes for those TSVs. Exact-byte recovery cannot be certified from the inspected repository records. Newly regenerated data would be new pinned inputs, not proof of recovery.

## Frozen-universe amendment evidence
Live git log identifies results/clip_rows_136.csv's commit as 12513adb7eee02480f03f8108ea6fca9850379b1. Inspection of scripts/clip_falsify.py at that commit shows:
- `cons_genes.setdefault(s, set()).add(row["gene"])`
- `excl = cons_genes.get(seq[1:8], set())`
- `if g is None or g in excl: continue`
- `a = agg.setdefault(tid2gene[t], ...)`
- final gene-level row writing with miRNA, gene and fixed covariates.

The later committed scripts/second_clip_label_tarbase.py documents:
"Row universe and feature columns are copied VERBATIM from results/clip_rows_136.csv (the committed primary-endpoint rows). Only the label column is new".

This supports a narrowly scoped amendment that treats the frozen row universe as already filtered/mapped, with direct exact-identifier intersection and no alias expansion or recomputed exclusions. It documents intended construction and earlier reuse, not independent raw-input integrity certification. Missing historical TSV pins remain disclosed.

## Proposed manifest scope, awaiting parent review
Use results/clip_rows_136.csv as the exact frozen pair/universe/covariate reference (SHA256 5172012685ecc4767a52ccb32e24f29dfdff010f3f6408084f1329e412cbe20f), plus the pinned expression/reference files in the locked plan. Require no external alias mapping. Reject unresolved identifier rows rather than inventing mappings. Do not claim the absent raw inputs recovered.

This cannot resolve the independent comparison-opportunity or schema-semantic gates. No count execution is authorized by this assessment.

## Independent documentary comparison check
Read the linked publisher Supplementary Information (DOCX), under the parent's October 10 06:42:32 IST permission for that documentary step, with no table counts or scoring.
Observed URL: https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41598-023-49757-z/MediaObjects/41598_2023_49757_MOESM3_ESM.docx
SHA256: 7bf8b9838a629f8ba11fed023ab964e79122ff4490de83594bfd9e166202a343.
The supplement describes observed-record annotation and study analyses. It does not certify comparable observation opportunity across the frozen candidate-pair universe. No supplementary-table counts were run.
The article's explicit limitation remains decisive: "It's crucial to acknowledge that chimeric interactions are infrequent occurrences, resulting in a limited sample size for our study. As a consequence, it's entirely feasible that many of the 'control' mRNAs are actual targets of the inhibited miRNAs. Therefore, the observed trend should be interpreted as a cautious estimate of the effect."
Source: https://www.nature.com/articles/s41598-023-49757-z .
Verdict remains UNKNOWN-comparison-coverage for this replication endpoint, independent of any manifest amendment. The source is an admissible licensed table, not yet an admissible two-class replication dataset. Do not construct comparison labels or count coverage to escape this gap.
