# DOC-1-008 — A Virtual Yeast Cell for Metabolic Engineering
# GATES locked 2026-09-24 ~02:26 IST, BEFORE model download outcomes.

## Question
Can a genome-scale virtual yeast cell (Yeast8, constraint-based FBA) (a) reproduce
experimental gene-essentiality on a FROZEN external dataset, beating the named
published baseline model iMM904, and (b) propose a concrete, literature-checked
metabolic-engineering knockout design for succinate overproduction?

## Data (public; URLs + SHA-256 in provenance)
- MODEL: Yeast8 (SysBioChalmers/yeast-GEM, model/yeast-GEM.xml, SBML).
- BASELINE MODEL: iMM904 (BiGG, named published predecessor).
- FROZEN EXPERIMENTAL TRUTH: SGD phenotype_data.tab (yeastgenome.org) - deletion
  "null" alleles with viability phenotypes; per-gene collapse: gene = inviable if any
  null allele annotated "viability: inviable", else viable if annotated "viable".
  Genes lacking either annotation are excluded from scoring.
- Cross-check list: yeast-GEM data/essentialGenes (inviable_orfs.txt, verified_orfs.txt).

## Method (frozen)
- cobrapy + GLPK, model default medium as shipped (aerobic minimal glucose);
  if the shipped model lacks a succinate exchange reaction, ADD a boundary exchange
  for extracellular succinate and document it as the only model edit.
- Essentiality: single-gene deletion, growth < 1% of wild-type => predicted essential.
- Metric: balanced accuracy on the intersect of model genes and SGD-scored genes.

## Gates
- G1 (frozen external validation): Yeast8 balanced accuracy >= 0.85 on SGD truth AND
  Yeast8 BA >= iMM904 BA on the same gene set (beat-or-document loss honestly).
- G2 (engineering prediction): greedy single-knockout scan for succinate:
  at least ONE non-essential single knockout with predicted succinate export >= 5% of
  the model's theoretical maximum at biomass >= 10% of wild-type. Then MECHANISM
  CHECK: top-3 designs compared against published yeast succinate-engineering
  literature (e.g., SDH-complex deletions); agreement or documented discrepancy.
- Tool + nomination: yeast_cell.py CLI (gene knockouts -> growth + succinate flux,
  smoke-tested vs known WT) + top design nominated for wet-lab validation (if G2 passes).
- Failure: G1 fails -> documented boundary (virtual cell does not validate);
  G2 fails while G1 passes -> "validates but yields no design" finding, no relaxation.

## Compute honesty
Yeast8 ~4k reactions, ~1.1k genes: single-deletion scan = ~1.1k FBA solves (GLPK,
seconds). iMM904 same. Fully feasible in-environment.
