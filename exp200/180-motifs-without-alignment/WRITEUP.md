# DOC-2-080 Functional Motifs Without Alignment - sandbox slice (exp200/180)

**Outcome: PASS on all locked gates (15 held-out Pfam families).**

## Setup
Running a protein language model was not possible in the sandbox (no GPU, 1 GB RAM). So this slice builds the model-free, alignment-free baseline that any PLM motif method should have to beat. Families: 20 Pfam families, up to 400 reviewed Swiss-Prot members each (first page of UniProt REST results, identical sequences removed). For each family: the document frequency of every 4-mer, vs composition-preserving shuffles. The top 5 over-represented 4-mers present in >= 20% of members are the motifs. Truth set: UniProt Active site + Binding site residues. The method was frozen on 5 dev families before the 15 test families were scored.

## Results (test families)
- Median site enrichment 9.3x (gate >= 3). 13/15 families > 1 (gate >= 11, sign p = 0.004). Median 15.4% of functional residues covered while motifs cover ~1-3% of all residues (gate >= 10%).
- Strongest cases: thioredoxin WCGPC (29x, 44% of sites), papain CGSCW/NSWG (19x), pepsin DTGS (19x), class-D beta-lactamase SxxK/SNTK (18x), aminotransferase class III (17x), enoyl-CoA hydratase (15x).
- Failures, kept: alpha-amylase PF00128 (0x) and glutathione peroxidase PF00255 (0x). Dev failure: P450 PF00067 (0.1x). In all three, the most conserved 4-mers sit next to the catalytic residues rather than on them. GPx's active residue is selenocysteine (U), which breaks every 4-mer that would contain it. P450's heme cysteine motif FxxGxxxCxG is gapped, so contiguous 4-mers catch only its FGAG end. Boundary: contiguous k-mers miss gapped motifs and non-standard residues.

## Useful result
A 20-line, alignment-free, model-free method already puts ~15% of annotated functional residues inside motifs covering ~2% of each sequence (9x enrichment) on held-out families. That makes it a floor any PLM "motif discovery without alignment" claim should beat under the same metric. The three failures show where a learned model could add value: gapped motifs and non-canonical residues.

## Limits and novelty
- Enriched-k-mer motif finding is old (PROSITE/MEME lineage). The contribution is the frozen benchmark and the held-out numbers, not the method.
- The UniProt "first 400" sampling is not random.
- Binding-site annotations are partly inferred by similarity, which can favour conserved stretches.
- Unit of analysis is the family, n = 15.

## Reproduce
python3 code/fetch.py; python3 code/run.py.
