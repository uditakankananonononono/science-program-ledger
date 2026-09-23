---
id: P15-02
title: "Phage Arsenal: Mining Annotated Phage Genomes for Anti-AMR Lysins and Depolymerases"
parent: "CBIO045 - Viral Genome Annotation with RNNs (source abstract, 2024)"
---

# Phage Arsenal

**Parent project:** CBIO045 ViGAR (fast genome annotation enabling drug-therapy research).

## Premise
Annotation is the bottleneck between the world's phage collections and the antibiotic-resistance crisis. Therapeutically valuable phage proteins - endolysins that lyse bacterial cell walls and depolymerases that strip capsules - sit annotated as "hypothetical protein" across public phage databases. This project re-annotates public phage genomes (INPHARED, PhagesDB) with structure-aware function prediction, ranks candidates against priority AMR pathogens (Klebsiella, E. coli, Acinetobacter), and validates in silico by structure comparison to known lysins. The deliverable is a ranked, open candidate list any phage-therapy lab can pick up and test.

## Data sources
- INPHARED (public): curated phage genome database.
- PhagesDB (public): actinobacteriophage genomes.
- AlphaFold DB: predicted structures for candidate ranking.
- PDB: known lysin/depolymerase structures for Foldseek-style comparison.

## Method outline
1. Re-annotate all public phage genomes with the annotation stack + domain-level pLM embeddings.
2. Build lysin/depolymerase classifiers from known examples (curated positives from the literature).
3. Rank candidates by classifier score + structural similarity to known enzymes.
4. Map candidate host ranges via phage-host labels; prioritize hits against ESKAPE pathogens.
5. Publish the ranked atlas with per-candidate evidence pages.

## Success gates (locked before results)
- G1: classifier recovers >= 90% of held-out known lysins at precision >= 0.8.
- G2: atlas covers >= 90% of INPHARED genomes.
- G3: >= 50 high-confidence novel candidates against ESKAPE hosts, none identical to known enzymes (novelty check via clustering).
- G4: structural plausibility: >= 70% of top-100 candidates have confident structure matches to enzyme folds (pLDDT/ Foldseek thresholds locked).

## Expected deliverable
The open Phage Arsenal candidate atlas with evidence pages, the re-annotation pipeline, and the classifier + structure-validation stack as a reusable tool.

## Failure/pivot rule
If structural validation mostly fails (candidates don't fold like enzymes), pivot to the negative-control study: why sequence-level lysin classifiers overcall - with calibrated confidence revisions, gates re-locked.
