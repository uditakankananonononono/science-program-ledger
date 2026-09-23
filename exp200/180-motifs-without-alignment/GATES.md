# DOC-2-080 Functional Motifs Without Alignment - locked gates (22:05 IST, before data download)

## Sandbox-fit slice
Protein-language-model motif discovery (ESM-scale) does not fit 1 GB RAM / no GPU. Slice: an alignment-free, model-free baseline that any PLM method must beat - over-represented k-mers in unaligned family members - tested on whether they land on experimentally annotated functional residues. Families: 20 Pfam families, reviewed Swiss-Prot members only (UniProt REST). Dev (method frozen here): PF00089, PF00069, PF00106, PF00561, PF00067. Test (never used for tuning): PF00071, PF00128, PF00085, PF00112, PF00026, PF00501, PF00378, PF00300, PF00248, PF00107, PF00144, PF00155, PF00202, PF00255, PF00462.

## Method (frozen)
Per family (<= 400 reviewed members, dedup identical seqs): document frequency (DF) of every contiguous 4-mer; expected DF from composition-preserving shuffles of each member (3 shuffles). Score = log2((DF+1)/(E+1)). Top 5 4-mers by score with DF >= 20% of members = motifs. Positions covered = all occurrences in members.
Functional residues: UniProt "Active site" + "Binding site" features on those members.

## Metric
Per family: site enrichment = (fraction of functional residues covered) / (fraction of all residues covered).

## Gates (on the 15 test families)
G1 median site enrichment >= 3.
G2 >= 11/15 families with enrichment > 1 (sign test p < 0.06).
G3 median fraction of functional residues covered >= 0.10 (motifs must reach a real share of sites, not one residue).
Failure policy: negative preserved; pivots appended with new locked gates.
