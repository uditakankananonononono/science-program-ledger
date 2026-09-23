# algo50/05 - Reference-free self-consistent codon adaptation index vs classic CAI for predicting yeast protein abundance

Status: LOCKED before any index was computed against abundance (timestamp + sha256 in results/lock.txt). Lane RES-1. Algorithm study (not counted toward the flagship 100).

## Question
The Codon Adaptation Index (CAI, Sharp & Li 1987) needs a hand-picked reference set of highly expressed genes, usually ribosomal proteins. Can a label-free iterative method that discovers its own reference set from the genome (start from all genes, re-pick the top-scoring genes as the reference, repeat until stable) predict protein abundance as well as ribosomal-reference CAI, with no prior biological knowledge? And how much does a supervised codon model trained on one abundance dataset gain on independent datasets?

## Data
- CDS: SGD S288C orf_coding.fasta.gz (sgd-archive.yeastgenome.org). Keep "Verified ORF" only, length divisible by 3, start ATG, no internal stops, >= 100 codons.
- Abundance (PaxDb, per-dataset, not the integrated set to avoid circularity): Ghaemmaghami 2003 (TAP-western), Kulak 2014 (MS), Mueller 2020 (MS). log10(ppm), genes with abundance > 0.
Retrieval time + sha256 in data/.

## Methods (all indices are computed from sequence only unless stated)
- B1 CAI-RP: Sharp-Li weights from ribosomal protein genes (standard gene names RPL*/RPS*, excluding mitochondrial MRP*).
- B2 ENC (Wright 1990), sign flipped so higher = more biased.
- B3 GC3.
- P SC-CAI (proposed, label-free): reference = all genes; iterate: compute Sharp-Li weights from the reference, score all genes, reference = top 2% by score; stop when the reference is unchanged or after 20 iterations.
- S supervised: 59 relative synonymous codon frequencies (excluding Met, Trp, stops) -> ridge regression on log-abundance, alpha by 5-fold CV, trained on Ghaemmaghami only.
Genes used to fit S are excluded from nothing else; for S, evaluate only on genes NOT in the Ghaemmaghami set, plus all genes on Kulak/Mueller with 5-fold gene-level CV fold predictions (gene held out in all training).

## Metric
Spearman rho with log-abundance per dataset; 95% CI by 2,000 gene bootstrap resamples; paired bootstrap for differences.

## Gates
- G1: SC-CAI rho >= CAI-RP rho - 0.02 on all three datasets (non-inferiority without prior knowledge).
- G2: SC-CAI reference set after convergence overlaps the ribosomal-protein set by >= 30% (it rediscovers the biology).
- G3: S beats CAI-RP by >= 0.05 rho on both Kulak and Mueller with the paired bootstrap CI excluding 0.
PASS = G1 and G2.

## Failure policy
Failures are recorded as-is. A failed direction triggers a documented pivot with new gates locked in an amendment before new results are inspected. Original gates are never re-scored.
