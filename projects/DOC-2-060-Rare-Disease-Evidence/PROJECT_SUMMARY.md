# Sculpted Project Summary - Rare Disease Evidence Triangulation Engine

## Status
The proposed 2020 retrospective predictive route is closed after three pre-outcome source rounds. No candidate ranking or outcome modeling occurred.

## Useful result
The project established that a leakage-safe 2020 rare-disease evidence triangulation study is not reconstructible from the verified public source set available here:
- R0 found cutoff-safe ClinVar historical outcomes and gnomAD v2.1.1 constraint, but no verified 2020 HPO association bundle, frozen literature index, Monarch graph or Open Targets evidence release.
- R1 proved that genuine HPO disease/gene/phenotype association history in the inspected official archive ends around older 2015-era builds, with a 2017 repository head; the ontology commit alone contains no associations.
- R2 searched official trees, legacy archives, likely repositories, Zenodo, Software Heritage, Wayback, Monarch and the public web without finding an immutable checksum/license-qualified 2020 HPO disease-association bundle.

The key result is a hard temporal-data provenance boundary. Silently substituting older HPO data would change the estimand and create leakage/misdating risk.

## What is new
This project treats historical source reconstruction itself as an experimental gate. It documents a common but underreported failure mode in retrospective biomedical AI: the nominal cutoff exists for outcomes, while a critical feature channel lacks an immutable historical snapshot.

## Why it matters
Rare-disease ranking systems are especially vulnerable to hindsight leakage because gene-disease knowledge changes rapidly. A model built with current or misdated HPO associations could appear prospectively useful while encoding future discoveries.

## Working tool/application
The useful application is a temporal-source eligibility auditor. It accepts a proposed cutoff and feature channels, then records immutable versions, checksums, licenses, association-vs-ontology distinction, earliest/latest valid dates and leakage status. It blocks model development when one required channel cannot be reconstructed.

## Top-lab reviewer questions
1. Can HPO maintainers or institutional archives supply a checksum-qualified 2020 association release?
2. Would a separately preregistered 2015-era ExAC/HPO project answer a scientifically worthwhile but different question?
3. Which biomedical benchmark claims rely on ontologies whose historical associations are not actually recoverable?
4. Can a community temporal-source registry prevent repeated leakage failures?

## Next direction
Do not reopen the 2020 route without the missing immutable association bundle. A 2015-era project must be a fresh protocol and estimand, not a continuation.
