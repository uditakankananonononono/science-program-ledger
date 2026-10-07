# P3 preregistration (locked before any density/conservation computation)
Data: NCBI nuccore efetch FASTA, sha256: NC_000913.3 6b195feda4c66140f6762742eb8b30c2652f02b45878b174f5b00ef85ecc95d7; NC_001416.1 78a78913d3585570fa28b7cec05e4fcf067c1aaa3740d37a377f2babda70618c; NC_001422.1 caa155c83967cc080f4f188f14f1f28c18d77448e87c3d00d3579ed348f4de2a. NCBI policy: no NCBI restriction, third-party rights not cleared; not CC0.
Params: k=15, w=10 (window of w consecutive k-mers). Non-ACGT removed (none expected). Canonical k-mers not used (forward strand only).
Arms (rank order, minimizer = leftmost lowest rank in each window): 
 B1 random: rank=splitmix64(kmer_int).
 B2 lexicographic: rank=kmer_int.
 NEW ECHO (entropy-gated hash order): rank=splitmix64(kmer_int) + 2^63*[k-mer low-complexity] where low-complexity = contains a homopolymer run >=5 OR has <=4 distinct 2-mers. Intent: avoid selecting repeat-prone k-mers, lowering spurious density and raising conservation.
Metrics: density = (#distinct selected positions)/(#k-mers); conservation = mean over 10 mutation seeds (0..9; 5% iid substitutions, position-preserving) of fraction of original selected positions also selected in the mutated sequence.
Reference: theoretical random density 2/(w+1)=0.1818.
WIN (per genome, all three required for project WIN): ECHO density <= B1 density*0.97 OR conservation >= B1 conservation +0.01, AND NOT (density > B1*1.03 or conservation < B1-0.01) (no material loss on the other metric). NEGATIVE: ECHO materially worse on either metric. Else NULL. Verbatim, no re-banding.
Equivalence check: ECHO with gate disabled must equal B1 exactly (asserted).

Amendment A1 (before any result): runner crashed with a dtype IndexError before computing anything; fix is an int64 cast in the 2-mer index. No logic, params or bands changed.
