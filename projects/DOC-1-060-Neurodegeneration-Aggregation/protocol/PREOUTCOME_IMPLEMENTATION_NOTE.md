# Pre-outcome implementation note

Recorded 2026-09-21 before model fitting or inspection of class performance. ESM-2 has a 1,024-token context limit. Sequences longer than 1,000 residues are split into deterministic contiguous non-overlapping chunks of at most 1,000 residues. Per-residue embeddings are concatenated in original order, then protein mean and maximum pooling are computed. No labels enter this operation. This note clarifies mechanics without changing cohort, endpoints, gates, or success rules.
