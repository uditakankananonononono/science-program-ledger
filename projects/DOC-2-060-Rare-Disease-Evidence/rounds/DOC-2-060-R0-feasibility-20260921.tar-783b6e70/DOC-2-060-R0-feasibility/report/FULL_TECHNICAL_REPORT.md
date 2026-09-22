# DOC-2-060 R0: Rare Disease Evidence Triangulation Feasibility

**Date:** 21 September 2026  
**Status:** PRE-OUTCOME FEASIBILITY GATE FAILED

## Decision
A leakage-safe 2020 rare-disease triangulation experiment was not identifiable from three independently versioned channels during this run. ClinVar archived releases and gnomAD v2.1.1 constraint were verifiable. A 2020 HPO disease/gene annotation bundle, 2020 Monarch pathway/model-organism release, or exact historical Open Targets evidence release was not verified from the observed archives. Europe PMC publication dates are historical, but querying the current index/annotations would introduce present-day entity mapping and indexing changes unless results were frozen from a historical dump.

The protocol required at least three genuine cutoff-time channels before constructing candidates or inspecting later outcomes. R0 therefore stops before model fitting. No current HPO/Monarch/Open Targets snapshot was backdated to 2020.

## Why this matters
A compelling-looking retrospective model can leak later gene-disease annotations through phenotype profiles, ontology mappings, literature entity extraction or integrated KGs. Publication date alone does not make a current annotation index historical. Current disease aliases can map 2020 candidates using knowledge unavailable at cutoff. The same issue invalidated careless temporal ClinVar work in the prior topic.

## Channel audit
- **ClinVar outcome:** usable, with exact December 2020/2023 archives already demonstrated.
- **gnomAD constraint:** usable as a gene-level channel; v2.1.1 object reachable and versioned.
- **HPO phenotype similarity:** blocked until an exact 2020 annotation release, not only ontology term history, is frozen and licensed.
- **Europe PMC literature:** partially feasible from publication dates, but historical entity-recognition/index state is not frozen. A raw PMID query designed only from 2020 names could be defensible in a later round.
- **Monarch model organism/pathway:** observed data archive emphasizes 2024+ releases; no verified 2020 bundle in this run.
- **Open Targets:** current FTP archives and license docs exist, but an exact 2020 evidence schema/release was not verified.

## Gate result
The minimum of three independent prospective-safe channels failed: outcome plus constraint were available, while phenotype/pathway/literature channels were not yet frozen. Candidate counts, later positives, enrichment, calibration and ablations were intentionally not computed.

## Next executable route
1. Clone the HPO annotation archive at a commit dated before 2021 and verify that disease-to-phenotype and gene-to-phenotype annotation files, not only ontology terms, are present.
2. Build a literature channel by freezing a 2020 gene/disease synonym dictionary from cutoff-time resources and querying PMID publication dates without current annotation APIs.
3. Use gnomAD v2.1.1 constraint as the third channel.
4. Freeze candidate pairs absent from ClinVar December 2020, then evaluate December 2023 and current outcomes.
5. Record source licenses per row, especially integrated Monarch/Open Targets sources.

## Safety, economics and product boundary
The user is a rare-disease analyst; output would be manual-review priority only. It must not diagnose, exclude genes, or recommend treatment. Public aggregate sources avoid patient privacy data, but licenses and attribution remain. The main costs are historical data curation, ontology mapping and expert review. A product claim requires demonstrated prospective enrichment and calibration over single-channel baselines; none exists yet.
