# DOC-2-089 One Function, Many Microbes - sandbox slice (exp200/189)

**Outcome: primary FAILED on its convergence gate (preserved); Pivot 1 (lineage lock, corrected for sparsity) PASSED 4/5. Novelty is low - see below.**

## Setup
KEGG complete-module calls for 150 prokaryotic genomes (one per genus, 25 phyla), covering 5 functions that have alternative KEGG routes: lysine (DAP variants vs AAA), isoprenoid precursors (MEP vs MVA), glycolytic backbone (EMP vs ED), heme (protoporphyrin vs coproporphyrin-dependent vs siroheme), menaquinone (classical vs futalosine). The organism-list endpoint was down, so the sampling amendments are recorded in GATES.md before any data.

## Results
- **Primary:** route choice tracks phylum strongly (raw V 0.58-1.00, p <= 0.007 in 5/5). But "many solutions within one lineage" appeared in only 2/5 functions: lysine and EMP/ED. The gate needed 3, so it fails. Raw V is inflated by sparse phyla.
- **Pivot 1:** restricted to the 6 phyla with >= 5 genomes and using bias-corrected V: heme 0.77, isoprenoid 0.69, lysine 0.46, glycolysis 0.45, all p = 0.001. Menaquinone had too few genomes and counts as a fail.
- Modal routes: heme uses the coproporphyrin-dependent route in Actinomycetota and Bacillota vs the classical route in Pseudomonadota and Bacteroidota. Isoprenoid uses MEP in bacteria vs MVA in Methanobacteriota. Lysine uses succinyl-DAP in Pseudomonadota and Actinomycetota vs DAP-aminotransferase in Bacteroidota and methanogens.

## Useful result
Across these five core functions, *which* alternative route a microbe uses is mostly a lineage property (corrected V 0.45-0.77). Real within-lineage "convergent alternatives" are the exception, found only for lysine and glycolysis. For metagenome function inference, that means route-level calls for heme, isoprenoid and lysine carry taxonomic information and should not be treated as independent functional evidence. Genuine alternative-solution diversity is concentrated in lysine and central glycolysis.

## Novelty (honest)
The lineage split for heme (coproporphyrin-dependent route in Gram-positives) and isoprenoid (MVA in archaea) is known biology. This is a quantified, reproducible confirmation on a random genus-level sample, not a discovery. The within-lineage lysine and EMP/ED mixing is the part worth following up.

## Limits
- n = 150 genomes.
- KEGG module completeness calls can miss divergent genes.
- Route combinations with fewer than 5 genomes are pooled as "other".
- Phylum-level only, with no deeper phylogenetic control.

## Reproduce
python3 code/fetch.py; python3 code/run.py; python3 code/pivot1.py
