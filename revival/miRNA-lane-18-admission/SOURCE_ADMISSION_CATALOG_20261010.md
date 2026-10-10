# Lane 18 catalog admission audit
Checked October 10, 2026. Catalog designation only, not dataset admission for analysis.

## Catalog accession
GSE221572 is the candidate catalog accession. Live GEO identifies it as a three-sample record. GSE221573 is the companion expression-data record.

Sources:
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE221572
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE221573

## Preserved source discrepancy
The HybriDetector README states, verbatim:
"AGO2-CLASH data used in the publication are deposited in GEO with accession number [GSE221573](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE221573)."

Observed README: https://github.com/ML-Bioinfo-CEITEC/HybriDetector/
The README accession assignment disagrees with the live GEO dataset types. This is retained as a source-documentation discrepancy; it is not silently corrected in the original source.

## Registry crosswalk
| Catalog accession | Project | Study | Registry runs |
|---|---|---|---|
| GSE221572 | PRJNA915020 | SRP414454 | 3 |
| GSE232686 (reserve) | PRJNA973584 | SRP438190 | 13 |

Observed NCBI registry URLs:
- https://www.ncbi.nlm.nih.gov/Traces/study/?acc=PRJNA915020&o=acc_s%3Aa
- https://www.ncbi.nlm.nih.gov/Traces/study/?acc=PRJNA973584&o=acc_s%3Aa

Neither accession, parent-series identifier (GSE221574 / GSE232687), publication identifier (38129478 / 38412296), nor mapped SRP identifier matches the recorded ENCORI reference in results/encori_ago_study_list.json. Verdict: negative identifier-overlap against the recorded ENCORI reference, not exhaustive.
Reference recount: 361 rows, 37 distinct GSE and 11 distinct SRP identifiers, 41 numeric publication IDs and one placeholder ('-').

## Open admission checks
1. Payload-specific reuse terms. Article licenses and repository code licenses are not automatically dataset licenses. GEO states that submitter rights can remain.
2. Sufficiency. No candidate payload inspected; no breadth or usable-label count claimed. Requires a new dated protocol before counts or outcomes.

No payload download, label construction, model evaluation or manuscript change in this audit.

## Reuse review checkpoint
Publisher page: https://www.nature.com/articles/s41598-023-49757-z
Data availability, verbatim: "All data and code from this study are freely available at https://github.com/ML-Bioinfo-CEITEC/HybriDetector/."
Rights statement excerpt, verbatim: "This article is licensed under a Creative Commons Attribution 4.0 International License".
The full rights paragraph requires attribution, a license link and change notice; separately credited third-party material can be excluded. Article-material permission is not automatically a GEO-payload license.
The publication identifies Supplementary Table ST1 as its complete candidate table. Supplement metadata/credits are a possible admission route to inspect next; no supplement has been downloaded or admitted here.
GEO policy https://ncbi.nlm.nih.gov/geo/info/disclaimer.html preserves possible submitter rights. No separate dataset-license statement was found in the inspected catalog text. GEO-payload license remains unverified.

## Publisher supplement-listing review
Observed article page lists "Supplementary Information" and "Supplementary Table 1. (download XLSX )".
Observed file link (not opened or downloaded):
https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41598-023-49757-z/MediaObjects/41598_2023_49757_MOESM1_ESM.xlsx

Rights text, verbatim: "The images or other third party material in this article are included in the article's Creative Commons licence, unless indicated otherwise in a credit line to the material."
No separate exclusion or credit line appears in the supplement listing itself. In-file workbook credit lines remain unverified because this unit was documentary-only, with no table download. Admissibility is therefore conditional, not certified. Next necessary check is a bounded license/credit/header inspection with explicit download scope from the parent; no scoring or outcome analysis.

## Bounded ST1 inspection
Downloaded only the above publisher ST1 link under the parent's October 10, 06:40:01 IST scoped instruction: license/credit/header inspection, no scoring or content analysis.
Bytes: 8,855,617. SHA256: 87a59fa0e70b55e5dcf75d9f225f91bc6fe099a342e2bb177118003db4d92830.
Sheet names: 'Chimeras CLASH', 'High Confidence'. Both first rows contain structured headers including ID, gene annotation, category, family, replicate and confidence fields.
No license/restriction/third-party-credit text found in workbook shared strings or other XML text; no comments, embedded images or objects found. Core metadata has lastModifiedBy 'Panagiotis Alexiou'; it is file metadata, not an authority grant.
The standard Office text reader refused extraction because shared-string storage exceeded its limit. Bounded ZIP/XML inspection checked the requested metadata and restriction text without model scoring, sequence handling or data-value analysis. No visual/layout claim is made.
ST1 is recorded as the admissible publisher CC BY 4.0 route with attribution, license-link and change-notice duties retained. This does not license the GEO archive or certify sufficiency. Stop before sufficiency until a fresh locked plan is approved.
