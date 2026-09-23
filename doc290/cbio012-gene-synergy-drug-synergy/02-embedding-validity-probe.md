---
id: P04-02
title: "Do GoBERT Function Embeddings Encode Real Biology? Intrinsic Probes Before Downstream Trust"
parent: "CBIO012 - The Usage of Gene Synergy to Predict Drug Synergy (source abstract, 2025)"
---

# Do GoBERT Function Embeddings Encode Real Biology?

**Parent project:** CBIO012 - assumes each GoBERT embedding dimension is a meaningful function probability.

## Premise
The whole framework rests on embedding quality. Intrinsic probes - held-out GO annotation recovery, protein interaction prediction, pathway coherence - can certify what the embeddings actually encode before they drive synergy claims.

## Hypothesis
GoBERT embeddings recover held-out experimental GO annotations at AUPRC >= 0.5 and predict held-out PPIs above a degree-matched null, but performance collapses for rarely annotated functions - bounding where the parent framework can be trusted.

## Data sources (free/public)
- GoBERT public model/embeddings; GO + GOA experimental annotations (public).
- BioGRID/STRING public PPIs; MSigDB pathways.

## Method outline
1. Lock a temporal holdout: train probes on annotations before a cutoff date, test on annotations after.
2. Linear + MLP probes per GO term (frequency-stratified); AUPRC vs annotation-count curves.
3. PPI probe: cosine similarity + trained scorer vs degree-matched negative sampling; pathway-coherence test (do same-pathway gene pairs score higher?).

## Success gates (locked before results)
- G1: held-out GO recovery AUPRC reported per frequency stratum; >= 0.5 for common terms required to certify the embeddings.
- G2: PPI prediction beats degree-matched null by >= 0.1 AUC.
- G3: a published "trust boundary" - annotation-count threshold below which embedding values must not be used downstream.

## Expected deliverable
`embedcert`: a probe suite that issues a per-function reliability certificate for any gene embedding set, pre-run for GoBERT.

## Failure/pivot rule
If embeddings fail common-term recovery, publish the certificate of non-reliability - downstream synergy conclusions from this framework are then capped accordingly.
