# 88 druglib-aspect-sparse-stack

Algo50 batch 1 (builder lane, agent-run, not owner-verified). Result: WIN (agent-run) - test RMSE 2.0685 vs TF-IDF+Ridge 2.2386 (diff 0.1702, CI [0.0941,0.2473]); incremental stack, no ablation.
Protocol: PROTOCOL.md (locked before outcome evaluation; amendments appended inside). Code: code/run.py (expects data/ fetched from the sources and sha256 listed in PROTOCOL.md; raw data not committed). Results: results/.
Original local commit history preserved in the builder workspace only.

Robustness unit (locked before compute): ROBUST on 10 fresh random re-splits, mean RMSE diff +0.149 (CI [0.131,0.165], 10/10 splits). Ablation: the gain comes from the per-field stack; the sparsity step HURTS (stack without sparsity 2.126 vs ASL 2.145; concat+sparsity 2.351 vs baseline 2.294). The method name "aspect-sparse-lexicon" overstates; the supported claim is the aspect-wise stack.

Limitations: random splits ignore drug identity (reviews of one drug can sit in both train and test); one dataset; agent-run only. Supported method name: aspect-wise stacked ridge (sparsity step harms and is recorded as a negative component).
