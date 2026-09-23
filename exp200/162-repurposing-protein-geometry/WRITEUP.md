# DOC-2-062 Repurposing Through Protein Geometry - sandbox slice (exp200/162)

**Outcome: primary PASS on all locked gates. Forward validation passed its enrichment gate and FAILED its absolute-rate gate (both preserved).**

## Setup
There were no protein-language-model embeddings or structure search in the sandbox. Proxy for "functional geometry": the InterPro domain/family architecture of each target (UniProt). Sequence comparator: alignment-free 3-mer Jaccard. Data: ChEMBL phase-4 mechanisms, 448 human single-protein targets, 253 drugs with >= 2 targets, giving 391 co-target pairs vs 7,820 random target pairs.

## Primary results (locked gates)
- Among pairs with low sequence k-mer overlap (below the 75th percentile of random pairs), shared InterPro architecture separates same-drug co-targets from random pairs with AUROC 0.775 (CI 0.713-0.830, 78 positive pairs). Gates: >= 0.75, lower CI >= 0.65. Pass.
- Adding InterPro to sequence similarity lifts AUROC from 0.858 to 0.933 (+0.076, gate +0.03). Pass.
- 41% of low-overlap co-target pairs share no InterPro entry at all. These are cross-family polypharmacology, which domain architecture cannot explain.

## Forward output
results/candidate_alternative_targets.csv lists 2,057 (drug, candidate target) pairs across 464 approved drugs. Rule, set before generation: a target not annotated to the drug, InterPro Jaccard >= 0.5 to one of its annotated targets, and low k-mer overlap. Top examples: carbonic anhydrase inhibitors (methazolamide, dorzolamide, brinzolamide, topiramate, methocarbamol) -> CA12; heparins -> SERPING1 (C1-inhibitor).

## Validation V1 (locked before querying): is there measured binding in ChEMBL?
- 150 sampled candidates vs 150 same-drug controls with unrelated domain architecture. Active = any ChEMBL activity record with pChEMBL >= 6.
- Candidates 8/150 (5.3%), controls 0/150. Fisher p = 0.0035, so the enrichment gate passes. The absolute-rate gate (>= 10%) fails.
- Reading: the list is enriched for real binding, but most candidates have no potent measured activity. Many were never tested, so "no record" is not "no binding". The honest positive predictive value is at least 5% and unknown above that.

## Useful result
Domain architecture recovers drug co-targets that sequence overlap misses, and adds real information over sequence similarity (+0.08 AUROC). The generated candidate list is enriched for measured off-target binding vs architecture-mismatched controls. It is a triage list for off-target/repurposing assays, not a prediction of activity.

## Limits
- 3-mer Jaccard is a weak identity proxy. Carbonic anhydrase paralogs fall in the "low sequence" stratum, so this is not a remote-homology result.
- InterPro architecture is a sequence-derived annotation, not 3D geometry.
- ChEMBL mechanisms and activities come from the same database, though they are separate records.
- 150-pair validation sample.

## Reproduce
python3 code/fetch.py; python3 code/run.py; python3 code/forward.py; python3 code/validate.py. ChEMBL JSON (mechanisms/targets/molecules) from exp200/168 code/fetch.py.
