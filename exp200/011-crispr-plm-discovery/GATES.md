# DOC-1-011 GATES - Discovering Novel CRISPR Systems with Protein Language Models
Locked 2026-09-24 04:52 IST by EXP-1 BEFORE any embeddings, retrieval scoring, or outcome evaluation.

## Concept
Can a small protein language model (PLM) retrieve CRISPR-Cas effector proteins from sequence alone, beating classical sequence-similarity search, including on systems reported only AFTER the PLM's training-data cutoff? If yes, the PLM embedding space is a cheap discovery engine for novel CRISPR systems in unannotated metagenomic sequence.

## Data (all free public, URLs + checksums in PROVENANCE.md at download)
- Seed families (training anchors): UniProtKB/Swiss-Prot REVIEWED Cas9, Cas12a, Cas13a sequences via REST API (rest.uniprot.org), capped at 150 per family (seeded random).
- Dev retrieval pool: held-out members of the same 3 families (disjoint from seeds, <=100/family) + 1,500 seeded decoys = reviewed bacterial proteins (E. coli K-12 + Bacillus subtilis proteome subsets) excluding any CRISPR-annotated entry + 300 hard decoys (reviewed non-CRISPR nucleases/polymerases: DNApol/RNApol/restriction-endonuclease annotated).
- FROZEN external validation: UniProtKB entries annotated as CRISPR-associated Cas9/Cas12/Cas13 effectors with entry creation date >= 2022-01-01 (after the UniRef50 snapshot used to train ESM-2, published 2021) + a fresh seeded decoy set. Documented caveat: some source metagenomic sequences may have existed in databases pre-2022; the freeze is on ANNOTATION/reporting, stated here upfront. FLSHclust (Altae-Tran et al., Science 2023, doi:10.1126/science.adi1910) Zenodo archive cited as context for the discovery-pipeline framing.

## Method under test
ESM-2 esm2_t6_8M_UR50D (8M params; smallest published ESM-2; CPU-feasible; weights dl.fbaipublicfiles.com). Mean-pooled final-layer embeddings, sequences truncated to 512 aa. Score = max cosine similarity to seed-family centroids. Retrieval AUROC: held-out Cas vs decoys.

## G1 - Named published baseline (beat or document loss)
MMseqs2 release 15-6f452 static AVX2 binary (Steinegger & Soding, Nature Biotechnology 2017; github.com/soedinglab/MMseqs2/releases) easy-search of the same dev pool against the same seed families; score = best -log10(e-value). Gate G1 PASS iff PLM dev AUROC STRICTLY EXCEEDS MMseqs2 dev AUROC. Pre-registered single fallback: if the static binary cannot execute in this environment, baseline = NCBI BLAST+ 2.15 static binaries (blastp, same scoring); if that also fails, boundary documented and G1 unscorable - NO weaker ad-hoc baseline substituted.

## G2 - Frozen temporal validation
Single scoring pass on the frozen post-2022 set. Gate G2 PASS iff frozen-set AUROC >= 0.80 AND within 0.10 of dev AUROC (no tuning on frozen set; thresholds/hyperparams fixed from dev).

## G3 - Mechanistic interpretation vs literature
Nearest-seed-family assignments of top retrievals must be coherent with the Makarova et al. 2020 evolutionary classification (Nat Rev Microbiol 18:67-83) - e.g., Cas9/Cas12 (class 2 type II/V, DNA interference) should NOT dominate Cas13 (type VI, RNA interference) neighborhoods and vice versa; embedding-space clustering of the 3 seed families visualized (PCA) and interpreted. PASS iff assignments are coherent or incoherence is specifically explained.

## G4 - Working tool + prospective nomination
crispr_finder.py CLI: input multi-FASTA, output per-sequence effector-likelihood score + nearest seed family, smoke-tested. Nomination: Innovative Genomics Institute metagenome-mining program (Doudna) as prospective user for screening unannotated metagenomic contigs.

## Failure tree (locked)
If G1 or G2 FAILS on the single scoring pass: NO new arms, NO threshold/hyperparameter changes, NO family additions. Documented boundary with failure analysis. Compute cap: <= 3,000 total embeddings.
