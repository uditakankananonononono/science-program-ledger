# 011F GATES ADDENDUM A — pool disjointness + decoy sourcing (locked 2026-09-24 12:58 IST, before any scoring)

Pool-definition refinements only; all thresholds from GATES.md unchanged (011 Addendum A pattern).
Live UniProtKB counts pulled 12:57.

1. Dev/frozen disjointness: GATES.md's dev sample "random 300 from all 1,824 Cas12f1"
   could overlap the post-2023 frozen set. Dev positives are therefore drawn from PRE-2023
   members only: (protein_name:Cas12f1) AND date_created <= 2022-12-31 = 1,107 live count,
   sample n=300 (rng seed 7); plus all pre-2023 Cas12b (n=6) and pre-2023 Cas12k (n=5).
   Dev remote positives total n=311. Frozen positives: post-2023 Cas12f1 (717) sample n=300
   (rng seed 7) + all post-2023 Cas12b (n=6) + all post-2023 Cas12k (n=20); total n=326.
   Zero accession overlap between dev and frozen by construction.
2. Decoy sourcing: dev decoys reuse 011's exact committed pools
   (exp200/011-crispr-plm-discovery/data/dev_decoys.fasta + hard_decoys.fasta = "011's decoy
   queries" per GATES.md), then the locked length filter [p5, p95] of the 311 dev positive
   lengths, then rng-seed-7 samples n=1,500 (bacterial) and n=300 (hard). If a length-eligible
   pool is smaller than its target n, take all eligible and disclose.
3. Frozen decoys: from decoy_frozen pool (1,529 live count, reviewed bacterial post-2023
   non-CRISPR), same length filter vs frozen-positive lengths, rng-seed-7 sample n=300.
