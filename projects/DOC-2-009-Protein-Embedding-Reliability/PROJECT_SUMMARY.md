# DOC-2-009 - Protein Embedding Reliability Map

## R0 verdict
Locked useful negative. Transparent sequence composition/dipeptide features did not predict ESM2-650M DMS reliability across held-out InterPro family components.

## Useful discovery
Coverage was strong (186 proteins, 163 annotated, 102 components), yet held-family rho was only 0.120, R2 was -0.224, MAE was 5.8% worse than the fold-mean baseline, and the protein-bootstrap rho interval crossed zero. Human, other-eukaryote and prokaryote strata were flat/negative. Virus rho 0.536 is exploratory and cannot rescue the failed locked study.

## What is new and why it matters
The project predicts a model's expected reliability on an unseen protein family rather than another mutation score. R0 establishes that cheap sequence-composition coordinates are not a reliable abstention map. This prevents a weak pooled correlation from becoming a deployment confidence score.

## Application
The R0 artifact is a family-leakage-safe reliability benchmark and OOF audit table. It can test future reliability features against a fold-mean baseline and strict InterPro connected-component holdouts. It is not a clinical or protein-engineering confidence tool.

## Top-lab/grant next question
A separate locked R1 may test pretrained embeddings plus distance-to-training-manifold features with leave-one-taxon-out and temporal external DMS validation. Grant readiness requires immutable input acquisition, a family-level uncertainty analysis, calibration/abstention utility, multiple model families and an external release. The virus signal must be independently preregistered or treated only as hypothesis generation.

## Reproducibility limitation
`run_r0.py` captures the analysis but refers to temporary input paths (`ref.csv`, `dmslevel.csv`, `uniprot_interpro.tsv`) not included in this package and lacks acquisition commands. OOF predictions and result JSON are preserved; a full rerun requires rehydrating the cited ProteinGym/UniProt inputs. This prevents calling R0 a graduated project.
