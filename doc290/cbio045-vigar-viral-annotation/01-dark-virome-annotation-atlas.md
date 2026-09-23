---
id: P15-01
title: "Dark Virome Atlas: Annotating the 45,000 Unannotated GenBank Viral Genomes"
parent: "CBIO045 - Viral Genome Annotation with RNNs (source abstract, 2024)"
---

# Dark Virome Atlas

**Parent project:** CBIO045 ViGAR (BiLSTM viral CDS annotation; noted 45,342 GenBank viral genomes remain unannotated).

## Premise
ViGAR proved the model; this project does the job. GenBank holds tens of thousands of viral genomes with no CDS annotation - an invisible backlog that slows every downstream virology pipeline. This project applies a modernized annotation stack (the parent's RNN architecture retrained with current RefSeq plus protein-language-model refinement) to the complete unannotated backlog, with confidence scoring per prediction, and releases the result as an open, versioned annotation atlas. The scientific question underneath the engineering: does the dark virome look like the annotated one, or does systematic annotation bias mean unannotated genomes harbor different gene content - shorter ORFs, stranger proteins, new families?

## Data sources
- NCBI GenBank viral division (public): the unannotated genome set.
- NCBI RefSeq viral (public): training labels, current snapshot.
- AlphaFold DB / ESM Atlas: structure availability for novel predicted proteins.
- UniProt/InterPro: family assignment for validation.

## Method outline
1. Snapshot the current unannotated viral set with accession-version pinning for reproducibility.
2. Retrain the parent architecture on current RefSeq; add a pLM-based ORF-refinement stage.
3. Run the full backlog; attach per-CDS confidence scores and evidence tags.
4. Comparative analysis: gene-length distributions, family novelty, and protein-cluster composition vs. the annotated set.
5. Validate a stratified sample by structure model quality (AlphaFold pLDDT) and family-level consistency.

## Success gates (locked before results)
- G1: held-out RefSeq performance >= parent's reported bar (recall >= 96%, F1 >= 93%) before any backlog run.
- G2: full backlog processed with per-CDS confidence; >= 90% of genomes receive >= 1 high-confidence CDS.
- G3: bias analysis completed: annotated vs. dark-virome gene-content differences quantified with effect sizes, including the null result if they match.
- G4: atlas released versioned with a diff protocol so GenBank updates can be re-annotated incrementally.

## Expected deliverable
The versioned Dark Virome Annotation Atlas (data + browser), the bias study (are unannotated genomes different?), and the reusable annotation pipeline as an open tool.

## Failure/pivot rule
If retraining cannot reproduce G1 (data drift since 2024), that gap is itself the first finding: publish the drift measurement, fix the training protocol, gates re-locked before the backlog run.
