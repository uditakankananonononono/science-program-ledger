# LOCKED: ST1 sufficiency review
October 10, 2026, 06:42 IST. Supersedes the draft only for this review; no counts or scoring performed before lock.

Parent review rulings incorporated: High Confidence sheet only; all binding semantics certified from the paper's own text before counting; documentary Methods comparison-opportunity gate; exact frozen-reference pins; UNKNOWN stop on missing/unpinned inputs; coverage audit and report only, then stop.

## Input pins
| Input | SHA256 |
|---|---|
| Publisher ST1, /downloads/ST1_publisher_20261010.xlsx | 87a59fa0e70b55e5dcf75d9f225f91bc6fe099a342e2bb177118003db4d92830 |
| results/clip_rows_136.csv | 5172012685ecc4767a52ccb32e24f29dfdff010f3f6408084f1329e412cbe20f |
| results/hpa_hek293_ntpm.tsv | 03197d92b47ad1529acaf2ee3e46c377baa14d40f770180c520ddc4efa67df18 |
| results/encori_ago_study_list.json | 09b04cd33f0cd4eb7697c82cc81e6fae84387a8f126e81ac3c1596b7dcbc9f0a |
| data/human_sites.tsv (conserved-site exclusion reference) | MISSING, no pin possible |
| data/human_utrs.tsv (frozen gene/UTR reference) | MISSING, no pin possible |

Missing rows are explicitly blockers, not a fully populated manifest. Stop UNKNOWN-input-reference before counting unless source-grounded evidence shows the frozen row universe already embodies every required exclusion and mapping, followed by a separately reviewed manifest amendment. Do not download or reconstruct absent references in this unit.

## Ordered gates
1. Recheck ST1 hash and all present reference hashes. Any mismatch stops UNKNOWN-input-reference. Missing required reference stops the same way.
2. Review licensed article Methods for comparable capture/detection opportunity across frozen-universe pairs; quote evidence. Do not treat deposited non-observation as a biological negative. If the Methods cannot establish comparable opportunity, UNKNOWN-comparison-coverage regardless of potential totals.
3. Certify each used column binding from the paper's own text: exact entity identity, gene identity/category, confidence and ambiguity flags, record identity, replicate metadata and study scope. Unexplained encoding or semantics stops UNKNOWN-schema. Sequence-valued fields are excluded from this review.
4. Only if gates 1-3 pass: High Confidence sheet only; human miRNA/protein-coding-gene records only; exclude ambiguity and unresolved mappings; exact frozen-reference mapping only, no guessed aliasing or family expansion. Deduplicate exact entity/gene pairs; intersect frozen universe; preserve original conserved-site exclusions and covariate availability; record exclusion reasons.
5. Unchanged coverage rule: >=50 exact miRNAs each with >=50 unique supported and >=50 'not observed in this deposited support set' comparison pairs. The latter designation is permitted only after gate 2. Minimum 5,000 evaluable unique pairs is derived from this rule, not a new gate.

## Verdicts and scope
SUFFICIENT-FOR-DESIGN only if every gate passes. INSUFFICIENT-COVERAGE only if semantics/references/opportunity are resolved but numeric rule fails. Otherwise retain UNKNOWN-input-reference, UNKNOWN-comparison-coverage, UNKNOWN-schema, UNKNOWN-mapping or UNKNOWN-provenance as appropriate. New overlapping/rights-conflicting evidence stops INELIGIBLE-overlap/rights.
One JSON audit and short report only. No scoring, outcome analysis, pooling, alternate downloads, fallback, retraining or manuscript changes. Stop after report. Full proposed exclusions and design context remain in DRAFT_ST1_SUFFICIENCY_REVIEW_20261010.md; this lock tightens its order of operations and stop gates rather than relaxing anything.
