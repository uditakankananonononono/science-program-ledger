# DOC-2-090 The Community Context of Unknown Genes - locked gates (21:53 IST, before data download)

## Sandbox-fit slice
MGnify/HMP metagenome co-occurrence at scale does not fit 2 CPU/1 GB. Proxy for "community context": STRING v11.0 phylogenetic co-occurrence channel (presence/absence of orthologs across ~5000 genomes = the gene's ecological/evolutionary company) plus the gene-neighbourhood channel, in two independent bacteria: E. coli K-12 (511145, KEGG eco) and B. subtilis 168 (224308, KEGG bsu).

## Question
Does co-occurrence context alone recover a gene's hidden function (KEGG pathway) better than chance, and how does it compare with genomic neighbourhood and co-expression?

## Protocol
Labels: KEGG REST link/pathway (eco, bsu), excluding global/overview maps (01100-01240). Genes with >=1 pathway are "known". Leave-one-out: hide the gene's labels, predict top-1 pathway by score-weighted vote of its neighbours (channel score >= 400) that are known. Channels evaluated separately: cooccurence, neighborhood, coexpression; "database" channel is excluded (it is derived from KEGG - leakage), reported only as a leakage ceiling.
Null: 200 permutations shuffling label sets among known genes (network fixed).

## Primary gate (must hold in BOTH organisms)
G1 cooccurence-channel top-1 precision (among genes with >= 1 known neighbour) >= 0.30.
G2 >= 3x null mean, empirical p < 0.01.
G3 coverage (fraction of known genes with a prediction) >= 0.15.
Secondary (reported, not gated): channel ranking; predictions for unannotated genes (y-genes).

## Failure policy
Negative preserved; pivots appended with new locked gates before computation.
