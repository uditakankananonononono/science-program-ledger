---
id: P15-03
title: "Beyond Hypothetical: Protein-Language-Model Function Assignment for Viral Dark Proteins"
parent: "CBIO045 - Viral Genome Annotation with RNNs (source abstract, 2024)"
---

# Beyond Hypothetical

**Parent project:** CBIO045 ViGAR (finding CDS locations - the first half of annotation).

## Premise
ViGAR solves where genes are; the harder half is what they do. Roughly half of all proteins in annotated viral genomes are "hypothetical." Protein language models and structure prediction now allow function assignment at scale, but viral proteins evolve fast and break homology tools. This project builds a viral-specific function-assignment pipeline (pLM embeddings + structure comparison + genomic-context signals), benchmarks it against homology tools on held-out annotated proteins, and quantifies the gain precisely: how many viral hypothetical proteins get a defensible function call that BLAST cannot make?

## Data sources
- RefSeq viral proteins with curated functional labels (public): benchmark set.
- UniProt viral entries + InterPro annotations (public).
- AlphaFold DB viral structures; PDB for Foldseek comparison.
- PHROGs / pVOGs (public viral ortholog groups) as family-level labels.

## Method outline
1. Build the benchmark: functionally labeled viral proteins, homology-masked at increasing identity cutoffs to simulate darkness.
2. Compare BLAST/InterPro vs. pLM-embedding classifiers vs. structure-based calls at each darkness level.
3. Add genomic-context features (neighbor functions, gene order conservation).
4. Run the winning stack over RefSeq hypothetical proteins; assign confidence-tiered calls.
5. Manual-audit a random top-tier sample against the literature for precision estimation.

## Success gates (locked before results)
- G1: on homology-masked benchmarks, the stack beats BLAST by >= 15 percentage points top-1 accuracy at 30% identity cutoff.
- G2: >= 25% of RefSeq hypothetical viral proteins receive a confidence-tiered call, with the tier precision estimated by audit >= 0.8.
- G3: all assignments carry calibrated confidence (ECE reported); no uncalibrated calls shipped.
- G4: negative space documented: the fraction that stays uncalled is reported with reasons.

## Expected deliverable
The function-assignment pipeline (open tool), the darkness-benchmark (reusable by the field), and the annotated RefSeq-hypothetical call set with confidence tiers.

## Failure/pivot rule
If audit precision fails G2, recalibration is mandatory; if it still fails, pivot to shipping the benchmark alone as the deliverable - the field needs the measurement instrument even without the calls - gates re-locked.
