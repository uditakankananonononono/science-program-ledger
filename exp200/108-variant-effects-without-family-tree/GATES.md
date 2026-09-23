# EXP200-108 / DOC-2-008 - Variant Effects Without a Family Tree
Locked: 2026-09-23 21:48 IST, before any variant scores were computed or labels inspected.

## Question
Can a sequence-only protein language model (no population frequency, no pedigree, no conservation MSA)
separate pathogenic from benign missense variants in ClinVar, and where does it fail?

## Data (free, public)
- ClinVar variant_summary.txt.gz (NCBI FTP, current release; sha256 recorded in data/SOURCES.tsv)
- UniProtKB/Swiss-Prot canonical human sequences (rest.uniprot.org), sha256 recorded
Inclusion: single-nucleotide missense (protein change p.Xaa###Yaa), GRCh38, review status >= 2 stars
(criteria provided, multiple submitters, no conflicts / expert panel / practice guideline),
clinical significance Pathogenic or Likely pathogenic (label 1) vs Benign or Likely benign (label 0).
Reference residue must match the UniProt canonical sequence at that position (else variant dropped, count reported).
Proteins length <= 1022 aa (model window). Genes with >= 1 P/LP and >= 1 B/LB variant.
Compute cap: up to 150 genes, sampled with fixed seed 20260923 from eligible genes, stratified to keep balance.

## Scores (zero-shot, no training on labels)
- S_esm: ESM-2 t6_8M wild-type-marginal log-ratio log p(mut) - log p(wt) (single forward pass per protein).
- Baselines: BLOSUM62 substitution score; Grantham distance.

## Primary gates (all must pass for SUCCESS)
G1  Pooled AUROC(S_esm) >= 0.75 on the evaluation set (95% bootstrap CI lower bound >= 0.70, 1000 gene-level bootstrap resamples).
G2  S_esm beats BLOSUM62 by >= 0.05 pooled AUROC, with gene-level bootstrap CI of the difference excluding 0.
G3  Per-gene: median within-gene AUROC >= 0.70 across genes with >= 5 variants of each class.
G4  Temporal holdout: AUROC on variants whose ClinVar LastEvaluated date is >= 2024-01-01 is within 0.05 of AUROC on earlier variants
    (the model is zero-shot so this tests label-era drift, not leakage).

## Failure characterization (reported regardless of outcome)
Stratify AUROC by: protein length, residue position relative disorder proxy (ESM entropy at site), gene constraint class
not used (sequence-only regime), amino-acid class of substitution. Identify where sequence-only reasoning fails.

## Failure policy
Negative is preserved as-is. If a gate fails, the project pivots per program rule: new direction written as
GATES_R2.md and locked before any new result is computed. No threshold changes, no re-sampling of genes to rescue G1-G4.
