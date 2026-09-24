# GATES ADDENDUM B - DOC-1-033 (locked 2026-09-24 09:56 IST, before P1 runs, before dev CV completes)

## Trigger (feasibility fact, verified from CHERRY source edge_virus_prokaryote.py)
Locked P1 specified virus-prokaryote protein-sharing edges via mmseqs2 clusters on
protein.fasta joined to database_gene_to_genome.csv. Verification against the CHERRY source
shows protein.fasta and database_gene_to_genome.csv cover VIRUS proteins/genomes only; the
protein-sharing edges in the paper require prokaryote proteomes, which are outside the locked
scope (no prokaryote genomes). That edge type is not constructible in-envelope.

## Change (locked)
P1 (the single pre-registered rescue, if G2 fails) is redefined to the executable multimodal
augmentation: CRISPR-spacer-derived virus-prokaryote edges, replicating the paper's CRISPR
path exactly - blastn-short (evalue 1, perc_identity 90, gapopen 10, penalty -1) of all 1,875
virus genomes against the repo's prebuilt crispr_db (allCRISPRs), keeping hits with
alignment/spacer length > 0.95 and identity > 0.95, one predicted prokaryote per virus as in
the paper's code; added edges = those virus-prokaryote pairs. All gates (G2/G3 numbers)
unchanged. If blastn binaries cannot execute in-envelope, P1 is a documented dead end and the
G2-failure tree ends in a DOCUMENTED BOUNDARY.
