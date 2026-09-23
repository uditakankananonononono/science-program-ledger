# DOC-2-062 Repurposing Through Protein Geometry - locked gates (22:48 IST, before domain/sequence data download)

## Sandbox-fit slice
No PLM embeddings or structure search available. Functional-geometry proxy: InterPro domain/family architecture of targets (UniProt REST xref_interpro). Sequence-similarity comparator: 3-mer Jaccard of full sequences (alignment-free proxy of sequence identity).

## Question
For approved drugs hitting >= 2 human single-protein targets (ChEMBL phase-4 mechanisms), are co-targets of the same drug recognisable by shared InterPro architecture when sequence similarity is LOW - i.e. does functional-domain context find alternative targets that sequence misses?

## Protocol
Positives: unordered pairs of single-protein targets co-annotated to the same drug. Negatives: 20 random target pairs per positive drawn from all single-protein phase-4 targets, excluding any co-targeted pair.
"Low sequence similarity" stratum = 3-mer Jaccard below the 75th percentile of NEGATIVE pairs.
Score = Jaccard of InterPro entry sets.
## Gates
G1 In the low-sequence-similarity stratum, InterPro-Jaccard AUROC (pos vs neg) >= 0.75.
G2 Gene-level: >= 30 positive pairs in that stratum; AUROC 95% bootstrap CI (1000, pair resampling) lower bound >= 0.65.
G3 Adding InterPro to 3-mer similarity (logistic, 5-fold CV, all pairs) improves AUROC by >= 0.03.
Failure policy: negative preserved; pivots appended with new locked gates.

## Result (22:47) - PASS on locked gates
Low-sequence stratum AUROC 0.775 (CI 0.713-0.830), 78 positive pairs; InterPro adds +0.076 AUROC over 3-mer similarity. Major caveat, fixed before the forward list: 3-mer Jaccard is a weak identity proxy (carbonic anhydrase paralogs sit below the cut), so "low sequence similarity" means low k-mer overlap, not a remote-homology regime.
Forward output (descriptive, not gated, rule set here before generation): for each multi-target or single-target drug, candidate off-/alternative targets = phase-4 target proteins not annotated to that drug with InterPro Jaccard >= 0.5 to any of its annotated targets AND 3-mer Jaccard below the stratum cut. Ranked by InterPro Jaccard.

## Validation V1 (locked 22:49, before any activity query): do candidate alternative targets show measured binding in ChEMBL?
Sample 150 candidate (drug, target) pairs from results/candidate_alternative_targets.csv (seed 0) and 150 control pairs: same drugs, random phase-4 target proteins with InterPro Jaccard < 0.1 to all annotated targets. A pair is "active" if ChEMBL /activity has any record for (parent molecule, target) with pchembl_value >= 6.
V1-G1 active fraction(candidates) >= 3x active fraction(controls) with Fisher p < 0.01.
V1-G2 active fraction(candidates) >= 0.10.
Caveat: ChEMBL activity data and ChEMBL mechanism annotations share a source database but are separate records; mechanism rows are not activity rows.

## Validation V1 result (22:56): V1-G1 PASS (8/150 = 5.3% vs 0/150 controls, Fisher p = 0.0035); V1-G2 FAIL (5.3% < 10%). Preserved as a partial validation.
