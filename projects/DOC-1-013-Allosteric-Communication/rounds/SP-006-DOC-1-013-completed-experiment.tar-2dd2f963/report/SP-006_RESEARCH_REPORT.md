# SP-006: Protein-language embeddings enrich known allosteric-pocket residues

**Inventory:** DOC-1-013  
**Experiment date:** 21 September 2026  
**Status:** Completed retrospective open-data benchmark

## Abstract
We tested whether residue embeddings from a small pretrained protein language model identify residues lining experimentally solved allosteric ligand pockets. The cohort was selected from a live RCSB PDB search under a protocol frozen before outcome retrieval and modeling. Fifteen structures passed fixed structural and provenance gates, contributing 7,633 resolved residues and 204 positive pocket residues. In leave-one-PDB-entry-out testing, ESM-2 embeddings produced mean per-structure average precision (AUPRC) 0.1406 versus 0.0394 for amino-acid one-hot features, a paired gain of 0.1012 (protein-entry bootstrap 95% CI 0.0636-0.1397). The predeclared success rule was met. A within-protein shuffled-embedding ablation fell to 0.0469, and a random-label control returned 0.0387, close to the mean positive prevalence of 0.0295. The finding is enrichment, not causal pathway reconstruction. The benchmark contains repeated structures of the same protein family, so entry-level confidence intervals are optimistic for family-level generalization.

## Research question and locked decision rule
The exact protocol and its SHA-256 are in `protocol/LOCKED_PROTOCOL.md` and `protocol/LOCKED_PROTOCOL.sha256`. The primary gate required ESM-2 macro AUPRC to exceed the one-hot baseline by at least 0.05 and the paired structure-bootstrap 95% interval to exclude zero. No endpoint, threshold, feature, or model rule was changed after results were observed.

## Real-data sources and provenance
Biological records came from live RCSB PDB Search, Data, and coordinate endpoints. UniProt accessions mapped by RCSB were each retrieved from the live UniProt REST API. `provenance/http_ledger.jsonl` records timestamp, URL, status, byte count, and SHA-256 for every request. Raw server responses and mmCIF coordinate files are included. The representation model was the published `facebook/esm2_t6_8M_UR50D` checkpoint, used frozen without fine-tuning. `provenance/model_artifact.json` identifies the model and hashes the resulting embedding matrix.

## Cohort construction
The locked RCSB query returned 100 candidates. We inspected candidates in a fixed order until 15 passed. Twenty-four entries were screened. Nine were rejected, including three titles that did not actually describe an allosteric structure and six with no ligand satisfying the fixed ligand/proximity gate. Rejections are retained in `results/screening_log.csv`.

For each accepted structure, the longest protein chain between 60 and 1,200 resolved standard residues was used. A ligand had to have at least six heavy atoms and at least three neighboring protein residues. Standard additives, water, ions, and common native cofactors were excluded. A residue was positive if any heavy atom lay within 5.0 Å of any selected-ligand heavy atom. Across structures, positive prevalence averaged 2.95%.

## Analysis
The primary feature was the final-layer 320-dimensional per-residue ESM-2 embedding. Baselines were amino-acid one-hot encoding and one-hot plus seven prespecified physicochemical features. Evaluation used leave-one-PDB-entry-out cross-validation. Standardization, PCA for ESM (maximum 32 components), and logistic-regression regularization selection occurred only within training data. Metrics were computed separately for each held-out structure and macro-averaged.

| Model | Mean AUPRC | Mean AUROC | Mean recall in top 10% |
|---|---:|---:|---:|
| ESM-2 | 0.1406 | 0.7394 | 0.3291 |
| ESM-2, positions shuffled within structure | 0.0469 | 0.5427 | 0.1531 |
| Amino-acid one-hot | 0.0394 | 0.5367 | 0.1116 |
| One-hot + physicochemical | 0.0393 | 0.5368 | 0.1116 |
| ESM-2 with labels shuffled within structure | 0.0387 | 0.4908 | 0.1100 |

The ESM-2 minus one-hot AUPRC difference was 0.1012. Its paired entry-bootstrap 95% interval was 0.0636 to 0.1397 (10,000 resamples, seed 13013). The locked success criterion was met. The random-label AUPRC was within 0.05 of prevalence, so the locked leakage sanity gate passed.

## Interpretation
ESM-2 embeddings concentrated known ligand-contact residues nearer the top of residue rankings than residue identity alone. The sharp decline after shuffling embeddings within each structure supports the role of sequence context encoded by the model rather than simple amino-acid composition. The absolute AUPRC of 0.1406 remains modest: this is useful enrichment over a 2.95% prevalence, not a complete pocket detector.

## Negative and limiting evidence
- The one-hot and physicochemical baselines performed only slightly above prevalence.
- Shuffled embeddings lost most of the signal.
- Several structurally plausible candidate entries failed the ligand gate and were not silently dropped.
- The cohort is not family-independent. Seven accepted entries are closely related ribonucleotide-reductase structures, and two are TEM-1 beta-lactamase structures. Leave-one-entry-out folds can therefore place close homologs in training and test sets. The confidence interval quantifies entry variation, not unseen-family variation.
- Ligand assignment used a deterministic largest-eligible-pocket rule after title filtering; it was not manually validated against specialist allostery databases.
- A ligand-contact pocket is not the same thing as a full allosteric communication pathway. No causal residues, dynamic coupling, or prospective activity were tested.
- The title search is a convenience sample of solved structures and is biased toward historically well-studied proteins.

## Conclusion
The experiment passed its predeclared gate: frozen ESM-2 residue embeddings enriched experimentally solved allosteric-pocket contacts beyond amino-acid baselines in this RCSB benchmark. The correct claim is narrow. It supports contextual sequence representations as a triage signal for known pocket residues, while family-independent performance and causal allosteric pathways remain untested.

## Reproduction map
1. `scripts/search_rcsb.py` performs the frozen live candidate query.
2. `scripts/build_cohort.py` retrieves coordinates, applies gates, logs rejections, and creates labels.
3. `scripts/fetch_uniprot.py` retrieves live UniProt records.
4. `scripts/embed.py` computes frozen ESM-2 embeddings.
5. `scripts/analyze.py` runs locked cross-validation, controls, bootstrap inference, and writes results.

All raw inputs, processed labels, model-derived embeddings, exact metrics, source ledger, and scripts are bundled. No simulated observations or fabricated citations are used.
