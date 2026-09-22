# SP-004 Round 5: PRIDE-Native Detection Feasibility
## A locked clean stop before heterogeneous peptide evidence became a false experiment

**Date:** 21 September 2026  
**Status:** **FEASIBILITY GATE NOT ESTABLISHED - NO SCIENTIFIC OUTCOME ANALYSIS**

## Decision
The PRIDE-native design is promising but not yet outcome-ready under the locked requirements. A live API audit of 25 current project-search results per species phrase found processed candidates in all 75 projects and explicit 1% FDR language in 8 human, 10 mouse and 9 yeast project records. However, project/file metadata could not establish the remaining load-bearing conditions: unique peptide mapping to a frozen canonical proteome, comparable protein inference, verified target species, >=200 opportunity-eligible proteins per arm, and >=10 shared families with >=5 per arm. Candidate processed files totaled 35.0 GB human, 36.6 GB mouse and 40.9 GB yeast even in this bounded audit, with highly heterogeneous mzIdentML, parquet, spreadsheets, DIA matrices, search-engine outputs and archives.

The locked protocol required all conditions before outcomes. Therefore R5 stops before detection estimates. It does not claim that small proteins are or are not underdetected.

## Why metadata was insufficient
File categories such as SEARCH or RESULT show that processed output exists, but not that peptide-level q-values, decoy state, protein groups, canonical accessions and study batches are available in a common schema. Some small files were already aggregated protein matrices; others were peptide or PSM-level results; large archives hid internal schemas. Explicit "1% FDR" prose did not prove which level the threshold applied to. Species-keyword search also returned cell-line, disease, environmental and cross-species projects, so search relevance could not substitute for sample taxonomy.

The scientific design needs two independent, comparable studies per species. Picking whichever files are easiest after seeing formats would select on pipeline convenience and could bias detection. A correct next step is a separately locked harmonization round with preselected formats or repositories, not an improvised mixture.

## Audit results
| Domain | Projects audited | With processed candidate | With explicit 1% FDR prose | Meeting basic processed+FDR screen | Candidate processed volume |
|---|---:|---:|---:|---:|---:|
| Human | 25 | 25 | 8 | 8 | 35.0 GB |
| Mouse | 25 | 25 | 10 | 10 | 36.6 GB |
| Yeast | 25 | 25 | 9 | 9 | 40.9 GB |

"Meeting basic" is not feasibility-gate passage. It only means a downloadable processed candidate and explicit FDR wording were found. The locked six-part gate also demanded peptide/protein schema and sufficient biological support, which metadata cannot certify.

## Examples of heterogeneity
Human candidates included mzIdentML files around 20-54 MB, 108 MB parquet results, multi-gigabyte output archives, DIA protein-group matrices, Excel workbooks and plain TSVs. Mouse and yeast projects similarly mixed TMT tables, DIA matrices, search archives and large processed bundles. Candidate totals were dominated by a few very large submissions, while small files often lacked peptide-level detail.

## Preserved design for a future round
- Freeze two or more studies per species before download, selected by explicit sample taxonomy, whole-proteome intent, processed open format and peptide-level q-values.
- Pin a canonical reference proteome including reviewed and unreviewed entries.
- Enforce <=1% peptide FDR and >=2 unique peptides for primary detection.
- Recompute peptide uniqueness against the same proteome, not submitter protein groups alone.
- Model theoretical tryptic opportunity, TM/signal, study/batch, family/cluster, reviewed status and annotation age.
- Report studies separately before random-effects synthesis.

## What this round contributes
R5 provides a live, reproducible inventory of 75 projects and all their file metadata, a quantified processed-data burden, explicit feasibility criteria, and a reasoned stop boundary. It prevents a plausible but invalid shortcut: treating heterogeneous protein matrices as if they represented the same peptide evidence process.

## Limits
The audit is a bounded sample of the first 25 current results per species phrase, not the entire PRIDE archive. Keyword search is not a species ontology query. No processed candidate bytes were downloaded, so internal schemas were not inspected. These limits are exactly why no outcome was estimated.
