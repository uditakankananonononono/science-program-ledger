# EXP200-108 (DOC-2-008) Variant Effects Without a Family Tree - 1-page writeup
Outcome: R1 FAIL (preserved) -> R2 pivot SUCCESS on a disjoint gene set.

## Question
Can a sequence-only protein language model (no allele frequency, no pedigree, no MSA) call pathogenic vs benign
missense variants, and where does it fail?

## Data
ClinVar variant_summary (NCBI, 2026-09-23), missense SNVs on GRCh38 with >=2-star review, P/LP vs B/LB; reference residue
checked against UniProt canonical (58,854/62,817 matched). Checksums in data/SOURCES.tsv. Model: ESM-2 t6_8M, zero-shot.

## R1 (gates locked in GATES.md)
150 random genes, 2,278 variants. Pooled AUROC 0.635 (CI 0.58-0.70) -> G1 FAIL. BLOSUM62 0.667 -> G2 FAIL (ESM not better).
Median within-gene AUROC 0.71 (22 genes) -> G3 pass. No label-era drift (0.634 post-2024 vs 0.635 earlier) -> G4 pass.
Honest reading: a small sequence-only model is not a usable universal missense caller; it is no better than a 1992 substitution matrix.
Failure pattern: AUROC 0.80 at sites where the model's own predictive entropy is low, ~0.60 elsewhere.

## R2 pivot (GATES_R2.md locked before scoring)
Hypothesis: the model's label-free site entropy tells you where it can be trusted. Threshold fixed from R1 (entropy <= 0.907),
tested on 150 NEW genes (disjoint from R1), 2,197 variants.
- Confident sites: 31.5% coverage, AUROC 0.793 (gene-bootstrap CI 0.735-0.856) -> H1 PASS.
- vs BLOSUM62 at the same sites 0.633: +0.16 (CI +0.11 to +0.21) -> H2 PASS.
- Non-confident sites: AUROC 0.564 (near chance).

## Finding
Sequence-only variant calling fails as a blanket method, but a tiny 8M-parameter model carries a free, label-independent
reliability signal: its own per-site entropy splits variants into a ~30% subset it calls well (AUROC ~0.79, beats BLOSUM by 0.16)
and a ~70% subset where it should abstain. The useful tool is a self-auditing caller that reports "call" or "abstain" per variant.

## Limits
One small model (35M/650M not tested at this budget); ClinVar label bias toward well-studied genes; pooled AUROC mixes genes;
confident-site subset is enriched for pathogenic (82%), so base rates differ; not a clinical tool.

## Reproduce
python3 code/01_filter.py; 02_select.py; 03_score.py; 04_eval.py (R1); 02b_select_R2.py; 03b_score_R2.py; 05_eval_R2.py (R2).
